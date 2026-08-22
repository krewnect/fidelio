with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-loyalty"')
if idx != -1:
    before = html[:idx]
    div_opens = before.count('<div')
    div_closes = before.count('</div')
    print(f"Divs open before tab-loyalty: {div_opens - div_closes}")
