import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_functions = """window.selectSegment = function(segment) {
    document.querySelectorAll('.segment-card').forEach(c => c.classList.remove('selected'));
    const card = document.getElementById('seg-card-' + segment);
    if (card) card.classList.add('selected');
    
    const names = {
        'all': 'Todos los Clientes',
        'active': 'Frecuentes (Últimos 30 días)',
        'risk': 'En Riesgo (Sin visitas recientes)'
    };
    const targetEl = document.getElementById('selected-segment-name');
    if (targetEl) targetEl.textContent = names[segment] || 'Todos los Clientes';
};

window.selectCampaign = function(type) {
    document.querySelectorAll('.campaign-card').forEach(c => c.classList.remove('active'));
    event.currentTarget.classList.add('active');
    
    const txt = document.getElementById('push-message');
    if (!txt) return;

    if (type === 'recuperacion') {
        window.selectSegment('risk');
        txt.value = "¡Te extrañamos! Visítanos este fin de semana y obtén doble cashback en tu cuenta.";
    } else if (type === 'cumpleanos') {
        window.selectSegment('all');
        txt.value = "¡Es tu mes! Ven a celebrar con nosotros y recibe una cortesía sorpresa.";
    } else if (type === 'dias_lentos') {
        window.selectSegment('active');
        txt.value = "Oferta Flash: Ven hoy entre 4PM y 7PM y tu nivel sube a VIP por el día.";
    } else if (type === 'vip_exclusivo') {
        window.selectSegment('active');
        txt.value = "Alerta VIP Oro: Tenemos un beneficio exclusivo esperándote hoy. Muestra tu Apple Wallet.";
    } else if (type === 'resenas') {
        window.selectSegment('active');
        txt.value = "¡Gracias por tu última visita! Califícanos en Google Maps y gana 5 sellos extra.";
    } else if (type === 'manual') {
        window.selectSegment('all');
        txt.value = "";
    }
};"""

new_functions = """window.selectAICampaign = function(type, element) {
    // UI Update
    document.querySelectorAll('.campaign-module').forEach(c => c.classList.remove('active'));
    if(element) element.classList.add('active');
    
    const titles = {
        'recuperacion': '<i class="fa-solid fa-heart-crack" style="color:var(--accent-violet); margin-right:8px;"></i> Recuperar Perdidos',
        'cumpleanos': '<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:8px;"></i> Cumpleañeros del Mes',
        'dias_lentos': '<i class="fa-solid fa-clock" style="color:var(--accent-violet); margin-right:8px;"></i> Inyección Días Lentos',
        'vip_exclusivo': '<i class="fa-solid fa-crown" style="color:var(--accent-violet); margin-right:8px;"></i> Recompensa VIP',
        'manual': '<i class="fa-solid fa-pen-nib" style="color:var(--accent-violet); margin-right:8px;"></i> Campaña Libre'
    };
    
    const defaultTexts = {
        'recuperacion': '¡Te extrañamos! Vuelve esta semana y tu siguiente recarga tiene 50% de bono extra.',
        'cumpleanos': 'Celebra tu cumpleaños con nosotros. Muestra este mensaje para tu postre de cortesía.',
        'dias_lentos': '¡Hora feliz secreta! Solo por hoy de 4 a 6 PM tienes doble puntaje en todo.',
        'vip_exclusivo': 'Como miembro Oro, tienes un beneficio esperando. Actívalo en tu próxima compra.',
        'manual': ''
    };
    
    document.getElementById('config-camp-title').innerHTML = titles[type] || titles['manual'];
    
    const manualSelector = document.getElementById('manual-segment-selector');
    const select = document.getElementById('camp-segment-select');
    
    if(type === 'manual') {
        manualSelector.style.display = 'block';
    } else {
        manualSelector.style.display = 'none';
        if(type === 'recuperacion') select.value = 'risk';
        if(type === 'dias_lentos' || type === 'vip_exclusivo') select.value = 'active';
        if(type === 'cumpleanos') select.value = 'all';
    }
    
    document.getElementById('camp-push-message').value = defaultTexts[type] || '';
};

window.toggleChannel = function(checkbox) {
    const label = checkbox.parentElement;
    if(checkbox.checked) {
        label.classList.add('active');
        label.style.background = 'var(--accent-violet)';
        label.style.color = '#fff';
    } else {
        label.classList.remove('active');
        label.style.background = 'var(--bg-input)';
        label.style.color = 'var(--text-main)';
    }
};

window.updateTriggerUI = function() {
    // En el futuro, aquí se puede mostrar UI adicional de scheduling
};

window.generateAIPush = function() {
    const loading = document.getElementById('ai-loading');
    const txt = document.getElementById('camp-push-message');
    
    if (loading) loading.style.display = 'flex';
    
    // Simulate API call
    setTimeout(() => {
        if (loading) loading.style.display = 'none';
        const activeModule = document.querySelector('.campaign-module.active h4');
        const type = activeModule ? activeModule.textContent : 'Mensaje';
        
        // Simular diferentes variaciones de IA según el tamaño del texto actual
        if (txt.value.length < 10) {
            txt.value = `¡No te lo pierdas! ${type} exclusivo para ti. Ven y aprovéchalo hoy mismo.`;
        } else {
            txt.value = `🔥 [Optimizado por IA] ${txt.value} ¡Apresúrate antes de que expire!`;
        }
    }, 1500);
};"""

if old_functions in js:
    js = js.replace(old_functions, new_functions)
    with open('dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("JS functions updated successfully!")
else:
    print("Failed to find old JS functions.")
