import re

file_path = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Consolidate accents to 600 for light mode
    content = re.sub(r'\btext-fidelio-[45]00\b', 'text-fidelio-600', content)
    content = re.sub(r'\btext-blue-[45]00\b', 'text-fidelio-600', content)
    content = re.sub(r'\btext-purple-[45]00\b', 'text-fidelio-600', content)
    content = re.sub(r'\btext-violet-[45]00\b', 'text-fidelio-600', content)

    # Bump semantic colors to 600 for contrast
    content = re.sub(r'\btext-emerald-[45]00\b', 'text-emerald-600', content)
    content = re.sub(r'\btext-rose-[45]00\b', 'text-rose-600', content)
    content = re.sub(r'\btext-amber-[45]00\b', 'text-amber-600', content)
    content = re.sub(r'\btext-orange-[45]00\b', 'text-orange-600', content)
    content = re.sub(r'\btext-yellow-[45]00\b', 'text-amber-600', content)
    
    # Similarly for backgrounds if any were 400/500
    content = re.sub(r'\bbg-fidelio-[45]00\b', 'bg-fidelio-600', content)
    content = re.sub(r'\bbg-blue-[45]00\b', 'bg-fidelio-600', content)
    content = re.sub(r'\bbg-purple-[45]00\b', 'bg-fidelio-600', content)
    content = re.sub(r'\bbg-violet-[45]00\b', 'bg-fidelio-600', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Accents updated")
except Exception as e:
    print("Error:", e)
