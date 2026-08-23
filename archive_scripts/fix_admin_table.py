import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Specifically replace the contents of the last <td> in loadMerchantsControl
old_td = """                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="toggleMerchantStatus('${m.id}', '${m.plan_status}')" title="Pausar/Activar">
                            <i class="fa-solid ${m.plan_status === 'paused' ? 'fa-play' : 'fa-pause'}" style="color:var(--text-muted);"></i>
                        </button>
                        <button class="fidelio-btn-secondary-preset" onclick="grantFreeAccount('${m.id}')" title="Regalar Lifetime Free"><i class="fa-solid fa-gift" style="color:var(--accent-violet);"></i></button>
                    </td>"""

new_td = """                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="openAdminMerchant('${m.id}')" style="background:var(--bg-main); color:var(--text-main); padding:6px 12px; font-size:12px; border:1px solid var(--border-soft);">
                            <i class="fa-solid fa-sliders"></i> Administrar
                        </button>
                    </td>"""

if old_td in js:
    js = js.replace(old_td, new_td)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Table action buttons fixed.")
else:
    print("WARNING: Could not find old_td.")

