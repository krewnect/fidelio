import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add JS Confetti script before closing head
if 'js-confetti' not in html:
    html = html.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/js-confetti@latest/dist/js-confetti.browser.js"></script>\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        if (error) {
            console.error("Save error:", error);
            if (typeof showToast === 'function') showToast("Error al guardar diseño", "error");
        } else {
            console.log("Campaña guardada");
            // Also save category to merchants table
            if (window.merchantSession && window.merchantSession.user) {
                window.supabaseClient.from('merchants')
                  .update({ category: state.category })
                  .eq('id', window.merchantSession.user.id)
                  .then(() => console.log("Categoría actualizada en merchant"));
            }
            if (typeof showToast === 'function') showToast("Campaña guardada exitosamente", "success");
        }"""

replacement = """        if (error) {
            console.error("Save error:", error);
            if (typeof showToast === 'function') showToast("Error al guardar diseño", "error");
        } else {
            console.log("Campaña guardada");
            // Also save category to merchants table
            if (window.merchantSession && window.merchantSession.user) {
                window.supabaseClient.from('merchants')
                  .update({ category: state.category })
                  .eq('id', window.merchantSession.user.id)
                  .then(() => console.log("Categoría actualizada en merchant"));
            }
            
            if (typeof showToast === 'function') showToast("Campaña guardada exitosamente", "success");
            
            // Micro-interaction: Confetti Dopamine Hit (only if user manually clicked save, usually when not auto-saving)
            // But we'll just do it if confetti is loaded
            try {
                if (window.JSConfetti) {
                    const jsConfetti = new window.JSConfetti();
                    jsConfetti.addConfetti({
                        emojis: ['✨', '🚀', '🎉', '🌟'],
                        confettiNumber: 40,
                    });
                }
            } catch(e) {}
        }"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
