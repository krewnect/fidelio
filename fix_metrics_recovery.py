import re

# Read current HTML
with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

# Read old HTML
with open('old_index.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# Extract old tab-metrics
start_idx = old_html.find('<section id="tab-metrics" class="tab-content">')
end_idx = old_html.find('</section>', start_idx) + len('</section>')
old_metrics = old_html[start_idx:end_idx]

# In the old metrics, the user complained about horizontal scroll.
# The horizontal scroll is usually caused by tables or width:120% or massive margins.
# Let's clean up the old metrics slightly so it obeys the box model but keeps all the "potent" content.

# 1. Fix the ugly purple gradient ROI card to a beautiful dark one (he actually liked the potent metrics, but not the UI of the purple gradient).
# Wait, let's just restore it exactly as it was first, except fix the horizontal scroll.
# Horizontal scroll is caused by `.stats-grid` having fixed widths or margins extending beyond 100%.
old_metrics = old_metrics.replace('style="width: 120%;"', 'style="width: 100%;"')
old_metrics = old_metrics.replace('width: 110%;', 'width: 100%;')
old_metrics = old_metrics.replace('margin-left: -5%;', '')
old_metrics = old_metrics.replace('margin-right: -5%;', '')

# Apply fidelio-table to any raw tables
old_metrics = old_metrics.replace('<table style="width: 100%; border-collapse: collapse; text-align: left;">', '<div class="fidelio-table-container"><table class="fidelio-table">')
old_metrics = old_metrics.replace('</table>\n                        </div>\n                    </div>', '</table></div>\n                        </div>\n                    </div>')

# Replace the current tab-metrics with the cleaned old metrics
curr_start = current_html.find('<section id="tab-metrics" class="tab-content">')
curr_end = current_html.find('</section>', curr_start) + len('</section>')

new_html = current_html[:curr_start] + old_metrics + current_html[curr_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

