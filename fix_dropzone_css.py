import re

with open('index.html', 'r') as f:
    html = f.read()

dropzone_css = """
        /* FILE DROPZONE */
        .file-dropzone { border: 2px dashed #d1d5db; border-radius: 12px; padding: 24px; text-align: center; cursor: pointer; transition: var(--transition); position: relative; background: var(--bg-input); }
        .file-dropzone:hover { border-color: var(--accent-violet); background: rgba(139, 92, 246, 0.05); }
        .file-dropzone input[type="file"] { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        .file-dropzone i { font-size: 28px; color: #9ca3af; margin-bottom: 12px; display: block; transition: var(--transition); }
        .file-dropzone:hover i { color: var(--accent-violet); transform: scale(1.1); }
        .file-dropzone span { display: block; font-size: 13px; color: #6b7280; font-weight: 500; }
        
        /* FORM ELEMENTS - Premium */"""

html = html.replace('/* FORM ELEMENTS - Premium */', dropzone_css)

with open('index.html', 'w') as f:
    f.write(html)
