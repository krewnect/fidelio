with open('/Users/robertoordonez/.gemini/antigravity/brain/98972967-1d06-4691-82e8-55cb66259961/fidelio_studio_spec.md', 'r', encoding='utf-8') as f:
    spec = f.read()

new_section = """
**Variables Visuales y Descriptivas Base:**
*   `rest-name` (Input Text): Nombre del Negocio (Ej. "Cafetería La Selva").
*   `business-category-input` (Input Text) / `business-category-select`: Tipo o Categoría del Negocio (Ej. "Restaurante", "Gimnasio").
*   `rest-desc` (Input Text): Descripción Dinámica / Lema (Ej. "Tu membresía exclusiva").
*   `rest-terms` (Textarea): Términos Legales de las recompensas impresos en el reverso de la tarjeta.
*   `portal-logo-upload` (File Input): Carga de imagen del Logotipo de la marca (procesado como Base64).
*   `program-type-select` / `magic-shape-select`: Tipo de diseño base Apple Wallet:
    *   `storeCard` (Tarjeta de Lealtad Clásica)
    *   `coupon` (Cupón Descuento)
    *   `eventTicket` (Boleto de Evento / Muescas Laterales)
    *   `boardingPass` (Pase de Abordaje / Vertical)
*   `color-primary` (Input Color): Código Hexadecimal para el fondo.
*   `color-accent` (Input Color): Código Hexadecimal para textos y etiquetas.
"""

spec = spec.replace("**Variables Visuales Base:**\n*   `program-type-select`: Tipo de diseño base Apple Wallet (`storeCard`, `coupon`, `eventTicket`, `boardingPass`). En la interfaz se llama \"Formato de Tarjeta\" (Muescas Laterales, Pase Clásico, etc).\n*   `color-primary` (Fondo) y `color-accent` (Fuentes/Botones).\n*   Logotipo de la Marca (Inyección directa al Payload).", new_section.strip())

with open('/Users/robertoordonez/.gemini/antigravity/brain/98972967-1d06-4691-82e8-55cb66259961/fidelio_studio_spec.md', 'w', encoding='utf-8') as f:
    f.write(spec)
print("Updated spec.")
