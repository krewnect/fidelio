with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "list.innerHTML = data.campaigns" in line:
        start_idx = i
    if "        `).join('');" in line and start_idx != -1 and end_idx == -1:
        end_idx = i

if start_idx != -1 and end_idx != -1:
    new_code = """        list.innerHTML = data.campaigns
            .filter(c => !['membership', 'multipass', 'certificates'].includes(c.type))
            .map(c => `
            <div class="campaign-magic-card" style="position:relative; width: 100%; max-width: 340px; height: 180px; border-radius: 20px; cursor:pointer; perspective: 1000px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);" onclick="selectCampaign('${c.id}')">
                
                <!-- The actual card using strict Fidelio Brand Colors (no ugly user colors here) -->
                <div class="campaign-magic-inner" style="position:absolute; inset:0; border-radius: 20px; background: linear-gradient(135deg, #2a0845 0%, #6441A5 100%); box-shadow: 0 10px 30px -10px rgba(100, 65, 165, 0.5); overflow: hidden; transition: all 0.4s; display: flex; flex-direction: column;">
                    
                    <!-- Top section with Wallet shape notch -->
                    <div style="padding: 20px 24px; flex: 1; display:flex; flex-direction:column; justify-content:space-between; position:relative; z-index:2;">
                        
                        <!-- Header -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div style="width: 44px; height: 44px; background: rgba(255,255,255,0.15); border-radius: 12px; display:flex; align-items:center; justify-content:center; backdrop-filter: blur(10px); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2);">
                                ${c.logo_url ? `<img src="${c.logo_url}" style="width:100%; height:100%; border-radius:12px; object-fit:cover;">` : `<i class="fa-solid ${c.stamp_icon_url || 'fa-star'}" style="font-size:20px; color:white;"></i>`}
                            </div>
                            
                            <!-- Pulse Live Indicator -->
                            <div style="display:flex; align-items:center; gap:6px; background:rgba(0,0,0,0.3); padding:4px 10px; border-radius:20px; backdrop-filter:blur(5px); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);">
                                <div style="width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981; animation: pulseGlow 2s infinite;"></div>
                                <span style="color:white; font-size:10px; font-weight:800; letter-spacing:1px;">ACTIVA</span>
                            </div>
                        </div>
                        
                        <!-- Title -->
                        <div style="margin-top:auto;">
                            <h3 style="margin:0; font-size:22px; font-weight:800; letter-spacing:-0.5px; color:white; text-shadow: 0 2px 4px rgba(0,0,0,0.3); line-height:1.2;">${c.name || 'Sin Nombre'}</h3>
                            <p style="margin:4px 0 0; color:rgba(255,255,255,0.7); font-size:13px; font-weight:600; letter-spacing: 0.5px; text-transform: uppercase;"><i class="fa-solid fa-qrcode" style="margin-right:4px;"></i> ${c.type === 'stamps' ? 'Tarjeta de Sellos' : 'Wallet Digital'}</p>
                        </div>
                    </div>
                    
                    <!-- Decorative background shapes for that premium Apple Wallet feel -->
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%); border-radius:50%;"></div>
                    <div style="position:absolute; bottom:-40px; left:-20px; width:150px; height:150px; background:radial-gradient(circle, rgba(0,0,0,0.2) 0%, transparent 70%); border-radius:50%;"></div>

                    <!-- Bottom Action Bar (slides up on hover) -->
                    <div class="campaign-magic-actions" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 12px 20px; display:flex; justify-content:space-between; align-items:center; transform: translateY(100%); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: absolute; bottom: 0; left: 0; width: 100%;">
                        <div style="color:#111827; font-size:13px; font-weight:800;"><i class="fa-solid fa-wand-magic-sparkles" style="color:#8b5cf6; margin-right:4px;"></i> Editar Diseño</div>
                        <button class="btn-delete-campaign" onclick="event.stopPropagation(); window.deleteCampaign('${c.id}')" style="background:rgba(239, 68, 68, 0.1); border:none; color:#ef4444; width:32px; height:32px; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all 0.2s;" onmouseover="this.style.background='#ef4444'; this.style.color='white';" onmouseout="this.style.background='rgba(239, 68, 68, 0.1)'; this.style.color='#ef4444';"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
        `).join('');\n"""
    
    lines[start_idx:end_idx+1] = [new_code]
    
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("SUCCESS: REPLACED LINES")
else:
    print(f"FAILED TO FIND TARGET. start={start_idx}, end={end_idx}")
