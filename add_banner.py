import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                                            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->"""
replacement = """                                            <!-- Middle Image Banner -->
                                            <div id="render-banner-container" style="display: none; width: 100%; height: 100px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;">
                                                <img id="render-banner-img" src="" style="width: 100%; height: 100%; object-fit: cover;">
                                            </div>

                                            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->"""

html = html.replace(target, replacement)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('pass.html', 'r', encoding='utf-8') as f:
    pass_html = f.read()

target_pass = """            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->"""
replacement_pass = """            <!-- Middle Image Banner -->
            <div id="ui-card-banner" style="display: none; width: 100%; height: 100px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;">
                <img id="ui-banner-img" src="" style="width: 100%; height: 100%; object-fit: cover;">
            </div>

            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->"""

pass_html = pass_html.replace(target_pass, replacement_pass)

# Update pass.html JS for banner
target_pass_js = """                if (campaign.logo_url) {"""
replacement_pass_js = """                if (campaign.banner_url) {
                    const bContainer = document.getElementById('ui-card-banner');
                    const bImg = document.getElementById('ui-banner-img');
                    bImg.src = campaign.banner_url;
                    bContainer.style.display = 'block';
                }
                
                if (campaign.logo_url) {"""
pass_html = pass_html.replace(target_pass_js, replacement_pass_js)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(pass_html)

