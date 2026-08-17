import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will replace the block where I declared `const stampsGrid` in my injection.
# Actually, I can just find the second `const stampsGrid = document.getElementById('render-stamps-grid');` and change it to `stampsGrid = document.getElementById('render-stamps-grid');`. Or I can rename my injected one to `const stampsGrid_injected`.

js = js.replace(
    '''            // Force redraw of stamps just in case
            const stampsGrid = document.getElementById('render-stamps-grid');''',
    '''            // Force redraw of stamps just in case
            let stampsGrid_injected = document.getElementById('render-stamps-grid');'''
)

js = js.replace(
    '''            if (stampsGrid && !stampsGrid.innerHTML) {
                 stampsGrid.innerHTML = '';
                 for(let i=1; i<=10; i++) {
                     stampsGrid.innerHTML += `<div class="stamp-coin ${i<=3?'filled':'empty'}" style="background-color:${i<=3?cAcc:''};">${i>3?i:''}</div>`;
                 }
            }''',
    '''            if (stampsGrid_injected && !stampsGrid_injected.innerHTML) {
                 stampsGrid_injected.innerHTML = '';
                 for(let i=1; i<=10; i++) {
                     stampsGrid_injected.innerHTML += `<div class="stamp-coin ${i<=3?'filled':'empty'}" style="background-color:${i<=3?cAcc:''};">${i>3?i:''}</div>`;
                 }
            }'''
)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Syntax error fixed.")
