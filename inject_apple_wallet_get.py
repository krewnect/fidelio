import re

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the new GET route for customers to download the pass
new_get_route = """
// Generar Pase de Apple Wallet para Clientes (Descarga Directa)
app.get('/api/wallet/apple/:customerId/:campaignId', apiLimiter, async (req, res) => {
    const { customerId, campaignId } = req.params;
    if (!customerId || !campaignId) return res.status(400).send('Falta customerId o campaignId');

    try {
        const { PKPass } = require('passkit-generator');
        
        // Credenciales de Apple
        const wwdr = process.env.APPLE_WWDR_CERT; 
        const signerCert = process.env.APPLE_SIGNER_CERT; 
        const signerKey = process.env.APPLE_SIGNER_KEY; 
        const signerKeyPassphrase = process.env.APPLE_SIGNER_KEY_PASSPHRASE; 
        const teamIdentifier = process.env.APPLE_TEAM_ID;
        const passTypeIdentifier = process.env.APPLE_PASS_TYPE_ID;

        if (!wwdr || !signerCert || !signerKey || !teamIdentifier || !passTypeIdentifier) {
            return res.status(500).send('Apple Wallet no configurado en el servidor.');
        }

        // Fetch Customer
        const { data: customer, error: cErr } = await supabase.from('customers').select('*').eq('id', customerId).single();
        if (cErr || !customer) return res.status(404).send('Cliente no encontrado');

        // Fetch Campaign
        const { data: campaign, error: campErr } = await supabase.from('campaigns').select('*').eq('id', campaignId).single();
        if (campErr || !campaign) return res.status(404).send('Campaña no encontrada');

        // Fetch Customer_Campaign status
        const { data: cStatus } = await supabase.from('customer_campaigns').select('*').eq('customer_id', customerId).eq('campaign_id', campaignId).single();
        const stamps = cStatus ? cStatus.stamps_count : 0;
        const cashback = cStatus ? cStatus.balance_cashback : 0;
        
        const balanceVal = campaign.type === 'stamps' ? `${stamps} / ${campaign.rules_config.stamps_total || 5}` : `$${cashback}`;
        const labelVal = campaign.type === 'stamps' ? 'SELLOS' : 'CASHBACK';

        // Fetch Branches for Geofencing
        const { data: branches } = await supabase.from('branches').select('lat, lng, name').eq('merchant_id', campaign.merchant_id);

        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: `${customerId}|${campaignId}`,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fideliorewards.com/api/wallet",
                authenticationToken: customerId.replace(/-/g, '').substring(0, 16),
                organizationName: campaign.name || "Mi Negocio",
                description: campaign.description || "Tarjeta de Lealtad",
                logoText: campaign.name || "Mi Negocio",
                backgroundColor: campaign.color_primary || "#090d16",
                foregroundColor: "#ffffff",
                labelColor: campaign.color_accent || "#8b5cf6",
                storeCard: {
                    primaryFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" }
                    ],
                    backFields: [
                        { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` },
                        { key: "terms", label: "TÉRMINOS", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes." }
                    ]
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Código Cliente"
                }
            }
        });

        // Geofencing (si hay sucursales)
        if (branches && branches.length > 0) {
            const locations = branches.map(b => ({
                latitude: b.lat,
                longitude: b.lng,
                relevantText: `¡Hola! Estás cerca de ${b.name}. Pasa a escanear tu tarjeta.`
            }));
            pass.add('locations', locations);
        }

        // Cargar Certificados
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });

        // Intentar agregar iconos o logos customizados
        try {
            // El módulo passkit-generator requiere al menos un icono
            // Se asume que icon.png y logo.png existen en la raíz o cargarlos desde URL
            // Como fallback, Passkit-generator requiere archivos locales. 
            const fs = require('fs');
            if (fs.existsSync('./icon-192.png')) pass.add('icon.png', fs.readFileSync('./icon-192.png'));
            if (fs.existsSync('./icon-192.png')) pass.add('logo.png', fs.readFileSync('./icon-192.png'));
            
            // Si el user tiene strip_icon (Base64)
            if (campaign.stamp_icon_url && campaign.stamp_icon_url.startsWith('data:image')) {
                const base64Data = campaign.stamp_icon_url.replace(/^data:image\\/\\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.add('strip.png', stripBuffer);
            } else if (campaign.banner_url && campaign.banner_url.startsWith('data:image')) {
                const base64Data = campaign.banner_url.replace(/^data:image\\/\\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.add('strip.png', stripBuffer);
            }
        } catch(e) {
            console.error("Error agregando imagenes al pase:", e);
        }

        // Generar archivo binario (.pkpass)
        const buffer = await pass.getAsBuffer();
        
        // Responder
        res.set({
            'Content-Type': 'application/vnd.apple.pkpass',
            'Content-Disposition': `attachment; filename="${(campaign.name || 'tarjeta').replace(/[^a-z0-9]/gi, '_')}.pkpass"`
        });
        res.send(buffer);

    } catch (err) {
        console.error("Error Generando GET Apple Wallet:", err);
        res.status(500).send('Error interno generando el pase de Apple Wallet: ' + err.message);
    }
});
"""

# Insert it before the existing app.post('/api/wallet/apple')
content = content.replace("app.post('/api/wallet/apple'", new_get_route + "\napp.post('/api/wallet/apple'")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("app.js updated successfully with GET /api/wallet/apple route.")
