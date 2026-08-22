import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

prompt_old = r'"tip": "Tu consejo como IA experta explicando por qué elegiste esa cantidad de sellos y ese premio específicamente para su industria."\n}'
prompt_new = r""""tip": "Tu consejo como IA experta explicando por qué elegiste esa cantidad de sellos y ese premio específicamente para su industria.",
  "iconClass": "uno de estos exactos valores: fa-star (general), fa-mug-hot (cafeteria), fa-scissors (belleza), fa-dumbbell (gym), fa-paw (mascotas), fa-heart (salud), fa-tooth (dentista)"
}"""

js = js.replace(prompt_old, prompt_new)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    djs = f.read()

inject_js_old = r"if \(document\.getElementById\('program-type-select'\)\) document\.getElementById\('program-type-select'\)\.value = 'stamps';"
inject_js_new = """if (document.getElementById('program-type-select')) document.getElementById('program-type-select').value = 'stamps';
        if (document.getElementById('icon-class') && strategy.iconClass) {
            document.getElementById('icon-class').value = strategy.iconClass;
            if (typeof state !== 'undefined') state.iconClass = strategy.iconClass;
        }"""

djs = djs.replace(inject_js_old, inject_js_new)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(djs)

