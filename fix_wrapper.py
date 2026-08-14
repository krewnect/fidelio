import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Give the standard panels a wrapper ID
html = html.replace(
    '<div style="display:flex; gap: 24px; flex-wrap: wrap; margin-bottom: 24px;">\n                    <!-- CASHBACK SETTINGS -->',
    '<div id="panel-loyalty-standard">\n                <div style="display:flex; gap: 24px; flex-wrap: wrap; margin-bottom: 24px;">\n                    <!-- CASHBACK SETTINGS -->'
)

# And close the wrapper after VIP Tiers
html = html.replace(
    '                        </table>\n                    </div>\n                </div>\n            </section>',
    '                        </table>\n                    </div>\n                </div>\n                </div>\n            </section>'
)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated HTML wrapper.")
