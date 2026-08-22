import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

toast_css_injection = """    window.showToast = function(message, type = "info") {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
            
            // INJECT TOAST CSS DYNAMICALLY BECAUSE IT WAS MISSING
            const style = document.createElement('style');
            style.innerHTML = `
                .toast-container { position: fixed; bottom: 20px; right: 20px; display: flex; flex-direction: column; gap: 10px; z-index: 999999; }
                .toast-msg { background: #ffffff; color: #111827; border-left: 4px solid #3b82f6; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); border-radius: 8px; padding: 16px 20px; min-width: 300px; display: flex; align-items: center; justify-content: space-between; font-family: sans-serif; font-size: 14px; font-weight: 600; animation: slideInUp 0.3s ease-out forwards; }
                .toast-msg i { font-size: 18px; margin-right: 12px; }
                .toast-msg.success { border-left-color: #10B981; }
                .toast-msg.error { border-left-color: #EF4444; }
                .toast-msg.warning { border-left-color: #F59E0B; }
                @keyframes slideInUp { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            `;
            document.head.appendChild(style);
        }"""

js = js.replace("""    window.showToast = function(message, type = "info") {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }""", toast_css_injection)

# Add the correct classes so the CSS applies
js = js.replace("toast.className = 'toast-msg';", "toast.className = 'toast-msg ' + type;")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
