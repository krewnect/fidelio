import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update applyQuickTemplate to set category and label
target_wizard = "state.activeMode = 'stamps';"
def add_labels(match):
    return "state.activeMode = 'stamps';\n            state.category = type;\n"

js = js.replace("state.activeMode = 'stamps';", "state.activeMode = 'stamps';\n            state.category = type;")

# Also need to add category for custom
target_custom = "state.activeMode = 'stamps';\n        }"
replacement_custom = "state.activeMode = 'stamps';\n            state.category = 'custom';\n        }"
js = js.replace(target_custom, replacement_custom)


# 2. Update updatePassRender to use dynamic shapes, icons, and text
target_render_stamps = """        if (pType === 'stamps') {
            if(renderStampsBody) renderStampsBody.style.display = 'flex';
            if(renderCashbackBody) renderCashbackBody.style.display = 'none';
            if(renderStampsTotalText) renderStampsTotalText.textContent = sTotal;"""

replacement_render_stamps = """        if (pType === 'stamps') {
            if(renderStampsBody) renderStampsBody.style.display = 'flex';
            if(renderCashbackBody) renderCashbackBody.style.display = 'none';
            
            // Dynamic Label
            let unitLabel = "SELLOS";
            if (state.category === 'medico') unitLabel = "CONSULTAS";
            if (state.category === 'belleza') unitLabel = "VISITAS";
            if (state.category === 'clases') unitLabel = "CLASES";
            if(renderStampsTotalText) renderStampsTotalText.textContent = sTotal + " " + unitLabel;"""

js = js.replace(target_render_stamps, replacement_render_stamps)


target_loop = """            // Generate Stamp Grid matching premium design
            if (renderStampsGrid) {
                let html = '<div style="position:absolute; top:50%; left:5%; right:5%; height:2px; background:#f3f4f6; z-index:0; transform:translateY(-50%);"></div>';
                const earnedStamps = 3; // Mock value for preview
                
                for(let i=1; i<=sTotal; i++) {
                    if (i <= earnedStamps) {
                        html += `<div style="width:36px; height:36px; border-radius:50%; background:${cPri}; color:white; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            <i class="fa-solid ${pIcon}"></i>
                        </div>`;
                    } else {
                        html += `<div style="width:36px; height:36px; border-radius:50%; background:white; border:2px solid #e5e7eb; color:#9ca3af; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            ${i}
                        </div>`;
                    }
                }
                renderStampsGrid.innerHTML = html;
            }"""

replacement_loop = """            // Generate Stamp Grid matching premium design
            if (renderStampsGrid) {
                let html = '<div style="position:absolute; top:50%; left:5%; right:5%; height:2px; background:#f3f4f6; z-index:0; transform:translateY(-50%);"></div>';
                const earnedStamps = 3; // Mock value for preview
                
                // DYNAMIC SHAPES AND ICONS
                let shape = "50%"; // Default circle
                let emptyIcon = null;
                
                if (state.category === 'medico') { shape = "10px"; emptyIcon = "fa-heart"; }
                if (state.category === 'belleza') { shape = "50%"; emptyIcon = "fa-sparkles"; }
                if (state.category === 'clases') { shape = "6px"; emptyIcon = "fa-fire"; }
                
                for(let i=1; i<=sTotal; i++) {
                    if (i <= earnedStamps) {
                        html += `<div style="width:36px; height:36px; border-radius:${shape}; background:${cPri}; color:white; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; z-index:1; box-shadow:0 0 0 4px #ffffff; transform:scale(1.1); transition:all 0.3s;">
                            <i class="fa-solid ${pIcon}"></i>
                        </div>`;
                    } else {
                        const innerContent = emptyIcon ? `<i class="fa-solid ${emptyIcon}" style="opacity:0.3; font-size:12px;"></i>` : i;
                        html += `<div style="width:36px; height:36px; border-radius:${shape}; background:white; border:2px solid #e5e7eb; color:#9ca3af; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            ${innerContent}
                        </div>`;
                    }
                }
                renderStampsGrid.innerHTML = html;
            }"""

js = js.replace(target_loop, replacement_loop)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

