import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace the require at the top
app_js = app_js.replace("const { generateStampsStrip } = require('./render_stamps.js');", "const { generatePremiumBanner } = require('./render_premium_banner.js');")

# Fix Client Route Fields
target_client_fields = """                storeCard: {
                    headerFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    primaryFields: campaign.type === 'stamps' ? [] : [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Saldo VIP" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "type", label: "TIPO", value: campaign.type === 'stamps' ? 'Sellos' : 'Cashback' }
                    ],
                    auxiliaryFields: [],"""

replacement_client_fields = """                storeCard: {
                    headerFields: [
                        { key: "status", label: "ESTADO", value: "ACTIVO" }
                    ],
                    primaryFields: [],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "progress", label: campaign.type === 'stamps' ? "SELLOS" : "CASHBACK", value: balanceVal }
                    ],
                    auxiliaryFields: [],"""

app_js = app_js.replace(target_client_fields, replacement_client_fields)

# Fix Client Route Image Injection
target_client_img = """        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateStampsStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Puppeteer strip generation failed", e);
            }
        }"""

replacement_client_img = """        try {
            const stripBuffer = await generatePremiumBanner(campaign.banner_url);
            if (stripBuffer) {
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            }
        } catch (e) {
            console.error("Premium banner generation failed", e);
        }"""

app_js = app_js.replace(target_client_img, replacement_client_img)


# Fix Demo Route Fields
target_demo_fields = """                storeCard: {
                    primaryFields: campaign.type === 'stamps' ? [] : [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Recompensa VIP" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "type", label: "TIPO", value: campaign.type === 'stamps' ? 'Sellos' : 'Cashback' }
                    ],"""

replacement_demo_fields = """                storeCard: {
                    headerFields: [
                        { key: "status", label: "ESTADO", value: "ACTIVO" }
                    ],
                    primaryFields: [],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "progress", label: campaign.type === 'stamps' ? "SELLOS" : "CASHBACK", value: "3 / 10" }
                    ],"""

app_js = app_js.replace(target_demo_fields, replacement_demo_fields)

# Fix Demo Route Image Injection
target_demo_img = """        // Geofencing (si hay sucursales)"""

replacement_demo_img = """        try {
            const stripBuffer = await generatePremiumBanner(campaign.banner_url);
            if (stripBuffer) {
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            }
        } catch (e) {
            console.error("Premium banner generation failed", e);
        }
        
        // Geofencing (si hay sucursales)"""

app_js = app_js.replace(target_demo_img, replacement_demo_img)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
