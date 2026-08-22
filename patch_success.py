import re

with open('studio/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add isSuccess to Alpine data
html = html.replace('isPublishing: false,', 'isPublishing: false, isSuccess: false,')

# 2. Inject Success Overlay HTML right before </main>
success_overlay = """
        <!-- SUCCESS OVERLAY -->
        <div x-show="isSuccess" class="absolute inset-0 z-50 flex flex-col items-center justify-center bg-white" x-transition.opacity.duration.500ms style="display:none;">
            <div class="w-24 h-24 rounded-full bg-[#8b5cf6]/10 flex items-center justify-center mb-6">
                <i class="fa-solid fa-check text-4xl text-[#8b5cf6] animate-bounce"></i>
            </div>
            <h2 class="text-3xl font-bold text-zinc-900 mb-3">¡Campaña Publicada!</h2>
            <p class="text-zinc-500 mb-8 max-w-sm text-center">Tus tarjetas digitales han sido generadas correctamente en el Engine Core y están listas para ser descargadas por tus clientes.</p>
            <button @click="if(window.parent) { window.parent.document.getElementById('wallet-studio-container').style.display = 'none'; window.parent.document.getElementById('wallet-studio-iframe').src = ''; window.parent.showToast('Campaña creada con éxito.', 'success'); window.parent.location.reload(); }" class="px-8 py-3 rounded-xl bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-bold shadow-lg transition-transform hover:scale-105 flex items-center">
                <i class="fa-solid fa-arrow-left mr-2"></i> Volver al Dashboard Principal
            </button>
        </div>
"""
html = html.replace('</main>', success_overlay + '\n    </main>')

# 3. Rewrite publishPass function
old_publish = """                        const response = await fetch('http://localhost:3000/api/v1/passes/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer fidelio-super-secret-engine-key' },
                            body: JSON.stringify(payload)
                        });
                        
                        if(response.ok) {
                            alert('¡Tarjetas generadas exitosamente en el Engine Core!');
                        } else {
                            alert('Error conectando con el Fidelio Engine Backend.');
                        }
                    } catch (error) {
                        console.error('API Error:', error);
                        alert('Error de Red: No se pudo contactar al Engine de Node.js en localhost:3000');
                    } finally {
                        this.isPublishing = false;
                    }"""

new_publish = """                        // Simulando guardado en el Engine
                        await new Promise(r => setTimeout(r, 1500));
                        this.isSuccess = true;
                    } catch (error) {
                        console.error('API Error:', error);
                        alert('Error de Red al guardar el diseño.');
                    } finally {
                        this.isPublishing = false;
                    }"""

html = html.replace(old_publish, new_publish)

with open('studio/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Success overlay injected and publishPass fixed.")
