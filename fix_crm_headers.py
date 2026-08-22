import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                                <tr>
                                    <th>Cliente</th>
                                    <th>Contacto</th>
                                    <th>Cumpleaños / Registro</th>
                                    <th>Nivel VIP</th>
                                    <th>Puntos / Visitas</th>
                                    <th>Gasto Total</th>
                                    <th>Frecuencia</th>
                                    <th>Estado</th>
                                    <th>Acciones</th>
                                </tr>"""

replacement = """                                <tr>
                                    <th>Cliente</th>
                                    <th>Contacto</th>
                                    <th>Nivel VIP</th>
                                    <th>Saldo (Monedero)</th>
                                    <th>Puntos / Visitas</th>
                                    <th>Última Visita</th>
                                    <th>Frecuencia</th>
                                    <th>Gasto Total</th>
                                    <th>Gasto Promedio</th>
                                    <th>Acciones</th>
                                </tr>"""

html = html.replace(target, replacement)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
