with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """window.triggerAIMagicDesign = function() {
    if (typeof showToast === 'function') showToast("IA Analizando tu industria...", "info");
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    setTimeout(() => {
        let aiTip = "";
        let newStamps = 10;
        
        if (state.category === 'medico') {"""

replacement = """window.triggerAIMagicDesign = function() {
    if (typeof showToast === 'function') showToast("IA Analizando tu industria...", "info");
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    setTimeout(() => {
        let aiTip = "";
        let newStamps = 10;
        
        // Smart AI detection
        const catInputVal = document.getElementById('business-category-input') ? document.getElementById('business-category-input').value.toLowerCase() : '';
        const iconVal = document.getElementById('rest-icon') ? document.getElementById('rest-icon').value : '';
        
        let detectedCategory = state.category || 'general';
        if (iconVal === 'fa-stethoscope' || catInputVal.includes('salud') || catInputVal.includes('medico') || catInputVal.includes('doctor') || catInputVal.includes('dentista') || catInputVal.includes('clinica')) {
            detectedCategory = 'medico';
        } else if (iconVal === 'fa-scissors' || catInputVal.includes('belleza') || catInputVal.includes('spa') || catInputVal.includes('barber') || catInputVal.includes('salon')) {
            detectedCategory = 'belleza';
        } else if (iconVal === 'fa-dumbbell' || catInputVal.includes('gym') || catInputVal.includes('crossfit') || catInputVal.includes('fitness')) {
            detectedCategory = 'clases';
        }
        
        if (detectedCategory === 'medico') {"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
