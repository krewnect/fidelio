with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_js = """

// --- FIDELIO CARD STUDIO (CANVA LOGIC) ---
window.switchToolTab = function(tabId) {
    document.querySelectorAll('.tool-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tool-content').forEach(c => {
        c.classList.remove('active');
        // Quitar block si tenía inline display block (por seguridad)
        c.style.display = '';
    });
    
    // El elemento que hizo click
    event.target.classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');
};

window.applyTemplate = function(templateId) {
    const pPrimary = document.getElementById('pass-primary');
    const pAccent = document.getElementById('pass-accent');
    
    if(templateId === 'luxury') {
        if(pPrimary) pPrimary.value = '#1e293b';
        if(pAccent) pAccent.value = '#fbbf24';
        window.applyMaterial('titanium');
    } else if(templateId === 'neon') {
        if(pPrimary) pPrimary.value = '#000000';
        if(pAccent) pAccent.value = '#ec4899';
        window.applyMaterial('neon');
    } else if(templateId === 'minimal') {
        if(pPrimary) pPrimary.value = '#ffffff';
        if(pAccent) pAccent.value = '#3b82f6';
        window.applyMaterial('glass');
    }
    
    // Disparar input para que updatePassRender lo detecte
    if(pPrimary) pPrimary.dispatchEvent(new Event('input'));
    window.showToast("Plantilla aplicada.", "success");
};

window.applyMaterial = function(material) {
    const card = document.querySelector('.card-front');
    if(!card) return;
    
    // Limpiar clases y estilos anteriores
    card.style.background = '';
    card.style.backdropFilter = '';
    card.style.boxShadow = '';
    card.style.border = '';
    card.classList.remove('mat-glass', 'mat-titanium', 'mat-neon');
    
    if(material === 'glass') {
        card.style.background = 'rgba(255,255,255,0.4)';
        card.style.backdropFilter = 'blur(20px)';
        card.style.border = '1px solid rgba(255,255,255,0.6)';
        card.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
        document.body.style.setProperty('--pass-text-main', '#1e293b');
    } else if(material === 'titanium') {
        card.style.background = 'linear-gradient(135deg, #334155, #0f172a, #1e293b)';
        card.style.border = '1px solid #475569';
        card.style.boxShadow = 'inset 0 0 20px rgba(255,255,255,0.1), 0 20px 40px rgba(0,0,0,0.5)';
        document.body.style.setProperty('--pass-text-main', '#ffffff');
    } else if(material === 'neon') {
        card.style.background = '#000000';
        card.style.border = '2px solid #ec4899';
        card.style.boxShadow = 'inset 0 0 30px #ec4899, 0 0 30px #ec4899';
        document.body.style.setProperty('--pass-text-main', '#ffffff');
    }
    
    // Actualizar color de texto en elementos (si updatePassRender está escuchando variables CSS, funciona mejor, pero lo forzamos visualmente aquí)
    const textEls = card.querySelectorAll('#render-name, #render-promo-text, #render-reward-text, #render-stamps-total-text');
    textEls.forEach(el => {
        el.style.color = material === 'glass' ? '#1e293b' : '#ffffff';
    });
};

window.handleLogoDrop = function(e) {
    e.preventDefault();
    document.getElementById('builder-canvas').classList.remove('drag-active');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const logoPreview = document.getElementById('render-logo');
            if(logoPreview) {
                logoPreview.innerHTML = `<img src="${event.target.result}" style="width: 100%; height: 100%; object-fit: contain; border-radius: 50%;">`;
                window.showToast("Logo aplicado con Drag & Drop", "success");
            }
        };
        reader.readAsDataURL(file);
    }
};

"""

if "FIDELIO CARD STUDIO (CANVA LOGIC)" not in js:
    js = js + new_js
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Injected Studio Logic")
else:
    print("Already injected")
