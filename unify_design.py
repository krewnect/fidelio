import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

unified_css = """
<!-- FIDELIO UNIFIED DESIGN SYSTEM (Stripe + Apple + Revolut) -->
<style>
/* 1. Global Reset & Typography */
body {
    background-color: #F7F9FC !important; /* Clean off-white background */
    color: #111827 !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
}

/* 2. Unified Cards (Pure White, Soft Shadow, 24px Radius) */
.tab-content > div[style*="background"], 
.stat-card, 
.content-panel, 
.settings-card,
.apple-section,
.stats-grid > div,
.gemini-insight-panel {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
    backdrop-filter: none !important; /* Remove messy glassmorphism */
    -webkit-backdrop-filter: none !important;
    padding: 32px !important;
    margin-bottom: 24px !important;
    transition: box-shadow 0.2s ease !important;
}

/* Specific fix for grid layouts inside tabs */
.stats-grid {
    gap: 24px !important;
    margin-bottom: 32px !important;
}

/* 3. Unified Buttons (Fidelio Purple #7C3AED) */
button.btn-primary, 
.btn-primary,
button[style*="background: #8b5cf6"],
button[style*="background: linear-gradient"],
.btn-success,
#btn-real-ai {
    background: #7C3AED !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.15) !important;
    transition: all 0.2s ease !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}
button.btn-primary:hover, .btn-primary:hover, #btn-real-ai:hover {
    background: #6D28D9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
}

/* Secondary Buttons */
button.btn-secondary {
    background: #F3F4F6 !important;
    color: #374151 !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
button.btn-secondary:hover {
    background: #E5E7EB !important;
    color: #111827 !important;
}

/* 4. Unified Inputs & Dropdowns */
input[type="text"], input[type="email"], input[type="url"], input[type="number"], input[type="password"], select, textarea, .apple-input, .fidelio-input, .form-control {
    background: #F9FAFB !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    color: #111827 !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease !important;
    width: 100%;
}
input:focus, select:focus, textarea:focus {
    background: #FFFFFF !important;
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    outline: none !important;
}

/* Form Labels */
label, .apple-label {
    display: block !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #4B5563 !important;
    margin-bottom: 8px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* 5. Unified Headers */
.workspace-header {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 0 24px 0 !important;
    margin-bottom: 32px !important;
    border-bottom: 1px solid #E5E7EB !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-end !important;
    border-radius: 0 !important;
}
.workspace-header h1 {
    font-size: 32px !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    color: #111827 !important;
    margin: 4px 0 0 0 !important;
}
.workspace-eyebrow {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #7C3AED !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.workspace-header p {
    color: #6B7280 !important;
    font-size: 16px !important;
    margin: 8px 0 0 0 !important;
    max-width: 600px !important;
}

/* 6. Sidebar Polish */
aside {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
}
.nav-tab {
    border-radius: 10px !important;
    margin: 4px 16px !important;
    padding: 12px 16px !important;
    color: #4B5563 !important;
    font-weight: 500 !important;
}
.nav-tab.active {
    background: #F3F4F6 !important;
    color: #111827 !important;
    font-weight: 600 !important;
}
.nav-tab:hover:not(.active) {
    background: #F9FAFB !important;
}
.nav-tab.active i {
    color: #7C3AED !important;
}

/* Cleanup bad gradients and fake glass */
.iphone-pro-mockup {
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important; /* Cleaner Apple shadow */
    transform: scale(0.65) !important; /* Remove the skewed 3D, keep it flat and elegant */
}
</style>
"""

if "FIDELIO UNIFIED DESIGN SYSTEM" not in html:
    # Inject right before </head>
    html = html.replace('</head>', unified_css + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

