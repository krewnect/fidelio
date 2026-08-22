import re
with open('magic_bridge.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the real fetch with a mocked fetch for local development
old_fetch = """        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.message || `Error del Engine: ${response.status}`);
            }

            // Si el Engine devuelve el .pkpass o una imagen 3D renderizada, devolvemos el archivo (Blob)
            const contentType = response.headers.get('content-type');
            if (contentType && (contentType.includes('application/vnd.apple.pkpass') || contentType.includes('image/'))) {
                return await response.blob();
            }

            // Si devuelve datos o estado, devolvemos JSON
            return await response.json();
        } catch (error) {"""

new_fetch = """        try {
            // ===== SIMULACIÓN (MOCK) PARA DESARROLLO LOCAL =====
            console.log(`[MagicEngine] Mocking request to ${url} with payload:`, payload || (isMultipart ? 'FormData' : 'None'));
            await new Promise(r => setTimeout(r, 1200)); // Simulate processing delay
            
            if (endpoint === '/render') {
                console.log("[MagicEngine] Generando Blob .pkpass simulado...");
                return new Blob(['mock-pkpass-data'], { type: 'application/vnd.apple.pkpass' });
            }
            if (endpoint === '/decode') {
                return { status: 'success', data: { userId: '123', balance: 500, tier: 'oro' } };
            }
            
            return { status: 'success', message: 'Mocked successful response' };
            // ===================================================
        } catch (error) {"""

if "SIMULACIÓN (MOCK)" not in js:
    js = js.replace(old_fetch, new_fetch)
    with open('magic_bridge.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched magic_bridge.js to mock fetch.")
else:
    print("Already mocked.")
