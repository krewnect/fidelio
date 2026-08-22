import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            state.activeMode = 'stamps';
            state.category = type;
        }
        
        state.restaurantName = camp.name || "Campaña";"""

replacement = """            state.activeMode = 'stamps';
        }
        
        state.restaurantName = camp.name || "Campaña";"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
