import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/' + username)}`;"""
replacement = """const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/' + username + '?v=3')}`;"""

text = text.replace(target, replacement)

target2 = """const landingLink = `fideliorewards.com/${slug}`;"""
replacement2 = """const landingLink = `fideliorewards.com/${slug}?v=3`;"""

text = text.replace(target2, replacement2)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
