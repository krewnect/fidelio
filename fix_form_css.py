import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update CSS for inputs and button to be ultra-premium
new_css = """        .form-group {
            text-align: left;
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 13px;
            font-weight: 700;
            color: #4b5563;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .input-field, select {
            width: 100%;
            padding: 16px 20px;
            border-radius: 16px;
            border: 2px solid transparent;
            font-size: 15px;
            font-weight: 500;
            font-family: inherit;
            box-sizing: border-box;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background-color: #f3f4f6;
            color: #111827;
        }
        .input-field::placeholder {
            color: #9ca3af;
            font-weight: 400;
        }
        .input-field:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .btn-download {
            width: 100%;
            padding: 18px;
            border-radius: 16px;
            border: none;
            background: var(--primary);
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-top: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 10px 25px -5px var(--primary);
        }
        .btn-download:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px -5px var(--primary);
            filter: brightness(1.1);
        }"""

text = re.sub(r'\.form-group\s*\{[\s\S]*?\.btn-download:hover\s*\{[\s\S]*?\}', new_css, text)

# Fix the color logic in JavaScript to inherit from campaign if only one
target_js = """                // 5. Apply Visual Branding
                const prefs = merch.appointment_settings?.landing_prefs || {};
                
                if (prefs.portal_color || merch.color_primary) {
                    const color = prefs.portal_color || merch.color_primary;
                    document.documentElement.style.setProperty('--primary', color);
                }"""

replacement_js = """                // 5. Apply Visual Branding
                const prefs = merch.appointment_settings?.landing_prefs || {};
                
                let themeColor = prefs.portal_color || merch.color_primary || '#000000';
                // If there's only one campaign (like Professional), inherit its card color automatically
                if (visibleCampaigns.length === 1 && visibleCampaigns[0].color_primary) {
                    themeColor = visibleCampaigns[0].color_primary;
                }
                
                document.documentElement.style.setProperty('--primary', themeColor);
                """

text = text.replace(target_js, replacement_js)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
