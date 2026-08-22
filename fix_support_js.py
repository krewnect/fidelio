import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

tut_js = """
window.openVideoTutorial = function(title, desc, icon, color) {
    const modal = document.getElementById('modal-video-tutorial');
    if (!modal) return;
    
    document.getElementById('video-tut-title').innerText = title;
    document.getElementById('video-tut-desc').innerText = desc;
    
    const iconBox = document.getElementById('video-tut-icon-box');
    iconBox.style.background = `linear-gradient(135deg, ${color}, #4c1d95)`;
    iconBox.style.boxShadow = `0 10px 25px ${color}40`;
    
    const iconEl = document.getElementById('video-tut-icon');
    iconEl.className = `fa-solid ${icon}`;
    
    modal.style.display = 'flex';
    // Trigger reflow
    void modal.offsetWidth;
    modal.style.opacity = '1';
    document.getElementById('video-tutorial-content').style.transform = 'scale(1)';
};

window.closeVideoTutorial = function() {
    const modal = document.getElementById('modal-video-tutorial');
    if (!modal) return;
    modal.style.opacity = '0';
    document.getElementById('video-tutorial-content').style.transform = 'scale(0.95)';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
};
"""

if "window.openVideoTutorial" not in js:
    js += "\n" + tut_js
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v3.js patched with openVideoTutorial.")
else:
    print("Already exists.")

