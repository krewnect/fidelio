const fs = require('fs');
let code = fs.readFileSync('pass.html', 'utf-8');

const regex = /function downloadAppleWallet\(\) \{[\s\S]*?window\.location\.href = url;\s*\}/;
const newCode = `async function downloadAppleWallet() {
            if (!globalCustomerId || !globalCampaignId) {
                alert("No se pudo identificar la campaña.");
                return;
            }
            
            const btn = document.getElementById('btn-apple-wallet');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generando Pase...';
            btn.disabled = true;

            try {
                const url = \`/api/wallet/apple/\${globalCustomerId}/\${globalCampaignId}\`;
                const response = await fetch(url);
                if (!response.ok) {
                    const text = await response.text();
                    Swal.fire('Aviso del Sistema', text || 'Configuración de Apple Wallet pendiente en el servidor (.env).', 'info');
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
        }`;

code = code.replace(regex, newCode);
fs.writeFileSync('pass.html', code);
