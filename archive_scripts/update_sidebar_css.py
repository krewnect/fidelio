import re

with open('index.html', 'r') as f:
    html = f.read()

# Make sidebar cleaner and softer
sidebar_css_patch = """
        /* APP LAYOUT - PREMIUM ENTERPRISE */
        .app-container { display: flex; height: 100vh; overflow: hidden; background-color: var(--bg-main); font-family: var(--font-main); letter-spacing: -0.2px; }
        
        /* SIDEBAR - Clean, borderless feel */
        .app-sidebar { width: 280px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); border-right: 1px solid rgba(0,0,0,0.03); display: flex; flex-direction: column; padding: 32px 24px; z-index: 50; }
        
        .sidebar-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 48px; padding: 0 8px; }
        .sidebar-brand i { font-size: 28px; color: var(--accent-violet); }
        .sidebar-brand span { font-size: 24px; font-weight: 800; color: var(--brand-purple); letter-spacing: -1px; }

        .sidebar-menu { flex: 1; display: flex; flex-direction: column; gap: 6px; overflow-y: auto; }
        .menu-category { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; margin: 24px 0 8px 8px; }
        
        .nav-tab {
            display: flex; align-items: center; gap: 14px; padding: 12px 16px; border-radius: 12px;
            color: var(--text-main); font-size: 14px; font-weight: 600; cursor: pointer; transition: var(--transition);
            border: 1px solid transparent; text-decoration: none;
        }
        .nav-tab i { font-size: 16px; color: #9ca3af; width: 24px; text-align: center; transition: var(--transition); }
        .nav-tab:hover { background: rgba(0,0,0,0.03); }
        .nav-tab.active {
            background: #ffffff; color: var(--accent-violet); box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            border: 1px solid rgba(0,0,0,0.04);
        }
        .nav-tab.active i { color: var(--accent-violet); }

        .menu-badge { margin-left: auto; background: var(--bg-input); color: var(--text-main); font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 8px; }

        .sidebar-footer { padding-top: 24px; margin-top: auto; border-top: 1px solid rgba(0,0,0,0.04); }
        .user-account-card { display: flex; align-items: center; gap: 14px; padding: 12px; border-radius: 12px; transition: var(--transition); cursor: pointer; border: 1px solid transparent; }
        .user-account-card:hover { background: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border-color: rgba(0,0,0,0.04); }
        .user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #1e1b4b, #8b5cf6); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3); }
        .user-info strong { font-size: 14px; font-weight: 700; color: var(--text-main); display: block; letter-spacing: -0.3px; }
        .user-info small { font-size: 12px; color: var(--text-muted); display: block; }
"""
# Replace everything from /* APP LAYOUT */ down to user-account-card end
pattern_sidebar = r'/\*\s*APP LAYOUT\s*\*/.*?\.user-info small \{.*?\}'
html = re.sub(pattern_sidebar, sidebar_css_patch, html, flags=re.DOTALL)

# Update accordion card (glassmorphism dashboard panels)
accordion_patch = """        .accordion-card {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(0,0,0,0.04);
            border-radius: var(--radius-lg); padding: 40px; box-shadow: var(--shadow-md);
            margin-bottom: 32px; transition: var(--transition); position: relative; overflow: hidden;
        }
        .accordion-card::before { content:''; position:absolute; top:0; left:0; width:100%; height:4px; background: linear-gradient(90deg, var(--accent-violet) 0%, transparent 100%); opacity:0; transition: opacity 0.3s; }
        .accordion-card:hover {
            box-shadow: var(--shadow-float);
            transform: translateY(-4px);
        }
        .accordion-card:hover::before { opacity:1; }

        .card-title-bar { display: flex; align-items: center; gap: 16px; margin-bottom: 32px; }
        .card-step-badge { font-size: 13px; font-weight: 800; background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); padding: 6px 14px; border-radius: var(--radius-pill); font-family: var(--font-main); letter-spacing: 0.5px; }
        .card-title-bar h2 { font-size: 22px; font-weight: 700; color: var(--text-main); letter-spacing: -0.5px; }"""

pattern_accordion = r'\.accordion-card \{.*?\.card-title-bar h2 \{.*?\}'
html = re.sub(pattern_accordion, accordion_patch, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
