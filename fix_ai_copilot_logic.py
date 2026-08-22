import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = r'if \(state\.category === \'medico\'\) \{.*?\} else \{'
replacement = """
        // Smart AI detection
        const catInputVal = document.getElementById('business-category-input') ? document.getElementById('business-category-input').value.toLowerCase() : '';
        const iconVal = document.getElementById('rest-icon') ? document.getElementById('rest-icon').value : '';
        
        let detectedCategory = state.category || 'general';
        if (iconVal === 'fa-stethoscope' || catInputVal.includes('salud') || catInputVal.includes('medico') || catInputVal.includes('doctor') || catInputVal.includes('dentista')) {
            detectedCategory = 'medico';
        } else if (iconVal === 'fa-scissors' || catInputVal.includes('belleza') || catInputVal.includes('spa') || catInputVal.includes('barber') || catInputVal.includes('salon')) {
            detectedCategory = 'belleza';
        } else if (iconVal === 'fa-dumbbell' || catInputVal.includes('gym') || catInputVal.includes('crossfit') || catInputVal.includes('fitness')) {
            detectedCategory = 'clases';
        }
        
        if (detectedCategory === 'medico') {"""

js = re.sub(target, replacement, js, flags=re.DOTALL)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
