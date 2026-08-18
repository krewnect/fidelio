import re

with open('pass.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    <!-- Supabase -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>"""

replacement = """    <!-- Supabase -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>"""

text = text.replace(target, replacement)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(text)
