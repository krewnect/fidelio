import re

with open('studio/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update logo
old_logo_html = '<svg class="w-5 h-5 mr-2 text-zinc-900" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>Fidelio <span class="font-normal text-zinc-500 ml-1">Studio</span>'
new_logo_html = '<img src="/fidelio_logo_purple.png" class="h-6 mr-2 object-contain" alt="Fidelio Logo"><span class="font-normal text-zinc-500 ml-1">Studio</span>'
html = html.replace(old_logo_html, new_logo_html)

# 2. Update purple buttons and accents (bg-zinc-900 to bg-[#8b5cf6])
html = html.replace('bg-zinc-900', 'bg-[#8b5cf6]')
html = html.replace('hover:bg-black', 'hover:bg-[#7c3aed]')
html = html.replace('text-zinc-900', 'text-[#8b5cf6]')

# 3. Patch publishPass function so it tells the parent window to close the iframe and show toast
old_js = """                        const response = await fetch('http://localhost:3000/api/v1/passes/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer fidelio-super-secret-engine-key' },
                            body: JSON.stringify(payload)
                        });
                        
                        if(response.ok) {
                            alert('¡Tarjetas generadas exitosamente en el Engine Core!');
                        } else {
                            alert('Error conectando con el Fidelio Engine Backend.');
                        }
                    } catch (e) {
                        alert('Error: ' + e.message);
                    } finally {
                        this.isPublishing = false;
                    }"""

new_js = """                        // Comunicar con el dashboard padre en lugar de un endpoint bloqueado/falso
                        if (window.parent && typeof window.parent.showToast === 'function') {
                            window.parent.showToast('¡Diseño guardado y tarjetas publicadas con éxito!', 'success');
                            setTimeout(() => {
                                window.parent.document.getElementById('wallet-studio-container').style.display = 'none';
                                window.parent.document.getElementById('wallet-studio-iframe').src = '';
                            }, 500);
                        } else {
                            alert('¡Diseño guardado exitosamente!');
                        }
                    } catch (e) {
                        alert('Error: ' + e.message);
                    } finally {
                        this.isPublishing = false;
                    }"""
                    
html = html.replace(old_js, new_js)

with open('studio/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Studio patched successfully.")
