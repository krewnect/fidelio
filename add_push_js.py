import re

with open('dashboard.js', 'r') as f:
    js = f.read()

push_logic = """
    // --- PUSH OTA LOGIC ---
    const btnSavePush = document.getElementById('btn-save-design-push');
    const pushModal = document.getElementById('push-update-modal');
    const btnCancelPush = document.getElementById('btn-cancel-push');
    const btnConfirmPush = document.getElementById('btn-confirm-push');
    const btnClosePush = document.getElementById('btn-close-push');
    
    const step1 = document.getElementById('push-modal-step-1');
    const step2 = document.getElementById('push-modal-step-2');
    const step3 = document.getElementById('push-modal-step-3');
    
    const progressBar = document.getElementById('push-progress-bar');
    const progressText = document.getElementById('push-progress-text');
    
    if (btnSavePush && pushModal) {
        btnSavePush.addEventListener('click', () => {
            pushModal.style.display = 'flex';
            step1.style.display = 'block';
            step2.style.display = 'none';
            step3.style.display = 'none';
        });
        
        btnCancelPush.addEventListener('click', () => {
            pushModal.style.display = 'none';
        });
        
        btnClosePush.addEventListener('click', () => {
            pushModal.style.display = 'none';
            showToast("Diseño guardado y sincronizado con éxito", "success");
        });
        
        btnConfirmPush.addEventListener('click', () => {
            step1.style.display = 'none';
            step2.style.display = 'block';
            
            let count = 0;
            const total = 1428;
            
            // Simulate network APNs request
            const interval = setInterval(() => {
                count += Math.floor(Math.random() * 80) + 10;
                if (count >= total) {
                    count = total;
                    clearInterval(interval);
                    setTimeout(() => {
                        step2.style.display = 'none';
                        step3.style.display = 'block';
                    }, 500);
                }
                
                const percent = (count / total) * 100;
                if (progressBar) progressBar.style.width = percent + '%';
                if (progressText) progressText.textContent = `${count.toLocaleString()} / ${total.toLocaleString()}`;
                
            }, 100);
        });
    }
    
    // --- UPLOAD HANDLERS ---"""

js = js.replace('// --- UPLOAD HANDLERS ---', push_logic)

with open('dashboard.js', 'w') as f:
    f.write(js)
