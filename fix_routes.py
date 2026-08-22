import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make it listen on BOTH routes to be absolutely safe
target = """app.post('/api/appointments/request', apiLimiter, async (req, res) => {"""
replacement = """app.post(['/api/appointments', '/api/appointments/request'], apiLimiter, async (req, res) => {"""

if target in js:
    js = js.replace(target, replacement)
else:
    print("WARNING: target not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
