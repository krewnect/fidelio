with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

injection = """
<!-- FIDELIO WALLET STUDIO MICRO-FRONTEND -->
<div id="wallet-studio-container" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:999999; background:#000;">
   <iframe id="wallet-studio-iframe" src="" style="width:100%; height:100%; border:none;"></iframe>
   <button onclick="document.getElementById('wallet-studio-container').style.display='none'; document.getElementById('wallet-studio-iframe').src='';" style="position:absolute; top:20px; left:20px; z-index:9999999; background:rgba(255,255,255,0.1); color:#fff; border:none; padding:10px 15px; border-radius:8px; cursor:pointer; font-family:var(--font-main); backdrop-filter:blur(10px);"><i class="fa-solid fa-arrow-left"></i> Volver al Dashboard</button>
</div>
</body>"""

html = html.replace("</body>", injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Injected iframe.")
