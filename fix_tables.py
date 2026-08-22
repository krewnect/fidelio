import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the campaigns table beautiful
html = html.replace('<table style="width: 100%; border-collapse: collapse; text-align: left;">', '<div class="fidelio-table-container"><table class="fidelio-table">')
html = html.replace('</table>\n                        </div>\n                    </div>\n                </div>', '</table></div>\n                        </div>\n                    </div>\n                </div>')

# Fix CRM table too if it has inline styles
html = html.replace('<table style="width:100%; border-collapse:collapse; text-align:left;">', '<div class="fidelio-table-container"><table class="fidelio-table">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
