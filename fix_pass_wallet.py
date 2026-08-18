import re

with open('pass.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        function downloadAppleWallet() {
            if (!globalCustomerId || !globalCampaignId) {
                alert("No se pudo identificar la campaña.");
                return;
            }
            const url = `/api/wallet/apple/${globalCustomerId}/${globalCampaignId}`;
            window.location.href = url;
        }"""

replacement = """        async function downloadAppleWallet() {
            if (!globalCustomerId || !globalCampaignId) {
                alert("No se pudo identificar la campaña.");
                return;
            }
            
            const btn = document.getElementById('btn-apple-wallet');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generando Pase...';
            btn.disabled = true;

            try {
                const url = `/api/wallet/apple/${globalCustomerId}/${globalCampaignId}`;
                const response = await fetch(url);
                if (!response.ok) {
                    const text = await response.text();
                    // Catch the 500 missing certs error gracefully
                    Swal.fire('Aviso del Sistema', text || 'Configuración de Apple Wallet pendiente.', 'info');
                    return;
                }
                const blob = await response.blob();
                const objUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = objUrl;
                a.download = 'fidelio.pkpass';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(objUrl);
            } catch (err) {
                console.error(err);
                Swal.fire('Error', 'No se pudo conectar con el servidor para generar la tarjeta.', 'error');
            } finally {
                btn.innerHTML = originalHTML;
                btn.disabled = false;
            }
        }"""

text = text.replace(target, replacement)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(text)
