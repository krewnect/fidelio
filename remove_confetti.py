import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Pattern 1: DO WOW CONFETTI block
pattern1 = r'// DO WOW CONFETTI\s+if\(typeof confetti === \'function\'\).*?document\.head\.appendChild\(script\);\s+\}'
js = re.sub(pattern1, '', js, flags=re.DOTALL)

# Pattern 2: jsConfetti block
pattern2 = r'try \{\s+if \(typeof jsConfetti !== \'undefined\'\) \{\s+jsConfetti\.addConfetti[^}]+\}\s+\} catch\(e\) \{\}'
js = re.sub(pattern2, '', js, flags=re.DOTALL)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
