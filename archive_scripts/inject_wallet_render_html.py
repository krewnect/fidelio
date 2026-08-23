import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_header_stats = """                                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                                    <div>
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Nivel Actual</div>
                                                        <div id="render-vip-caption" style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;">ORO VIP</div>
                                                    </div>
                                                    <div style="text-align:right;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Cashback</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-balance">$145.00</div>
                                                    </div>
                                                </div>"""

new_header_stats = """                                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                                    <div>
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Nivel Actual</div>
                                                        <div id="render-vip-caption" style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;">ORO VIP</div>
                                                    </div>
                                                    <div id="render-wallet-block" style="display:none; text-align:center;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Monedero</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-wallet-balance">$600.00</div>
                                                    </div>
                                                    <div id="render-cashback-block" style="text-align:right;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Cashback</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-balance">$145.00</div>
                                                    </div>
                                                </div>"""
html = html.replace(old_header_stats, new_header_stats)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Injected Wallet render block into HTML.")
