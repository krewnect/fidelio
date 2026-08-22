import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add global animation to tabs and sidebar items
magic_css = """
                    /* GLOBAL MAGIC ANIMATIONS */
                    .tab-content.active {
                        animation: staggerFadeIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards !important;
                    }
                    .sidebar-nav a {
                        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    }
                    .sidebar-nav a:hover {
                        transform: translateX(8px);
                        background: rgba(139, 92, 246, 0.05);
                        color: #8b5cf6;
                    }
                    .stats-grid > div {
                        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    }
                    .stats-grid > div:hover {
                        transform: translateY(-5px) scale(1.02);
                        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.15);
                        border-color: #8b5cf6;
                    }
"""
html = html.replace('/* MAGICAL ANIMATIONS & MICRO-INTERACTIONS */', magic_css + '\n                    /* MAGICAL ANIMATIONS & MICRO-INTERACTIONS */')

# 2. Inject Gemini Widget into Dashboard
gemini_dashboard = """
                <div id="gemini-dashboard-widget" style="margin-bottom: 32px; background: linear-gradient(135deg, rgba(139,92,246,0.05) 0%, rgba(59,130,246,0.05) 100%); padding:20px; border-radius:16px; border:1px solid rgba(139,92,246,0.2); display:flex; gap:16px; align-items:flex-start;">
                    <div style="font-size:24px; animation: pulseGlow 3s infinite alternate;">✨</div>
                    <div style="flex:1;">
                        <h4 style="margin:0 0 8px; font-size:14px; font-weight:800; color:#4c1d95; text-transform:uppercase; letter-spacing:1px;">Gemini AI Executive Summary</h4>
                        <p id="gemini-dashboard-text" style="margin:0; font-size:14px; color:#475569; line-height:1.5;">Analizando métricas de rendimiento en tiempo real...</p>
                    </div>
                    <button onclick="fetchGeminiDashboardInsights()" style="background:white; border:1px solid #ddd6fe; color:#8b5cf6; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer; font-size:12px; transition:all 0.2s;" onmouseover="this.style.background='#f5f3ff'" onmouseout="this.style.background='white'"><i class="fa-solid fa-rotate-right"></i> Actualizar IA</button>
                </div>
"""
target_dash = r'<div class="stats-grid" style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(200px, 1fr\)\); gap: 20px; margin-bottom: 40px;">'
html = html.replace(target_dash, gemini_dashboard + '\n' + target_dash)


# 3. Inject Gemini Widget into CRM
gemini_crm = """
                <div id="gemini-crm-widget" style="margin-bottom: 24px; background: linear-gradient(135deg, rgba(16,185,129,0.05) 0%, rgba(59,130,246,0.05) 100%); padding:20px; border-radius:16px; border:1px solid rgba(16,185,129,0.2); display:flex; gap:16px; align-items:flex-start;">
                    <div style="font-size:24px; animation: floatPhone 4s infinite alternate;">🧠</div>
                    <div style="flex:1;">
                        <h4 style="margin:0 0 8px; font-size:14px; font-weight:800; color:#065f46; text-transform:uppercase; letter-spacing:1px;">Gemini CRM Analyzer</h4>
                        <p id="gemini-crm-text" style="margin:0; font-size:14px; color:#475569; line-height:1.5;">Evaluando el estado de tu base de datos de clientes...</p>
                    </div>
                    <button onclick="fetchGeminiCRMInsights()" style="background:white; border:1px solid #a7f3d0; color:#10b981; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer; font-size:12px; transition:all 0.2s;" onmouseover="this.style.background='#ecfdf5'" onmouseout="this.style.background='white'"><i class="fa-solid fa-wand-magic-sparkles"></i> Analizar Audiencia</button>
                </div>
"""
target_crm = r'<div class="crm-toolbar" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">'
html = html.replace(target_crm, gemini_crm + '\n' + target_crm)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
