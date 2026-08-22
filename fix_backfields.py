import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# For the Client Pass
# Find the passTypeIdentifier ... to ... barcodes: block and replace backFields.
# Actually it's easier to dynamically build the JSON object before `const pass = new PKPass(...)` 
# because we want conditional fields!

target_client = """        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: `${customerId}|${campaignId}`,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fideliorewards.com/api/wallet",
                authenticationToken: customerId.replace(/-/g, '').substring(0, 16),
                organizationName: campaign.name || "Mi Negocio",
                description: campaign.description || "Tarjeta de Lealtad",
                logoText: campaign.name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)",
                storeCard: {
                    headerFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || (campaign.type === 'stamps' ? "Recompensa" : "Saldo VIP") }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" },
                        { key: "status", label: "ESTADO", value: "Activo" }
                    ],
                    auxiliaryFields: [
                        { key: "type", label: "PROGRAMA", value: campaign.type === 'stamps' ? 'Tarjetas de Sellos' : 'Cashback VIP' }
                    ],
                    backFields: [
                        { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` },
                        { key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." },
                        { key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" }
                    ]
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);"""

replacement_client = """        const backFieldsArr = [
            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` }
        ];

        if (campaign.rules_config?.show_appointment_btn) {
            backFieldsArr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment` });
        }
        if (campaign.rules_config?.show_payment_btn) {
            backFieldsArr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment` });
        }

        backFieldsArr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
        backFieldsArr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });

        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: `${customerId}|${campaignId}`,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fideliorewards.com/api/wallet",
                authenticationToken: customerId.replace(/-/g, '').substring(0, 16),
                organizationName: campaign.name || "Mi Negocio",
                description: campaign.description || "Tarjeta de Lealtad",
                logoText: campaign.name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)",
                storeCard: {
                    headerFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || (campaign.type === 'stamps' ? "Recompensa" : "Saldo VIP") }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" },
                        { key: "status", label: "ESTADO", value: "Activo" }
                    ],
                    auxiliaryFields: [
                        { key: "type", label: "PROGRAMA", value: campaign.type === 'stamps' ? 'Tarjetas de Sellos' : 'Cashback VIP' }
                    ],
                    backFields: backFieldsArr
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);"""

app_js = app_js.replace(target_client, replacement_client)

# Now for the Demo Pass
target_demo = """        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: "DEMO_123",
                teamIdentifier: teamIdentifier,
                organizationName: merchant.business_name || "Mi Negocio",
                description: "Tarjeta de Lealtad",
                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)",
                storeCard: {
                    primaryFields: [
                        { key: "balance", label: "SALDO", value: `$${customer.current_balance}` }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" }
                    ],
                    backFields: [
                        { key: "portal", label: "PORTAL WEB", value: `https://fidelio.com/portal.html?id=${customer.id}` }
                    ]
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }
            }))
        }, certs);"""

replacement_demo = """        const backFieldsDemo = [
            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}` }
        ];

        if (campaign.rules_config?.show_appointment_btn) {
            backFieldsDemo.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment` });
        }
        if (campaign.rules_config?.show_payment_btn) {
            backFieldsDemo.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment` });
        }
        
        backFieldsDemo.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
        backFieldsDemo.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });

        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: "DEMO_123",
                teamIdentifier: teamIdentifier,
                organizationName: merchant.business_name || "Mi Negocio",
                description: "Tarjeta de Lealtad",
                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)",
                storeCard: {
                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Recompensa VIP" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" },
                        { key: "status", label: "ESTADO", value: "Demo Profesional" }
                    ],
                    backFields: backFieldsDemo
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: `${customer.id}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
