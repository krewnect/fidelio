import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Revert to elegant, light, clean Apple-like aesthetic
old_builder_card_css = """                    .builder-card {
                        background: linear-gradient(145deg, #1f1140 0%, #3a1c71 100%);
                        border-radius: 24px;
                        padding: 32px;
                        box-shadow: 0 20px 50px rgba(0,0,0,0.2), inset 0 0 0 1px rgba(255,255,255,0.1);
                        color: #ffffff;
                        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s;
                    }
                    .builder-card:hover {
                        transform: translateY(-4px);
                        box-shadow: 0 30px 60px rgba(0,0,0,0.3), inset 0 0 0 1px rgba(139, 92, 246, 0.4);
                    }
                    
                    /* Override text colors inside the new dark cards */
                    .builder-card h2, .builder-card h3 { color: #ffffff !important; }
                    .builder-card .premium-label { color: rgba(255,255,255,0.7) !important; }
                    .builder-card p { color: rgba(255,255,255,0.6) !important; }
                    
                    /* Make inputs glassmorphic */
                    .builder-card .premium-input, .builder-card .premium-textarea {
                        background: rgba(0,0,0,0.2) !important;
                        border: 1px solid rgba(255,255,255,0.1) !important;
                        color: #ffffff !important;
                    }
                    .builder-card .premium-input:focus {
                        border-color: #8b5cf6 !important;
                        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3) !important;
                    }
                    
                    /* Drag area glassmorphic */
                    .builder-card .drag-area {
                        background: rgba(255,255,255,0.05) !important;
                        border: 2px dashed rgba(255,255,255,0.2) !important;
                    }
                    .builder-card .drag-area .icon { color: rgba(255,255,255,0.5) !important; }
                    .builder-card .drag-area header { color: #ffffff !important; }
                    
                    /* Fix the background of the whole builder scroll area so it matches */
                    #builder-scroll-area {
                        background: #0f0a1f !important; /* Deep space dark */
                    }
                    
                    /* Make the step numbers pop */
                    .builder-card h3 i, .builder-card h2 i {
                        color: #a78bfa !important;
                        text-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
                    }"""

new_builder_card_css = """                    .builder-card {
                        background: rgba(255, 255, 255, 0.95);
                        backdrop-filter: blur(20px);
                        border-radius: 24px;
                        padding: 32px;
                        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
                        border: 1px solid rgba(255,255,255,0.8);
                        color: #111827;
                        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s;
                    }
                    .builder-card:hover {
                        transform: translateY(-4px);
                        box-shadow: 0 20px 50px -10px rgba(0,0,0,0.12);
                    }
                    #builder-scroll-area {
                        background: #f9fafb !important; /* Soft light gray background */
                    }"""

html = html.replace(old_builder_card_css, new_builder_card_css)

# Remove the inline dark-mode override if present on premium inputs from the CSS override
html = re.sub(r'style="[^"]*background:\s*rgba\(0,0,0,0\.2\)[^"]*"', '', html)

# 2. Make sure ALL sections are wrapped in builder cards so it doesn't look like a "government page"
target_unwrapped = """                        <!-- 2.5 Citas y Pagos (Professional Only) -->
                        <div class="plan-professional-only">"""
replacement_wrapped = """                        <!-- 2.5 Citas y Pagos (Professional Only) -->
                        <div class="builder-card plan-professional-only" style="margin-bottom:24px;">"""
html = html.replace(target_unwrapped, replacement_wrapped)

target_unwrapped_2 = """                        <!-- 4. Beneficios Visibles -->
                        <div id="section-visible-benefits">"""
replacement_wrapped_2 = """                        <!-- 4. Beneficios Visibles -->
                        <div id="section-visible-benefits" class="builder-card" style="margin-bottom:24px;">"""
html = html.replace(target_unwrapped_2, replacement_wrapped_2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
