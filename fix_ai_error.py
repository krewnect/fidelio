import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make the frontend show the actual backend error message instead of a generic "No se pudo conectar"
def replace_catch(match):
    return match.group(0).replace("throw new Error('Error al conectar con Gemini');", "const errData = await res.json(); throw new Error(errData.error || errData.insight || 'Error desconocido del servidor');")

# Actually, a simpler replace:
js = js.replace("throw new Error('Error al conectar con Gemini');", "const errData = await res.json().catch(()=>({})); throw new Error(errData.error || errData.insight || 'Error al conectar con Gemini');")
js = js.replace("'<i style=\"color:#ef4444;\">No se pudo conectar con Gemini. Reintenta más tarde.</i>'", "'<i style=\"color:#ef4444;\">' + err.message + '</i>'")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated frontend AI error messages.")
