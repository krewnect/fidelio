import re

with open('dashboard.js', 'r') as f:
    content = f.read()

# Replace exact match with lenient match
content = content.replace("currentEmail.trim().toLowerCase() === 'hola@fideliorewards.com'", 
                          "(currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio'))")

content = content.replace("currentEmail.trim().toLowerCase() !== 'hola@fideliorewards.com'", 
                          "!(currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio'))")

with open('dashboard.js', 'w') as f:
    f.write(content)

print("Done")
