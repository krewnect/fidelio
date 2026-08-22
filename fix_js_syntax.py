import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_string = "if (!res.ok) const errData = await res.json().catch(()=>({})); throw new Error(errData.error || errData.insight || 'Error al conectar con Gemini');"
good_string = "if (!res.ok) { const errData = await res.json().catch(()=>({})); throw new Error(errData.error || errData.insight || 'Error al conectar con Gemini'); }"

js = js.replace(bad_string, good_string)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Syntax fixed.")
