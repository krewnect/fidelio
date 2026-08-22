import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = r'window\.triggerAIMagicDesign = function\(\) \{.*?updatePassRender\(\);\n        \}\n        tipBox\.innerHTML = aiTip;\n        \n        try \{\n            if \(window\.JSConfetti\) \{\n                const jsConfetti = new window\.JSConfetti\(\);\n                jsConfetti\.addConfetti\(\{ emojis: \[\'📈\', \'💡\', \'🧠\'\], confettiNumber: 30 \}\);\n            \}\n        \} catch\(e\) \{\}\n        \n        setTimeout\(\(\) => \{ if\(iphone\) iphone\.style\.animation = ""; \}, 800\);\n    \}, 600\);\n\};'

replacement = """window.triggerAIMagicDesign = function() {
    if (typeof showToast === 'function') showToast("IA Analizando tu industria...", "info");
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    setTimeout(() => {
        // Smart AI detection
        const catInputVal = document.getElementById('business-category-input') ? document.getElementById('business-category-input').value.toLowerCase() : '';
        const iconVal = document.getElementById('rest-icon') ? document.getElementById('rest-icon').value : '';
        
        let cat = 'general';
        if (iconVal === 'fa-stethoscope' || catInputVal.includes('salud') || catInputVal.includes('medico') || catInputVal.includes('doctor') || catInputVal.includes('dentista') || catInputVal.includes('clinica')) {
            cat = 'medico';
        } else if (iconVal === 'fa-scissors' || catInputVal.includes('belleza') || catInputVal.includes('spa') || catInputVal.includes('barber') || catInputVal.includes('salon')) {
            cat = 'belleza';
        } else if (iconVal === 'fa-dumbbell' || catInputVal.includes('gym') || catInputVal.includes('crossfit') || catInputVal.includes('fitness')) {
            cat = 'clases';
        }

        const strategies = {
            medico: [
                { pri: '#064e3b', acc: '#10b981', reward: 'Consulta de Seguimiento Sin Costo', desc: 'Prioriza tu bienestar. Premia tu constancia.', stamps: 5, tip: "💡 Tip MKT IA: Metas cortas (5) en salud evitan que el paciente abandone el tratamiento. Aumenta el retorno un 42%." },
                { pri: '#1e3a8a', acc: '#3b82f6', reward: 'Limpieza Dental o Chequeo Básico Gratis', desc: 'La prevención es tu mejor recompensa.', stamps: 8, tip: "💡 Tip MKT IA: Ofrecer un servicio preventivo gratis asegura que el paciente vuelva para tratamientos más complejos." },
                { pri: '#4c1d95', acc: '#8b5cf6', reward: 'Descuento de $500 MXN en Especialidad', desc: 'Acumula tus visitas y obtén acceso VIP.', stamps: 10, tip: "💡 Tip MKT IA: Recompensas de alto valor monetario justifican metas largas (10 sellos) en clínicas de especialidad." }
            ],
            belleza: [
                { pri: '#be185d', acc: '#f472b6', reward: 'Masaje Capilar y Tratamiento VIP', desc: 'Tu lealtad merece ser consentida.', stamps: 6, tip: "💡 Tip MKT IA: En salones, regalar servicios que toman poco tiempo (masaje) no te cuesta pero se percibe carísimo." },
                { pri: '#0f172a', acc: '#fbbf24', reward: 'Corte Premium Gratis', desc: 'Mantén tu estilo impecable.', stamps: 8, tip: "💡 Tip MKT IA: El 'Corte Gratis' es el estándar de barberías. Pide 8 visitas para garantizar rentabilidad anual." },
                { pri: '#4c1d95', acc: '#d946ef', reward: 'Kit de Productos de Mantenimiento', desc: 'Lleva la experiencia del salón a tu casa.', stamps: 10, tip: "💡 Tip MKT IA: Regalar productos físicos como premio obliga al cliente a probar tu marca y luego comprarla." }
            ],
            clases: [
                { pri: '#ea580c', acc: '#f97316', reward: 'Sesión de Entrenamiento Personalizado', desc: 'Supera tus límites en cada visita.', stamps: 10, tip: "💡 Tip MKT IA: En fitness, regalar una sesión 1-a-1 genera un 'upsell' natural para vender planes privados." },
                { pri: '#111827', acc: '#10b981', reward: 'Análisis de Composición Corporal Gratis', desc: 'Mide tu progreso. Alcanza tu meta.', stamps: 5, tip: "💡 Tip MKT IA: Premiar con mediciones (InBody) a corto plazo motiva al usuario a renovar su mensualidad." },
                { pri: '#0f172a', acc: '#3b82f6', reward: 'Semana de Invitado VIP', desc: 'Entrena acompañado. Invita a un amigo.', stamps: 8, tip: "💡 Tip MKT IA: Regalar pases de invitado es marketing viral. Tu cliente te trae a un prospecto nuevo." }
            ],
            general: [
                { pri: '#1e1b4b', acc: '#8b5cf6', reward: 'Descuento del 20% en tu Ticket', desc: 'Gracias por preferirnos. Disfruta tu premio.', stamps: 8, tip: "💡 Tip MKT IA: Un descuento porcentual protege tus márgenes mientras el cliente siente un gran ahorro." },
                { pri: '#7f1d1d', acc: '#ef4444', reward: 'Producto Estrella o Postre Gratis', desc: 'Acumula compras y date un gusto.', stamps: 6, tip: "💡 Tip MKT IA: Regalar comida/producto en lugar de dinero reduce el costo real del premio a un tercio." },
                { pri: '#064e3b', acc: '#10b981', reward: 'Upgrade de Tamaño o Servicio Sin Costo', desc: 'Sube de nivel. Eres cliente VIP.', stamps: 5, tip: "💡 Tip MKT IA: El 'Upsize' gratis tiene el mayor retorno psicológico con el menor costo operativo." }
            ]
        };

        const options = strategies[cat] || strategies.general;
        const choice = options[Math.floor(Math.random() * options.length)];

        // Force update the actual inputs so they render in the DOM!
        if (document.getElementById('color-primary')) document.getElementById('color-primary').value = choice.pri;
        if (document.getElementById('color-accent')) document.getElementById('color-accent').value = choice.acc;
        if (document.getElementById('unified-reward')) document.getElementById('unified-reward').value = choice.reward;
        if (document.getElementById('stamps-reward')) document.getElementById('stamps-reward').value = choice.reward; // Fallback
        if (document.getElementById('unified-desc')) document.getElementById('unified-desc').value = choice.desc;
        if (document.getElementById('stamps-total')) document.getElementById('stamps-total').value = choice.stamps;

        // Ensure program type is stamps
        if (document.getElementById('program-type-select')) document.getElementById('program-type-select').value = 'stamps';

        let tipBox = document.getElementById('ai-tip-box');
        if (!tipBox) {
            tipBox = document.createElement('div');
            tipBox.id = 'ai-tip-box';
            tipBox.style = 'margin-top:20px; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3); border-radius:12px; padding:16px; color:#4c1d95; font-size:13px; font-weight:600; line-height:1.5; animation:fadeIn 0.5s;';
            const magicButton = document.querySelector('button[onclick="triggerAIMagicDesign()"]');
            if (magicButton && magicButton.parentElement && magicButton.parentElement.parentElement) {
                magicButton.parentElement.parentElement.appendChild(tipBox);
            }
        }
        tipBox.innerHTML = choice.tip;
        
        // Force the UI refresh
        if (typeof updatePassRender === 'function') updatePassRender();
        
        try {
            if (window.JSConfetti) {
                const jsConfetti = new window.JSConfetti();
                jsConfetti.addConfetti({ emojis: ['📈', '💡', '🧠', '✨'], confettiNumber: 40 });
            }
        } catch(e) {}
        
        setTimeout(() => { if(iphone) iphone.style.animation = ""; }, 800);
    }, 600);
};"""

js = re.sub(target, replacement, js, flags=re.DOTALL)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
