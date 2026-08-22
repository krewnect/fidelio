with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add event listener for magic-shape-select
if "safeAdd('magic-shape-select', 'change', updatePassRender);" not in js:
    js = js.replace("safeAdd('program-type-select', 'input', updatePassRender);", "safeAdd('program-type-select', 'input', updatePassRender);\n    safeAdd('magic-shape-select', 'change', updatePassRender);")

# Apply the shape in updatePassRender
# We need to find the definition of rFront in updatePassRender
search_str = "const rFront = document.getElementById('pass-front-face');"
replacement = """const rFront = document.getElementById('pass-front-face');
        
        // Morphing (Arquitectura Visual)
        const shapeSelect = document.getElementById('magic-shape-select');
        if (shapeSelect && rFront) {
            const shape = shapeSelect.value;
            if (shape === 'event_ticket') {
                rFront.style.maskImage = 'radial-gradient(circle at 0 50%, transparent 12px, black 13px), radial-gradient(circle at 100% 50%, transparent 12px, black 13px)';
                rFront.style.maskComposite = 'intersect';
                rFront.style.webkitMaskImage = 'radial-gradient(circle at 0 50%, transparent 12px, black 13px), radial-gradient(circle at 100% 50%, transparent 12px, black 13px)';
                rFront.style.webkitMaskComposite = 'source-in';
            } else if (shape === 'boarding_pass') {
                rFront.style.maskImage = 'radial-gradient(circle at 50% 0, transparent 15px, black 16px)';
                rFront.style.maskComposite = 'intersect';
                rFront.style.webkitMaskImage = 'radial-gradient(circle at 50% 0, transparent 15px, black 16px)';
                rFront.style.webkitMaskComposite = 'source-in';
            } else {
                rFront.style.maskImage = 'none';
                rFront.style.webkitMaskImage = 'none';
            }
        }
"""

if "const shapeSelect =" not in js:
    js = js.replace(search_str, replacement)
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched updatePassRender for morphing.")
else:
    print("Already patched.")
