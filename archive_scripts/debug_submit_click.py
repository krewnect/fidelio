import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_click = """        if (btn) {
            e.preventDefault();
            console.log("Btn submit branch clicked!");
            
            const dynName = document.getElementById('branch-name');"""

new_click = """        if (btn) {
            e.preventDefault();
            console.log("Btn submit branch clicked!");
            try {
            const dynName = document.getElementById('branch-name');"""

old_end = """            if (addModal) addModal.style.display = 'none';
            renderBranches();
            if (window.saveDesignToSupabase) window.saveDesignToSupabase();
            showToast(`Sucursal "${newBranch.name}" agregada con éxito a la lista local. Recuerda darle a Guardar y Actualizar Tarjetas al final.`, "success");
        }"""

new_end = """            if (addModal) addModal.style.display = 'none';
            renderBranches();
            if (window.saveDesignToSupabase) window.saveDesignToSupabase();
            showToast(`Sucursal "${newBranch.name}" agregada con éxito a la lista local. Recuerda darle a Guardar y Actualizar Tarjetas al final.`, "success");
            } catch (err) {
                alert("CRASH LOG Submit: " + err.message + "\\n" + err.stack);
            }
        }"""

js = js.replace(old_click, new_click)
js = js.replace(old_end, new_end)

with open('dashboard.js', 'w') as f:
    f.write(js)
