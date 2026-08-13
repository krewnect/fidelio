import re

with open('dashboard.js', 'r') as f:
    js = f.read()

js = js.replace(
    'console.log("Sucursal guardada en la base de datos.");',
    'console.log("Sucursal guardada en la base de datos."); alert("¡EXITO TOTAL! La base de datos aceptó la sucursal.");'
)

with open('dashboard.js', 'w') as f:
    f.write(js)
