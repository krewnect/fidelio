import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace the require
app_js = app_js.replace("const { generatePremiumBanner } = require('./render_premium_banner.js');", "const { generateHybridStrip } = require('./render_hybrid_strip.js');")

# Change storeCard to coupon
app_js = app_js.replace("                storeCard: {", "                coupon: {")

# Fix Client Route Image Injection
target_client_img = """        try {
            const stripBuffer = await generatePremiumBanner(campaign.banner_url);
            if (stripBuffer) {
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            }
        } catch (e) {
            console.error("Premium banner generation failed", e);
        }"""

replacement_client_img = """        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateHybridStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Hybrid strip generation failed", e);
            }
        }"""

app_js = app_js.replace(target_client_img, replacement_client_img)


# Fix Demo Route Image Injection
target_demo_img = """        try {
            const stripBuffer = await generatePremiumBanner(campaign.banner_url);
            if (stripBuffer) {
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            }
        } catch (e) {
            console.error("Premium banner generation failed", e);
        }"""

replacement_demo_img = """        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = 3;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateHybridStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Hybrid strip generation failed", e);
            }
        }"""

app_js = app_js.replace(target_demo_img, replacement_demo_img)

app_js = re.sub(r'serialNumber: `\$\{customerId\}\|\$\{campaignId\}\|v2_\$\{Date\.now\(\)\}`', r'serialNumber: `${customerId}|${campaignId}|v3_${Date.now()}`', app_js)
app_js = re.sub(r'serialNumber: `\$\{customer\.id\}\|v2_\$\{Date\.now\(\)\}`', r'serialNumber: `${customer.id}|v3_${Date.now()}`', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
