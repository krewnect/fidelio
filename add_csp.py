import re

files_to_update = ['index.html', 'scanner.html', 'landing.html']

csp_tag = """    <!-- SECURITY: Strict Content Security Policy -->
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com https://cdn.jsdelivr.net https://kit.fontawesome.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://ka-f.fontawesome.com; connect-src 'self' https://*.supabase.co https://*.supabase.in https://api.stripe.com; frame-src 'self' https://js.stripe.com; img-src 'self' data: blob: https:;">
    <meta http-equiv="X-XSS-Protection" content="1; mode=block">
    <meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
    <meta http-equiv="X-Frame-Options" content="SAMEORIGIN">"""

for filename in files_to_update:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Insert after <head>
        if '<head>' in html and csp_tag not in html:
            html = html.replace('<head>', '<head>\n' + csp_tag)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Added CSP to {filename}")
    except Exception as e:
        print(f"Error updating {filename}: {e}")
