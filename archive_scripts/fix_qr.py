import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                                <div style="width:32px; height:32px; background:#FEF3C7; color:#D97706; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div>
                                Cobrar en Wallet
                            </button>
                        </div>
                    </div>"""

replacement = """                                <div style="width:32px; height:32px; background:#FEF3C7; color:#D97706; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div>
                                Cobrar en Wallet
                            </button>
                        </div>
                    </div>
                    
                    <div class="content-panel" style="margin-top: 24px;">
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 16px 0; display:flex; justify-content:space-between; align-items:center;">
                            <span>Código QR Universal</span>
                            <i class="fa-solid fa-qrcode" style="color: #6B7280;"></i>
                        </h3>
                        <p style="font-size: 13px; color: #6B7280; margin-bottom: 20px; line-height: 1.5;">Imprime y coloca este QR en mostrador. Los clientes elegirán qué tarjeta descargar.</p>
                        
                        <div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 16px;">
                            <img id="merchant-qr-preview" alt="Tu Código QR" style="width: 160px; height: 160px; mix-blend-mode: multiply; opacity: 0.9;" src="https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=cargando">
                        </div>

                        <button id="btn-download-merchant-qr" class="fidelio-btn-primary" style="width: 100%; justify-content: center;">
                            <i class="fa-solid fa-cloud-arrow-down" style="margin-right: 8px;"></i> Descargar Alta Calidad
                        </button>
                    </div>"""

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")
else:
    print("Target not found")
