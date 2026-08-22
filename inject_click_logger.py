import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

logger_script = """
    <!-- CLICK LOGGER -->
    <script>
    window.addEventListener('DOMContentLoaded', () => {
        let logDiv = document.createElement('div');
        logDiv.style.cssText = 'position:fixed; bottom:0; right:0; width:300px; height:200px; background:rgba(0,0,0,0.8); color:lime; z-index:999999; font-family:monospace; font-size:10px; overflow-y:auto; padding:10px;';
        document.body.appendChild(logDiv);
        
        function logMsg(m) {
            logDiv.innerHTML += `<div>${m}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }
        
        logMsg("DOM Loaded");
        
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                logMsg(`Clicked tab: ${tab.getAttribute('data-tab')} (computed display: ${window.getComputedStyle(tab).display})`);
            });
        });
        
        setTimeout(() => {
            logMsg(`Total .nav-tab elements: ${document.querySelectorAll('.nav-tab').length}`);
            logMsg(`Is dashboard_v3.js loaded? ${typeof window.initFidelio !== 'undefined' || typeof window.checkPlanPermissions !== 'undefined'}`);
            logMsg(`User plan: ${window.merchantData ? window.merchantData.business_type : 'no data'}`);
        }, 3000);
    });
    </script>
</body>"""

if '</body>' in html:
    html = html.replace('</body>', logger_script)
    print("Injected click logger")
else:
    print("Could not find </body>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
