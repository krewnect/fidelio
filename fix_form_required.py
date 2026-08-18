import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """<select id="campaign-select" class="input-field" required>"""
replacement = """<select id="campaign-select" class="input-field">"""

text = text.replace(target, replacement)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
