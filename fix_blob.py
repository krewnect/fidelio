import re

with open('pass.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                const blob = await response.blob();
                const objUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = objUrl;
                a.download = 'fidelio.pkpass';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(objUrl);"""

replacement = """                // En iOS Safari, descargar un Blob de .pkpass vía AJAX falla silenciosamente o da error "no puede descargar este archivo".
                // Por lo tanto, si la respuesta HTTP fue OK (los certificados existen), hacemos una redirección directa 
                // para que el sistema operativo intercepte el archivo y abra la app nativa de Apple Wallet.
                window.location.href = url;"""

text = text.replace(target, replacement)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(text)
