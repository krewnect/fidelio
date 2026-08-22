import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Modify applyQuickTemplate to populate the icon dropdown dynamically and set custom banners
target = "const uniReward = document.getElementById('unified-reward');"

replacement = """
        // DYNAMIC ICON DROPDOWN POPULATION
        const iconSelect = document.getElementById('rest-icon');
        if (iconSelect) {
            if (type === 'medico') {
                iconSelect.innerHTML = `
                    <option value="fa-heart-pulse">Corazón Médico</option>
                    <option value="fa-stethoscope">Estetoscopio</option>
                    <option value="fa-tooth">Diente (Dentista)</option>
                    <option value="fa-user-doctor">Doctor</option>
                    <option value="fa-eye">Ojo (Oftalmólogo)</option>
                    <option value="fa-bone">Hueso (Traumatólogo)</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&q=80"; // Clean Medical Abstract
            } else if (type === 'belleza') {
                iconSelect.innerHTML = `
                    <option value="fa-scissors">Tijeras de Estilista</option>
                    <option value="fa-spa">Flor de Spa</option>
                    <option value="fa-spray-can">Spray de Cabello</option>
                    <option value="fa-gem">Diamante</option>
                    <option value="fa-eye">Pestañas / Belleza</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&q=80"; // Elegant Salon Abstract
            } else if (type === 'clases') {
                iconSelect.innerHTML = `
                    <option value="fa-dumbbell">Pesa / Gimnasio</option>
                    <option value="fa-person-running">Corredor</option>
                    <option value="fa-fire">Llama de Energía</option>
                    <option value="fa-paw">Huella (Paseador)</option>
                    <option value="fa-medal">Medalla</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&q=80"; // Dark Gym Abstract
            } else {
                iconSelect.innerHTML = `
                    <option value="fa-star">Estrella (General)</option>
                    <option value="fa-crown">Corona VIP</option>
                    <option value="fa-gift">Regalo</option>
                    <option value="fa-gem">Diamante</option>
                `;
                state.customBannerUrl = null; // Default
            }
            iconSelect.value = state.iconClass; // Set the default we picked earlier
        }

        const uniReward = document.getElementById('unified-reward');"""

js = js.replace(target, replacement)

# We need to make sure the mockup actually renders the customBannerUrl!
# Currently updatePassRender might not use state.customBannerUrl for the builder preview!
# Let's check updatePassRender
with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
