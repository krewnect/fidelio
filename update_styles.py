import re

file_path = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Broad background and text color replacements for dark mode classes
    content = re.sub(r'\bbg-slate-900\b', 'bg-white', content)
    content = re.sub(r'\bbg-slate-800\b', 'bg-slate-50', content)
    content = re.sub(r'\bbg-slate-950\b', 'bg-white', content)
    content = re.sub(r'\bbg-black\b', 'bg-white', content)
    content = re.sub(r'\bbg-[#0f172a]\b', 'bg-white', content)
    
    # We need to be careful with text-white because of buttons. 
    # Let's temporarily change text-white inside buttons to something safe, then change other text-white, then revert.
    content = re.sub(r'class="([^"]*?bg-[^" ]+-600[^"]*?)text-white([^"]*?)"', r'class="\1TEXT_WHITE_SAFE\2"', content)
    content = re.sub(r'class="([^"]*?bg-fidelio-[0-9]+[^"]*?)text-white([^"]*?)"', r'class="\1TEXT_WHITE_SAFE\2"', content)
    
    content = re.sub(r'\btext-slate-200\b', 'text-slate-700', content)
    content = re.sub(r'\btext-slate-300\b', 'text-slate-600', content)
    content = re.sub(r'\btext-slate-400\b', 'text-slate-500', content)
    content = re.sub(r'\btext-white\b', 'text-slate-900', content)
    
    content = re.sub(r'\bTEXT_WHITE_SAFE\b', 'text-white', content)

    # Step 2: Borders and subtle background replacements
    content = re.sub(r'\bborder-slate-700\b', 'border-slate-200', content)
    content = re.sub(r'\bborder-slate-800\b', 'border-slate-200', content)
    content = re.sub(r'\bborder-white/10\b', 'border-slate-200', content)
    content = re.sub(r'\bborder-white/20\b', 'border-slate-200', content)
    content = re.sub(r'\bbg-white/5\b', 'bg-slate-50', content)
    content = re.sub(r'\bbg-white/10\b', 'bg-slate-100', content)

    # Convert generic cards with borders to crisp cards
    def card_replacer(match):
        classes = match.group(1).split()
        if 'bg-white' not in classes: classes.append('bg-white')
        if 'border' not in classes: classes.append('border')
        if 'border-slate-200' not in classes: classes.append('border-slate-200')
        if 'shadow-sm' not in classes: classes.append('shadow-sm')
        # preserve all existing classes including rounded forms
        return 'class="' + ' '.join(classes) + '"'

    # Try to find class attributes that likely represent cards (e.g. have padding and rounded corners)
    # Be careful not to mess up other classes.
    content = re.sub(r'class="([^"]*?(?:p-4|p-6|p-8)[^"]*?rounded-[^"]*?)"', card_replacer, content)

    # Remove duplicated classes
    def remove_dups(match):
        classes = match.group(1).split()
        seen = set()
        out = []
        for c in classes:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return 'class="' + ' '.join(out) + '"'
        
    content = re.sub(r'class="([^"]+)"', remove_dups, content)
    
    # Fix the generic body or main wrapper background if it exists
    content = re.sub(r'<body class="([^"]*?)"', r'<body class="bg-slate-50 text-slate-900 font-sans antialiased"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Update complete")
except Exception as e:
    print("Error:", e)
