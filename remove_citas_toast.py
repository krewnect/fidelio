import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the toast notification from saveComplexSchedule
js = js.replace(
    '''if(typeof showToast === 'function') {
            showToast("Franjas horarias guardadas exitosamente", "success");
        } else {
            alert("Franjas horarias guardadas exitosamente");
        }''',
    '''// Notificación silenciosa (se quitó el toast a petición del usuario)'''
)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Toast removed.")
