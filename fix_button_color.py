import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_css = r'\.apple-btn-primary \{.*?background: #111827;.*?\}'
replacement_css = """.apple-btn-primary {
                        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
                        color: white;
                        border: none;
                        border-radius: 14px;
                        padding: 18px;
                        font-size: 16px;
                        font-weight: 700;
                        width: 100%;
                        cursor: pointer;
                        transition: all 0.2s;
                        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 10px;
                    }"""
html = re.sub(target_css, replacement_css, html, flags=re.DOTALL)

target_hover = r'\.apple-btn-primary:hover \{.*?background: #1f2937;.*?\}'
replacement_hover = """.apple-btn-primary:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
                        background: linear-gradient(135deg, #7c3aed, #6d28d9);
                    }"""
html = re.sub(target_hover, replacement_hover, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
