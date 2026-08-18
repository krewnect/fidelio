import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Logo Container CSS
target_css = """        .logo-container {
            width: 120px;
            height: 120px;
            margin: 0 auto 20px auto;
            border-radius: 24px;
            background: var(--bg-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: var(--primary);
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }"""

replacement_css = """        .logo-container {
            width: 180px;
            height: auto;
            max-height: 140px;
            margin: 0 auto 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            box-shadow: none !important;
            border-radius: 0;
            overflow: visible;
        }"""

text = text.replace(target_css, replacement_css)

# Remove the JS dynamic styling of the logo container that forces box-shadow and background
text = re.sub(r"document\.getElementById\('logo-container'\)\.style\.boxShadow = `[^`]+`;", '', text)
text = re.sub(r"document\.getElementById\('logo-container'\)\.style\.background = '#ffffff';", '', text)
text = re.sub(r"document\.getElementById\('logo-container'\)\.style\.background = 'transparent';", '', text)

# Fix the Professional check
target_js = """                if (merch.business_type === 'professional') {"""
replacement_js = """                if (merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'))) {"""

text = text.replace(target_js, replacement_js)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
