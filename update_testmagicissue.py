import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_magic_issue = """            const res = await window.MagicEngine.issueCard('user_test_123', config);
            console.log("Respuesta binaria del Engine:", res);
            window.showToast("¡Tarjeta emitida exitosamente! (Revisa la consola)", "success");"""

new_magic_issue = """            const res = await window.MagicEngine.issueCard('user_test_123', config);
            console.log("Respuesta binaria del Engine:", res);
            window.showToast("¡Tarjeta emitida exitosamente!", "success");
            alert("¡Simulación Exitosa! El Magic Engine procesó la orden correctamente.\\n\\nEsto significa que si hubiera un iPhone conectado, la tarjeta se instalaría en este momento con las funciones Deep Tech activadas.");"""

if "¡Simulación Exitosa!" not in html:
    html = html.replace(old_magic_issue, new_magic_issue)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated testMagicIssue.")
else:
    print("Already updated.")
