import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Locate the map function that renders the campaigns
target_start = "list.innerHTML = data.campaigns"
target_end = "            }).join('');" # Wait, it ends with `.map(c => `...`).join('');`

# Let's extract and replace using a more precise regex.
pattern = re.compile(r'list\.innerHTML = data\.campaigns\s*\.filter\(c => \!\[.*?\]\.includes\(c\.type\)\)\s*\.map\(c => `(.*?)`\)\.join\(''\);', re.DOTALL)

new_card_html = """
            <div class="campaign-magic-card" style="position:relative; width: 100%; max-width: 340px; height: 180px; border-radius: 20px; cursor:pointer; perspective: 1000px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);" onclick="selectCampaign('${c.id}')">
                
                <!-- The actual card -->
                <div class="campaign-magic-inner" style="position:absolute; inset:0; border-radius: 20px; background: linear-gradient(135deg, ${c.color_primary||'#111827'}, ${c.color_accent||'#8b5cf6'}); box-shadow: 0 10px 30px -10px ${c.color_primary||'#111827'}; overflow: hidden; transition: all 0.4s; display: flex; flex-direction: column;">
                    
                    <!-- Top section with Wallet shape notch -->
                    <div style="padding: 20px 24px; flex: 1; display:flex; flex-direction:column; justify-content:space-between; position:relative; z-index:2;">
                        
                        <!-- Header -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div style="width: 44px; height: 44px; background: rgba(255,255,255,0.2); border-radius: 12px; display:flex; align-items:center; justify-content:center; backdrop-filter: blur(5px); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.3);">
                                ${c.logo_url ? `<img src="${c.logo_url}" style="width:100%; height:100%; border-radius:12px; object-fit:cover;">` : `<i class="fa-solid ${c.stamp_icon_url || 'fa-star'}" style="font-size:20px; color:white;"></i>`}
                            </div>
                            
                            <!-- Pulse Live Indicator -->
                            <div style="display:flex; align-items:center; gap:6px; background:rgba(0,0,0,0.3); padding:4px 10px; border-radius:20px; backdrop-filter:blur(5px);">
                                <div style="width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981; animation: pulseGlow 2s infinite;"></div>
                                <span style="color:white; font-size:10px; font-weight:800; letter-spacing:1px;">ACTIVA</span>
                            </div>
                        </div>
                        
                        <!-- Title -->
                        <div style="margin-top:auto;">
                            <h3 style="margin:0; font-size:22px; font-weight:800; letter-spacing:-0.5px; color:white; text-shadow: 0 2px 4px rgba(0,0,0,0.3); line-height:1.2;">${c.name || 'Sin Nombre'}</h3>
                            <p style="margin:4px 0 0; color:rgba(255,255,255,0.8); font-size:13px; font-weight:600;"><i class="fa-solid fa-qrcode" style="margin-right:4px;"></i> ${c.type === 'stamps' ? 'Tarjeta de Sellos' : 'Wallet'}</p>
                        </div>
                    </div>
                    
                    <!-- Decorative background shapes -->
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%); border-radius:50%;"></div>
                    <div style="position:absolute; bottom:-40px; left:-20px; width:150px; height:150px; background:radial-gradient(circle, rgba(0,0,0,0.1) 0%, transparent 70%); border-radius:50%;"></div>

                    <!-- Bottom Action Bar (slides up on hover) -->
                    <div class="campaign-magic-actions" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 12px 20px; display:flex; justify-content:space-between; align-items:center; transform: translateY(100%); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: absolute; bottom: 0; left: 0; width: 100%;">
                        <div style="color:var(--text-main); font-size:13px; font-weight:700;"><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-violet);"></i> Editar Magia</div>
                        <button class="btn-delete-campaign" onclick="event.stopPropagation(); window.deleteCampaign('${c.id}')" style="background:rgba(239, 68, 68, 0.1); border:none; color:#ef4444; width:32px; height:32px; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all 0.2s;" onmouseover="this.style.background='#ef4444'; this.style.color='white';" onmouseout="this.style.background='rgba(239, 68, 68, 0.1)'; this.style.color='#ef4444';"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
"""

def replacer(match):
    return r"""list.innerHTML = data.campaigns
            .filter(c => !['membership', 'multipass', 'certificates'].includes(c.type))
            .map(c => `""" + new_card_html + """`).join('');"""

js = pattern.sub(replacer, js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
