with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("""            // 3. Show loyalty tab
            const loy = document.getElementById('tab-loyalty');
            if (loy) {
                loy.classList.add('active');
                loy.style.display = 'block';
            }""",
            """            // 3. Show loyalty tab
            const loy = document.getElementById('tab-loyalty');
            if (loy) {
                loy.classList.add('active');
                loy.style.display = 'block';
                loy.style.visibility = 'visible';
                loy.style.opacity = '1';
                loy.style.height = 'auto';
            }""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Patched forceNewCampaignFlow visibility.")
