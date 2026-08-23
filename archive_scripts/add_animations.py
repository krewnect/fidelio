with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

animations = """
/* PREMIUM ANIMATIONS FOR SETTINGS */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes floatGlow {
    0% { box-shadow: 0 8px 16px rgba(139, 92, 246, 0.2); transform: translateY(0px); }
    50% { box-shadow: 0 16px 24px rgba(139, 92, 246, 0.4); transform: translateY(-4px); }
    100% { box-shadow: 0 8px 16px rgba(139, 92, 246, 0.2); transform: translateY(0px); }
}

.premium-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.6s ease-out backwards;
}

.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.06) !important;
}

.animated-avatar {
    animation: floatGlow 4s ease-in-out infinite;
}

.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }

.hover-glow:hover {
    filter: brightness(1.1);
    transform: scale(1.02);
}
"""
css += "\n" + animations

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Apply classes to the account elements
html = html.replace('<div class="premium-card"', '<div class="premium-card stagger-1"')
html = html.replace('id="section-profile" class="premium-card stagger-1"', 'id="section-profile" class="premium-card stagger-2"')
html = html.replace('id="section-portal" class="premium-card stagger-1"', 'id="section-portal" class="premium-card stagger-3"')
html = html.replace('id="section-security" class="premium-card stagger-1"', 'id="section-security" class="premium-card stagger-4"')

html = html.replace('class="btn btn-primary"', 'class="btn btn-primary hover-glow"')

# Apply animated avatar class
html = html.replace('class="premium-card stagger-1"', 'class="premium-card stagger-1" style="background: var(--surface); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid var(--border-soft); text-align: center;"')
html = html.replace('<div style="position:relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px; background: linear-gradient(135deg, var(--accent-violet), #c084fc); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; color: white; box-shadow: 0 8px 16px rgba(139, 92, 246, 0.2);">', '<div class="animated-avatar" style="position:relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px; background: linear-gradient(135deg, var(--accent-violet), #c084fc); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; color: white; transition: all 0.3s ease;">')

# Cache bust styles
html = re.sub(r'href="styles\.css\?v=\d+"', 'href="styles.css?v=' + str(__import__('time').time()) + '"', html)
# Cache bust js again just in case
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

