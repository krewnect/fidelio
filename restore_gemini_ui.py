import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert the AI banner right before "<!-- 1. IDENTIDAD -->"
target = r"<!-- 1\. IDENTIDAD -->"
ai_ui = """
                        <div style="margin-bottom: 32px; background: linear-gradient(135deg, rgba(139,92,246,0.1) 0%, rgba(59,130,246,0.1) 100%); padding:24px; border-radius:16px; display:flex; align-items:center; gap:20px; border:1px solid rgba(139,92,246,0.2);">
                            <div style="font-size:32px; filter:drop-shadow(0 4px 6px rgba(139,92,246,0.3)); animation: float 3s ease-in-out infinite;">🤖</div>
                            <div style="flex:1;">
                                <h4 style="margin:0 0 4px; font-size:16px; font-weight:800; color:#1e1b4b; display:flex; align-items:center; gap:8px;">Estratega IA (Gemini) <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); color:white; font-size:9px; padding:2px 6px; border-radius:6px; letter-spacing:1px; text-transform:uppercase;">Real AI</span></h4>
                                <p style="margin:0; font-size:13px; color:#475569; line-height:1.4;">Gemini 1.5 analizará el nombre y sector de tu negocio para diseñarte una estrategia de lealtad altamente rentable.</p>
                            </div>
                            <button id="btn-real-ai" onclick="triggerRealAIMagicDesign()" style="background:linear-gradient(135deg, #1e1b4b, #4c1d95); color:white; border:none; padding:12px 20px; border-radius:12px; font-weight:700; font-size:14px; cursor:pointer; transition:all 0.2s; box-shadow:0 4px 15px rgba(76,29,149,0.3); display:flex; align-items:center; gap:8px;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                <span><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar con IA</span>
                            </button>
                        </div>
                        
                        <!-- 1. IDENTIDAD -->"""

html = re.sub(target, ai_ui, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
