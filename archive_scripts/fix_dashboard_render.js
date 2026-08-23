const fs = require('fs');

let js = fs.readFileSync('dashboard.js', 'utf8');

const target = `        if (rFront) rFront.style.background = \`linear-gradient(135deg, \${cPri}, \${cAcc})\`;`;

const replacement = `        // Handle custom border and primary color text
        passRender.style.setProperty('--pass-primary', cPri);
        
        const renderStampsBody = document.getElementById('render-body-stamps');
        const renderCashbackBody = document.getElementById('render-body-cashback');
        const renderStampsGrid = document.getElementById('render-stamps-grid');
        const renderStampsTotalText = document.getElementById('render-stamps-total-text');
        
        if (pType === 'stamps') {
            if(renderStampsBody) renderStampsBody.style.display = 'flex';
            if(renderCashbackBody) renderCashbackBody.style.display = 'none';
            if(renderStampsTotalText) renderStampsTotalText.textContent = sTotal;
            
            // Generate Stamp Grid matching premium design
            if (renderStampsGrid) {
                let html = '<div style="position:absolute; top:50%; left:5%; right:5%; height:2px; background:#f3f4f6; z-index:0; transform:translateY(-50%);"></div>';
                const earnedStamps = 3; // Mock value for preview
                
                for(let i=1; i<=sTotal; i++) {
                    if (i <= earnedStamps) {
                        html += \`<div style="width:36px; height:36px; border-radius:50%; background:\${cPri}; color:white; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            <i class="fa-solid \${pIcon}"></i>
                        </div>\`;
                    } else {
                        html += \`<div style="width:36px; height:36px; border-radius:50%; background:white; border:2px solid #e5e7eb; color:#9ca3af; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            \${i}
                        </div>\`;
                    }
                }
                renderStampsGrid.innerHTML = html;
            }
        } else {
            if(renderStampsBody) renderStampsBody.style.display = 'none';
            if(renderCashbackBody) renderCashbackBody.style.display = 'flex';
        }`;

js = js.replace(target, replacement);

fs.writeFileSync('dashboard.js', js);
