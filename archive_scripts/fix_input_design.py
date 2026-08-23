import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the inputs look much more premium, not "asqueroso gray rectangles"
new_css = """
                    .apple-input {
                        width: 100%;
                        padding: 16px 20px;
                        background: #ffffff !important;
                        border: 2px solid #e2e8f0 !important;
                        border-radius: 16px !important;
                        font-size: 15px;
                        color: #0f172a;
                        font-weight: 500;
                        outline: none;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
                        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                    }
                    .apple-input:hover {
                        border-color: #cbd5e1 !important;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
                        transform: translateY(-1px);
                    }
                    .apple-input:focus {
                        transform: scale(1.02);
                        border-color: #8b5cf6 !important;
                        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2) !important;
                        background: #ffffff !important;
                    }
                    .apple-label {
                        display: block;
                        font-size: 12px;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        color: #64748b;
                        font-weight: 800;
                        margin-bottom: 8px;
                        margin-left: 4px;
                    }
"""

# Replace the old apple-input CSS
target = r'\.apple-input \{[^}]+\}\s*\.apple-input:focus \{[^}]+\}\s*\.apple-label \{[^}]+\}'
html = re.sub(target, new_css, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
