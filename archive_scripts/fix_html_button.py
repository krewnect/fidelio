import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the button to call a brand new globally guaranteed function
old_btn = '<button class="fidelio-btn-primary" onclick="window.openCampaignModal()"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar Nueva Campaña</button>'
new_btn = '<button class="fidelio-btn-primary" onclick="window.forceNewCampaignFlow()"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar Nueva Campaña</button>'

if old_btn in html:
    html = html.replace(old_btn, new_btn)
else:
    print("WARNING: Could not find old_btn")

# Inject the function directly into the HTML to completely bypass any external JS caching
injection = """
    <!-- FORCE NEW CAMPAIGN FLOW INJECTION -->
    <script>
    window.forceNewCampaignFlow = function() {
        try {
            console.log("forceNewCampaignFlow triggered");
            // 1. Reset state if it exists
            if (typeof window.state !== 'undefined' && window.state) {
                window.state.currentCampaignId = null;
            }
            
            // 2. Hide all tabs forcefully
            document.querySelectorAll('.tab-content').forEach(t => {
                t.classList.remove('active');
                t.style.display = 'none';
            });
            document.querySelectorAll('.nav-tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // 3. Show loyalty tab
            const loy = document.getElementById('tab-loyalty');
            if (loy) {
                loy.classList.add('active');
                loy.style.display = 'block';
            } else {
                alert("DOM ERROR: tab-loyalty is missing!");
            }
            
            // 4. Toast
            if (typeof window.showToast === 'function') {
                window.showToast("Paso 1: Elige el Programa de Fidelización.", "success");
            }
        } catch (e) {
            alert("Error crítico en forceNewCampaignFlow: " + e.message);
        }
    };
    </script>
</body>
"""

html = html.replace('</body>', injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html patched")
