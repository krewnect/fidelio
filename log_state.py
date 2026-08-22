with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

script = """
    <script>
    window.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            let data = window.merchantData ? JSON.stringify(window.merchantData) : 'undefined';
            let plan = window.merchantData ? window.merchantData.business_type : 'N/A';
            console.error(`DIAGNOSTIC STATE:<br>business_type: ${plan}<br>isBusiness: ${plan === 'business' || plan === 'enterprise'}<br>DOM tabs loaded: ${document.querySelectorAll('.nav-tab').length}`);
        }, 3000);
    });
    </script>
"""
if "DIAGNOSTIC STATE" not in html:
    html = html.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
