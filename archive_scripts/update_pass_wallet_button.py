import re

with open('pass.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the alert button with a link to download the pass
old_button = """<button class="btn-wallet" onclick="alert('Esta función se habilitará próximamente tras la certificación de Apple Developer.')">
            <i class="fa-brands fa-apple"></i> Añadir a Apple Wallet
        </button>"""

new_button = """<button class="btn-wallet" id="btn-apple-wallet" onclick="downloadAppleWallet()">
            <i class="fa-brands fa-apple"></i> Añadir a Apple Wallet
        </button>"""

content = content.replace(old_button, new_button)

# Add the JS function
js_function = """
        function downloadAppleWallet() {
            if (!customerId || !campaignId) {
                alert("No se pudo identificar la campaña.");
                return;
            }
            // Redirigir a la URL que genera y descarga el archivo .pkpass
            const url = `/api/wallet/apple/${customerId}/${campaignId}`;
            window.location.href = url;
        }
"""

content = content.replace("function openAppointmentModal() {", js_function + "\n        function openAppointmentModal() {")

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("pass.html wallet button updated successfully.")
