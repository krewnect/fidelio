import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacements = [
    (
        "'<div style=\"text-align: center; color: var(--text-muted); font-size: 13px; padding: 20px 0;\">No hay actividad reciente.</div>'",
        "`<div style='text-align: center; padding: 30px 10px; background: rgba(139,92,246,0.05); border-radius: 16px; border: 1px dashed rgba(139,92,246,0.2);'><div style='font-size:32px; margin-bottom:12px;'>👻</div><h4 style='margin:0 0 8px; font-size:15px; color:var(--text-main);'>Todo está muy tranquilo...</h4><p style='margin:0; font-size:12px; color:var(--text-muted);'>Aún no tienes actividad. ¡Anima a tus clientes a visitarte!</p></div>`"
    ),
    (
        "'<div style=\"text-align:center; padding:20px 0;\">No hay clientes suficientes.</div>'",
        "`<div style='text-align: center; padding: 20px 10px; background: rgba(59,130,246,0.05); border-radius: 16px; border: 1px dashed rgba(59,130,246,0.2);'><div style='font-size:28px; margin-bottom:8px;'>👑</div><p style='margin:0; font-size:12px; color:var(--text-muted);'>Acumula escaneos para ver a tus top fans aquí.</p></div>`"
    ),
    (
        "`<tr><td colspan=\"5\" style=\"text-align:center; color: var(--text-muted); padding: 30px;\">No hay personal registrado.</td></tr>`",
        "`<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#a78bfa;'><i class='fa-solid fa-users-viewfinder'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Tu equipo está vacío</h4><p style='color:var(--text-muted); font-size:14px; margin-bottom:16px;'>Invita a tus cajeros o meseros para que puedan dar puntos y cobrar sin que tú tengas que estar presente.</p></div></td></tr>`"
    ),
    (
        "'<tr><td colspan=\"4\" style=\"text-align:center;\">No hay clientes registrados.</td></tr>'",
        "`<tr><td colspan='4' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#3b82f6;'><i class='fa-solid fa-face-sad-tear'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Sin clientes aún</h4><p style='color:var(--text-muted); font-size:14px;'>Comparte tu código QR en tu mostrador o redes sociales para empezar a captar lealtad.</p></div></td></tr>`"
    ),
    (
        "`<tr><td colspan=\"5\" style=\"text-align: center; padding: 40px; color: var(--text-muted);\">No hay movimientos registrados.</td></tr>`",
        "`<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#10b981;'><i class='fa-solid fa-receipt'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Cero Movimientos</h4><p style='color:var(--text-muted); font-size:14px;'>Aquí aparecerá todo el historial cuando tus clientes escaneen su tarjeta en caja.</p></div></td></tr>`"
    ),
    (
        "'<tr><td colspan=\"5\" style=\"text-align:center;\">Bandeja de entrada limpia. No hay tickets.</td></tr>'",
        "`<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#10b981;'><i class='fa-solid fa-inbox'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Bandeja Limpia</h4><p style='color:var(--text-muted); font-size:14px;'>¡Todo al día! No tienes mensajes ni tickets pendientes de revisar. Excelente trabajo.</p></div></td></tr>`"
    )
]

for target, replacement in replacements:
    js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
