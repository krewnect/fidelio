with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        const response = await fetch('/api/ai/copilot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ merchantContext: mockContext })
        });
        
        if (!response.ok) {
            throw new Error('Error al contactar con la IA');
        }
        
        const data = await response.json();
        const opportunities = data.opportunities || [];"""

replacement = """        // Simular llamada a Gemini (Backend offline)
        await new Promise(resolve => setTimeout(resolve, 2500));
        
        const opportunities = [
            {
                title: "Recuperación de Inactivos",
                description: "Notamos que 480 clientes no han vuelto en 30 días. Envíales un SMS con un incentivo del 15% de descuento válido por 48 horas.",
                type: "retention",
                impact_est: "+$12,500 MXN",
                roi_est: "3.5x"
            },
            {
                title: "Impulso de Días Lentos",
                description: "Tus visitas caen un 40% los martes. Configura una automatización de Puntos Dobles los martes de 4 PM a 7 PM.",
                type: "traffic",
                impact_est: "+35 Visitas",
                roi_est: "5.2x"
            },
            {
                title: "Upsell de Ticket Promedio",
                description: "Tus clientes VIP están gastando por debajo de su histórico. Ofrece una recompensa sorpresa al superar los $500 MXN de compra.",
                type: "upsell",
                impact_est: "+$8,000 MXN",
                roi_est: "4.1x"
            }
        ];"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
