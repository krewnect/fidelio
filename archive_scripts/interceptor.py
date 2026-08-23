with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

interceptor = """
// --- FIDELIO STUDIO INTERCEPTOR ---
// Overrides any attempt to show the old loyalty tab and redirects to the new fullscreen iframe.
const observer = new MutationObserver((mutations) => {
    const loy = document.getElementById('tab-loyalty');
    if (loy && (loy.classList.contains('active') || loy.style.display === 'block')) {
        loy.classList.remove('active');
        loy.style.display = 'none';
        
        const container = document.getElementById('wallet-studio-container');
        const iframe = document.getElementById('wallet-studio-iframe');
        if (container && iframe && container.style.display !== 'block') {
            const restId = window.merchantData ? window.merchantData.id : '123';
            iframe.src = `/studio/index.html?rest_id=${restId}`;
            container.style.display = 'block';
            if (typeof window.showToast === 'function') {
                window.showToast("Cargando Fidelio Card Studio (Micro-Frontend)...", "success");
            }
        }
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const loy = document.getElementById('tab-loyalty');
    if(loy) {
        observer.observe(loy, { attributes: true, attributeFilter: ['class', 'style'] });
    }
});
// ----------------------------------
"""

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(interceptor + js)
print("Added mutation observer interceptor.")
