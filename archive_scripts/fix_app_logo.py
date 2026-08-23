import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Remove logoText entirely
app_js = re.sub(r'^\s*logoText:\s*.*?,?\n', '', app_js, flags=re.MULTILINE)

# Inject logic to download logo_url
target = """            const fs = require('fs');
            if (fs.existsSync('./icon-192.png')) {
                pass.addBuffer('icon.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('icon@2x.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('logo.png', fs.readFileSync('./icon-192.png'));
            }"""

replacement = """            const fs = require('fs');
            
            // Generate icon
            if (fs.existsSync('./icon-192.png')) {
                pass.addBuffer('icon.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('icon@2x.png', fs.readFileSync('./icon-192.png'));
            }
            
            // Download and add logo
            let logoAdded = false;
            if (campaign.logo_url && campaign.logo_url.startsWith('http')) {
                try {
                    const logoRes = await fetch(campaign.logo_url);
                    if (logoRes.ok) {
                        const logoArrayBuffer = await logoRes.arrayBuffer();
                        const logoBuffer = Buffer.from(logoArrayBuffer);
                        pass.addBuffer('logo.png', logoBuffer);
                        pass.addBuffer('logo@2x.png', logoBuffer);
                        logoAdded = true;
                    }
                } catch (err) {
                    console.error("Error downloading logo_url:", err);
                }
            } else if (campaign.logo_url && campaign.logo_url.startsWith('data:image')) {
                try {
                    const base64Data = campaign.logo_url.replace(/^data:image\/\\w+;base64,/, "");
                    const logoBuffer = Buffer.from(base64Data, 'base64');
                    pass.addBuffer('logo.png', logoBuffer);
                    pass.addBuffer('logo@2x.png', logoBuffer);
                    logoAdded = true;
                } catch (err) {
                    console.error("Error parsing base64 logo_url:", err);
                }
            }
            
            if (!logoAdded) {
                if (fs.existsSync('./icon-192.png')) {
                    pass.addBuffer('logo.png', fs.readFileSync('./icon-192.png'));
                }
            }"""

app_js = app_js.replace(target, replacement)

# There is a second occurrence of the target in the Demo route, let's just make sure we replace both if they exist.
# Wait, the demo route uses exactly the same code?
target2 = """            if (fs.existsSync('./icon-192.png')) {
                pass.addBuffer('icon.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('icon@2x.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('logo.png', fs.readFileSync('./icon-192.png'));
            }"""

app_js = app_js.replace(target2, replacement)

app_js = re.sub(r'v6_', 'v7_', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
