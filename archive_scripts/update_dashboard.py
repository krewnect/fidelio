import re
import os

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js'

with open(filepath, 'r') as f:
    content = f.read()

# Fix 1: Append client_reference_id to Stripe payment links
old_stripe_redirect = "window.location.href = data.stripe_payment_link;"
new_stripe_redirect = """
                let finalLink = data.stripe_payment_link;
                if(finalLink.includes('?')) {
                    finalLink += '&client_reference_id=' + window.merchantSession.user.id;
                } else {
                    finalLink += '?client_reference_id=' + window.merchantSession.user.id;
                }
                window.location.href = finalLink;
"""

content = content.replace(old_stripe_redirect, new_stripe_redirect)

# Fix 2: Replace `localStorage.getItem('fidelio_token') || 'dummy'` with `window.merchantSession.access_token`
# Make sure to handle potential null errors if window.merchantSession isn't set for some reason, though it should be.
old_token_str = "`Bearer ${localStorage.getItem('fidelio_token') || 'dummy'}`"
new_token_str = "`Bearer ${window.merchantSession?.access_token || ''}`"

content = content.replace(old_token_str, new_token_str)

with open(filepath, 'w') as f:
    f.write(content)
