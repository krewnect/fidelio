with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_hide = """            // 2. Hide all tabs forcefully
            document.querySelectorAll('.tab-content').forEach(t => {
                t.classList.remove('active');
                t.style.display = '';
            });"""

new_hide = """            // 2. Hide all tabs forcefully
            document.querySelectorAll('.tab-content').forEach(t => {
                t.classList.remove('active');
                t.style.display = 'none';
            });"""

html = html.replace(old_hide, new_hide)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed display issue.")
