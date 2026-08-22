import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            state.stampsReward = "Felicidades, ganaste un premio.";
            state.dynamicDesc = "Acumula sellos para ganar.";
        }"""

replacement = """            state.stampsReward = "Felicidades, ganaste un premio.";
            state.dynamicDesc = "Acumula sellos para ganar.";
            state.activeMode = 'stamps';
        }"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
