import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix double class attributes: e.g., class="content-panel" id="section-profile" class="premium-card"
# We want to merge them into class="content-panel premium-card" id="section-profile"
def merge_classes(match):
    tag_content = match.group(1)
    
    # Find all class="..."
    classes = re.findall(r'class="([^"]*)"', tag_content)
    if len(classes) <= 1:
        return '<' + tag_content + '>'
    
    # Merge classes
    merged_classes = set()
    for c in classes:
        merged_classes.update(c.split())
    merged_class_str = ' '.join(merged_classes)
    
    # Remove all existing class attributes
    tag_content = re.sub(r'\s*class="[^"]*"', '', tag_content)
    
    # Add the unified class attribute
    return '<' + tag_content + ' class="' + merged_class_str + '">'

html = re.sub(r'<([^>]+class="[^"]*"[^>]+class="[^"]*"[^>]*)>', merge_classes, html)

# Fix double style attributes
def merge_styles(match):
    tag_content = match.group(1)
    
    # Find all style="..."
    styles = re.findall(r'style="([^"]*)"', tag_content)
    if len(styles) <= 1:
        return '<' + tag_content + '>'
    
    # Merge styles
    merged_styles = []
    for s in styles:
        s = s.strip()
        if s and not s.endswith(';'):
            s += ';'
        merged_styles.append(s)
    
    merged_style_str = ' '.join(merged_styles)
    
    # Remove all existing style attributes
    tag_content = re.sub(r'\s*style="[^"]*"', '', tag_content)
    
    # Add the unified style attribute
    return '<' + tag_content + ' style="' + merged_style_str + '">'

html = re.sub(r'<([^>]+style="[^"]*"[^>]+style="[^"]*"[^>]*)>', merge_styles, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML syntax errors (double classes/styles) fixed.")
