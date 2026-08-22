with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure tab-loyalty is always displayed when requested
js = js.replace("""        const loy = document.getElementById('tab-loyalty');
        if(loy) {
            loy.classList.add('active');
            loy.style.display = 'block'; // Force visibility
            console.log("Set tab-loyalty to active and block");
        }""",
        """        const loy = document.getElementById('tab-loyalty');
        if(loy) {
            loy.classList.add('active');
            loy.style.display = 'block'; // Force visibility
            loy.style.visibility = 'visible';
            loy.style.opacity = '1';
            loy.style.height = 'auto';
            console.log("Set tab-loyalty to active, block, visible, opacity 1");
        }""")

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched display visibility for tab-loyalty.")
