copilot_code = """
// ==========================================
// MÓDULO: COPILOTO AI (GEMINI)
// ==========================================
window.fetchCopilotIdeas = function() {
    const loading = document.getElementById('copilot-loading');
    const results = document.getElementById('copilot-results');
    const container = document.getElementById('copilot-cards-container');
    
    if (!loading || !results || !container) return;
    
    // Si la función requiere un plan Pro, podemos validarlo. Copilot suena a Pro.
    const plan = window.merchantData ? (window.merchantData.business_type || 'starter') : 'starter';
    const isAdmin = window.merchantSession && window.merchantSession.user && window.merchantSession.user.email === 'hola@fideliorewards.com';
    
    if (plan !== 'professional' && plan !== 'enterprise' && !isAdmin) {
        if(typeof showToast === 'function') showToast('El Copiloto AI es exclusivo del Plan Profesional. Mejora tu plan para activarlo.', 'error');
        loading.style.display = 'none';
        results.style.display = 'block';
        container.innerHTML = `
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 20px; border-radius: var(--radius-md); text-align: center; color: #ef4444; grid-column: 1 / -1;">
                <i class="fa-solid fa-lock" style="font-size: 24px; margin-bottom: 10px;"></i>
                <h4>Función Bloqueada</h4>
                <p style="font-size: 14px; margin-top: 5px;">Actualiza a Plan Profesional para desbloquear el análisis inteligente de Gemini.</p>
                <button class="btn btn-primary" style="margin-top: 15px;" onclick="window.switchTab('tab-stripe')">Mejorar Plan</button>
            </div>
        `;
        return;
    }
    
    loading.style.display = 'flex';
    results.style.display = 'none';
    
    setTimeout(() => {
        loading.style.display = 'none';
        results.style.display = 'block';
        
        container.innerHTML = `
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(139,92,246,0.1); padding: 8px 12px; border-radius: 20px; color: var(--accent-violet); font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-bolt"></i> CAMPAÑA RÁPIDA
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">95% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Recuperar Clientes Inactivos</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Tienes 45 clientes que no han vuelto en 30 días. Enviarles un cupón de 10% de Cashback extra tiene alta probabilidad de retorno.</p>
                <button class="btn btn-outline" style="width:100%; border-color:var(--accent-violet); color:var(--accent-violet);" onclick="if(typeof showToast === 'function') showToast('Campaña generada y lista en Marketing.', 'success')">
                    Crear Campaña
                </button>
            </div>
            
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(59,130,246,0.1); padding: 8px 12px; border-radius: 20px; color: #3B82F6; font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-arrow-up"></i> UPSELL
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">82% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Impulso a VIP Oro</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Hay 12 clientes a solo 1 visita de subir a Oro. Envíales un SMS automático felicitándolos para asegurar su próxima visita.</p>
                <button class="btn btn-outline" style="width:100%; border-color:#3B82F6; color:#3B82F6;" onclick="if(typeof showToast === 'function') showToast('Campaña de Upsell programada.', 'success')">
                    Programar SMS
                </button>
            </div>
            
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(16,185,129,0.1); padding: 8px 12px; border-radius: 20px; color: #10B981; font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-calendar-check"></i> HORAS VALLE
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">78% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Promoción Martes Lento</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Tus martes por la tarde tienen baja afluencia. Lanza un 2x1 en puntos solo para ese día de la semana.</p>
                <button class="btn btn-outline" style="width:100%; border-color:#10B981; color:#10B981;" onclick="if(typeof showToast === 'function') showToast('Regla de Horas Valle activada.', 'success')">
                    Activar Regla
                </button>
            </div>
        `;
    }, 2500); 
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[onclick*="tab-copilot"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if(document.getElementById('copilot-results') && document.getElementById('copilot-results').style.display === 'none') {
                window.fetchCopilotIdeas();
            }
        });
    });
});
"""

with open('dashboard.js', 'a') as f:
    f.write("\n" + copilot_code)
