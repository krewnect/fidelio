/**
 * Fidelio Magic Engine - API Bridge
 * Este módulo actúa como el "Mesero", comunicando nuestra App Principal (CRM)
 * con el "Chef" (Magic Engine) que procesa la lógica profunda, renderizado 3D y esteganografía.
 */

class MagicEngineBridge {
    constructor() {
        // Entorno de ejecución en laboratorio (Localhost)
        this.baseURL = 'http://localhost:3000/api/engine';
        
        // Token maestro interno para proteger la comunicación (Seguridad Inter-Servicios)
        this.internalApiKey = 'fidelio-super-secret-engine-key'; 
    }

    /**
     * Motor interno de peticiones (Helper)
     * Maneja automáticamente la autenticación y el tipo de respuesta (JSON o Binario/Archivo)
     */
    async _request(endpoint, method = 'POST', payload = null, isMultipart = false) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Authorization': `Bearer ${this.internalApiKey}`
        };
        const options = { method, headers };

        if (payload) {
            if (isMultipart) {
                // Al enviar FormData, el navegador inyecta el Content-Type con el "boundary" adecuado
                options.body = payload;
            } else {
                headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(payload);
            }
        }

        try {
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
        } catch (error) {
            console.error(`[MagicBridge] Falla crítica en ${endpoint}:`, error);
            throw error;
        }
    }

    /**
     * Generación de Tarjeta y Gráficos (Chameleon Render)
     * Devuelve el Buffer (.pkpass o imagen) renderizado paramétricamente
     */
    async issueCard(userId, config) {
        const payload = {
            progress: config.progress || 0,
            tier: config.tier || 'bronce', // bronce, plata, oro
            weather: config.weather || 'unknown', // Inyección del Autopilot
            secretPayload: {
                userId: userId,
                balance: config.balance || 0,
                gamification_mode: config.mode || 'STAMPS' // LOOT_BOX, STREAK, MULTIPASS
            }
        };
        return this._request('/render', 'POST', payload);
    }

    /**
     * Decodificador Offline (Esteganografía)
     * Extrae los datos ocultos en los píxeles de una imagen de tarjeta si se corta el internet en caja
     */
    async decodeOfflineCard(imageFile) {
        const formData = new FormData();
        formData.append('card_image', imageFile);
        return this._request('/decode', 'POST', formData, true);
    }

    /**
     * Generador de Ultrasonido (Zero-Scan)
     * Prepara el token acústico para la transferencia ultrasónica entre dispositivos
     */
    async generateSonicToken(userJwt) {
        return this._request('/sonic', 'POST', { token: userJwt });
    }

    /**
     * Autopilot: Dispara una campaña relámpago basada en inventario o clima
     */
    async triggerFlashDrop(campaignId) {
        return this._request('/autopilot/flashdrop', 'POST', { campaignId: campaignId });
    }
}

// Exponemos el puente globalmente para que el Dashboard pueda usar `window.MagicEngine.issueCard(...)`
if (typeof window !== 'undefined') {
    window.MagicEngine = new MagicEngineBridge();
    console.log("🪄 Fidelio Magic Engine Bridge inicializado y listo para solicitudes.");
}
