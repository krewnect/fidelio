import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_css = """                .toast-container { position: fixed; bottom: 20px; right: 20px; display: flex; flex-direction: column; gap: 10px; z-index: 999999; }
                .toast-msg { background: #ffffff; color: #111827; border-left: 4px solid #3b82f6; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); border-radius: 8px; padding: 16px 20px; min-width: 300px; display: flex; align-items: center; justify-content: space-between; font-family: sans-serif; font-size: 14px; font-weight: 600; animation: slideInUp 0.3s ease-out forwards; }
                .toast-msg i { font-size: 18px; margin-right: 12px; }
                .toast-msg.success { border-left-color: #10B981; }
                .toast-msg.error { border-left-color: #EF4444; }
                .toast-msg.warning { border-left-color: #F59E0B; }
                @keyframes slideInUp { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }"""

new_css = """                .toast-container { position: fixed; bottom: 40px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; gap: 12px; z-index: 999999; pointer-events: none; align-items: center; }
                .toast-msg { background: rgba(17, 24, 39, 0.9); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color: #ffffff; border-radius: 100px; padding: 12px 24px; display: flex; align-items: center; justify-content: center; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 0.3px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1); animation: fadeUpIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
                .toast-msg i { margin-right: 10px; font-size: 14px; opacity: 0.9; }
                .toast-msg.success i { color: #34D399; }
                .toast-msg.error { background: rgba(153, 27, 27, 0.95); }
                .toast-msg.error i { color: #FCA5A5; }
                .toast-msg.warning { background: rgba(146, 64, 14, 0.95); }
                .toast-msg.warning i { color: #FCD34D; }
                @keyframes fadeUpIn { from { transform: translateY(20px) scale(0.95); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }"""

js = js.replace(old_css, new_css)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
