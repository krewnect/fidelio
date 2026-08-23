import re

with open('index.html', 'r') as f:
    html = f.read()

# Forms and buttons patch
forms_patch = """        /* FORM ELEMENTS - Premium */
        .form-group { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
        .form-group label { font-size: 13px; font-weight: 600; color: #374151; letter-spacing: -0.2px; }
        input[type="text"], input[type="number"], input[type="date"], select, textarea {
            background: var(--bg-input); border: 1px solid #e5e7eb; border-radius: 12px;
            padding: 14px 18px; color: var(--text-main); font-family: var(--font-main); font-size: 15px; 
            transition: var(--transition); width: 100%; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
            box-sizing: border-box;
        }
        input:focus, select:focus, textarea:focus { outline: none; border-color: var(--accent-violet); background: #ffffff; box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15); }

        .form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1.5fr; gap: 20px; }

        /* BUTTONS */
        .btn {
            display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px;
            border-radius: 12px; font-family: var(--font-main); font-size: 15px; font-weight: 700;
            cursor: pointer; transition: var(--transition); border: none; letter-spacing: -0.3px;
        }
        .btn-primary { background: var(--text-main); color: white; box-shadow: 0 4px 14px rgba(0,0,0,0.1); }
        .btn-primary:hover { background: #000000; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
        .btn-primary:active { transform: translateY(0); }
        
        .btn-secondary { background: white; color: var(--text-main); border: 1px solid #d1d5db; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        .btn-secondary:hover { border-color: var(--text-main); background: #f9fafb; transform: translateY(-1px); }

        .btn-outline { background: transparent; color: var(--accent-violet); border: 1px solid var(--accent-violet); }
        .btn-outline:hover { background: rgba(139, 92, 246, 0.05); }"""

pattern_forms = r'/\*\s*FORM ELEMENTS\s*\*/.*?\.btn-outline:hover \{.*?\}'
html = re.sub(pattern_forms, forms_patch, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
