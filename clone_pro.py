import os

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<title>Fidelio - Apple Wallet para Restaurantes</title>', '<title>Fidelio for Professionals - Apple Wallet & Citas</title>')
content = content.replace('El motor de lealtad de las grandes franquicias', 'El motor de lealtad y citas para profesionales')
content = content.replace('Fideliza a tus clientes con tarjetas en Apple Wallet', 'Agenda citas y fideliza a tus pacientes con tarjetas en Apple Wallet')
content = content.replace('Diseñado exclusivamente para restaurantes y cafeterías', 'Diseñado para doctores, psicólogos, clínicas y profesionales independientes')
content = content.replace('Únete a las cafeterías y restaurantes', 'Únete a los profesionales de la salud y servicios')
content = content.replace('Añade tus ubicaciones', 'Gestiona tu agenda')
content = content.replace('Agrega tus locales y envía notificaciones push', 'Lleva un control de tus citas médicas y envía recordatorios')
content = content.replace('¿Tienes más de 1 sucursal?', '¿Necesitas agendar citas?')
content = content.replace('Sucursales adicionales', 'Sistema de Citas (Incluido)')

# Set the default select to professional
content = content.replace('<option value="professional">💼 Profesional Independiente (Con Sistema de Citas)</option>', '<option value="professional" selected>💼 Profesional Independiente (Con Sistema de Citas)</option>')

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/professionals.html', 'w', encoding='utf-8') as f:
    f.write(content)
