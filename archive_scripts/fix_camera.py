import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add hidden file input next to the camera button
target_camera = """<div style="position:absolute; bottom: 0; right: 0; background: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; color: var(--accent-violet); font-size: 14px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                                    <i class="fa-solid fa-camera"></i>
                                </div>"""

replacement_camera = """<input type="file" id="acc-avatar-upload" accept="image/*" style="display:none;">
                                <div onclick="document.getElementById('acc-avatar-upload').click()" style="position:absolute; bottom: 0; right: 0; background: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; color: var(--accent-violet); font-size: 14px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                                    <i class="fa-solid fa-camera" id="acc-camera-icon"></i>
                                </div>"""

html = html.replace(target_camera, replacement_camera)

# Make sure avatar container can display an image
target_avatar = """<div class="animated-avatar" style="position:relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px; background: linear-gradient(135deg, var(--accent-violet), #c084fc); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; color: white; transition: all 0.3s ease;">
                                <span id="acc-avatar-letter">N</span>"""

replacement_avatar = """<div id="acc-avatar-container" class="animated-avatar" style="position:relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px; background: linear-gradient(135deg, var(--accent-violet), #c084fc); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; color: white; transition: all 0.3s ease; background-size: cover; background-position: center;">
                                <span id="acc-avatar-letter">N</span>"""

html = html.replace(target_avatar, replacement_avatar)

# Cache bust
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
