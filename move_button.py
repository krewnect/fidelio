with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change top:20px; left:20px to bottom:30px; left:30px; and make it look a bit more modern
old_btn = "style=\"position:absolute; top:20px; left:20px; z-index:9999999; background:rgba(255,255,255,0.1); color:#fff; border:none; padding:10px 15px; border-radius:8px; cursor:pointer; font-family:var(--font-main); backdrop-filter:blur(10px);\""
new_btn = "style=\"position:absolute; bottom:30px; left:30px; z-index:9999999; background:rgba(0,0,0,0.8); color:#fff; border:1px solid rgba(255,255,255,0.2); padding:12px 20px; border-radius:12px; cursor:pointer; font-family:var(--font-main); backdrop-filter:blur(10px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); font-weight:600; font-size:14px; transition: transform 0.2s;\" onmouseover=\"this.style.transform='scale(1.05)'\" onmouseout=\"this.style.transform='scale(1)'\""

html = html.replace(old_btn, new_btn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Button moved to bottom left.")
