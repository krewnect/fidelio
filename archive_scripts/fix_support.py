import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a universal video tutorial modal to the end of the body
video_modal = """
    <!-- VIDEO TUTORIAL MODAL -->
    <div id="modal-video-tutorial" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000; align-items: center; justify-content: center; backdrop-filter: blur(5px); opacity: 0; transition: opacity 0.3s ease;">
        <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 20px; width: 90%; max-width: 700px; position: relative; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.4); display: flex; flex-direction: column; transform: scale(0.95); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);" id="video-tutorial-content">
            <button onclick="closeVideoTutorial()" style="position: absolute; top: 16px; right: 16px; background: #f3f4f6; border: none; color: #6b7280; width: 36px; height: 36px; border-radius: 50%; font-size: 18px; cursor: pointer; z-index: 10; transition: all 0.2s;"><i class="fa-solid fa-xmark"></i></button>
            
            <div style="padding: 24px 24px 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border-soft);">
                <div id="video-tut-icon-box" style="width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                    <i id="video-tut-icon" class="fa-solid fa-play"></i>
                </div>
                <div>
                    <h2 id="video-tut-title" style="font-size: 1.2rem; font-weight: 800; margin: 0; color: var(--text-main);">Tutorial</h2>
                    <p id="video-tut-desc" style="font-size: 13px; color: var(--text-muted); margin: 4px 0 0;">Cargando descripción...</p>
                </div>
            </div>

            <div style="padding: 24px; background: #f9fafb; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 350px;">
                <!-- Dummy Video Player -->
                <div style="width: 100%; height: 100%; min-height: 300px; background: #111827; border-radius: 12px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);">
                    <img src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&q=80&w=800&h=450" style="position: absolute; width: 100%; height: 100%; object-fit: cover; opacity: 0.4;">
                    <div style="position: relative; z-index: 2; text-align: center;">
                        <button style="width: 70px; height: 70px; border-radius: 50%; background: var(--accent-violet); border: none; color: white; font-size: 28px; cursor: pointer; margin-bottom: 16px; box-shadow: 0 10px 25px rgba(139,92,246,0.5); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                            <i class="fa-solid fa-play" style="margin-left: 4px;"></i>
                        </button>
                        <p style="color: white; font-weight: 600; font-size: 14px; margin: 0;">Fidelio Academy v2.0</p>
                        <p style="color: #9ca3af; font-size: 12px; margin: 4px 0 0;"><i class="fa-solid fa-clock"></i> 3:45 mins</p>
                    </div>
                </div>
            </div>
            
            <div style="padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; background: white; border-top: 1px solid var(--border-soft);">
                <button class="fidelio-btn-secondary" onclick="closeVideoTutorial()"><i class="fa-solid fa-book"></i> Leer Documentación</button>
                <button class="fidelio-btn-primary" onclick="closeVideoTutorial()">Entendido <i class="fa-solid fa-check"></i></button>
            </div>
        </div>
    </div>
"""

if "<!-- VIDEO TUTORIAL MODAL -->" not in html:
    html = html.replace('</body>', video_modal + '\n</body>')


def add_onclick(match):
    full_div = match.group(0)
    # Extract the icon and title to generate the onclick
    icon_match = re.search(r'<i class="fa-solid ([^"]+)" style="color:([^;]+);', full_div)
    title_match = re.search(r'<h4[^>]*>.*?<\/i> (.*?)<\/h4>', full_div)
    desc_match = re.search(r'<p[^>]*>(.*?)<\/p>', full_div)
    
    if icon_match and title_match and desc_match:
        icon = icon_match.group(1)
        color = icon_match.group(2)
        title = title_match.group(1)
        desc = desc_match.group(1)
        
        # Insert onclick before onmouseover
        new_div = full_div.replace('onmouseover=', f'onclick="window.openVideoTutorial(\'{title}\', \'{desc}\', \'{icon}\', \'{color}\')" onmouseover=')
        return new_div
    return full_div

# Find all tutorial cards and inject onclick
html = re.sub(r'<div style="background: [^"]+; padding: 16px; border-radius: 12px; cursor: pointer; transition:[^"]+" onmouseover=.*?</p>\s*</div>', add_onclick, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html patched with video tutorial modal and onclick handlers.")

