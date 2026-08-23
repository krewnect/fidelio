with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

toggle_css = """
/* NATIVE CSS TOGGLE SWITCHES */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
  margin: 0;
}
.toggle-switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-switch .slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}
.toggle-switch .slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.toggle-switch input:checked + .slider {
  background-color: #10b981;
}
.toggle-switch input:focus + .slider {
  box-shadow: 0 0 1px #10b981;
}
.toggle-switch input:checked + .slider:before {
  transform: translateX(20px);
}
"""

css += "\n" + toggle_css

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the toggle HTML to use purely CSS (remove the inner knob spans and inline styles)
target_phone = """<label class="toggle-switch" style="position:relative; display:inline-block; width:44px; height:24px; margin:0;">
                                        <input type="checkbox" id="req-phone" checked style="opacity:0; width:0; height:0;">
                                        <span class="slider round" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#10b981; transition:.4s; border-radius:34px;"></span>
                                        <span class="knob" id="req-phone-knob" style="position:absolute; content:''; height:18px; width:18px; left:22px; bottom:3px; background-color:white; transition:.4s; border-radius:50%; box-shadow:0 2px 4px rgba(0,0,0,0.2);"></span>
                                    </label>"""
replacement_phone = """<label class="toggle-switch">
                                        <input type="checkbox" id="req-phone" checked>
                                        <span class="slider"></span>
                                    </label>"""
html = html.replace(target_phone, replacement_phone)

target_bday = """<label class="toggle-switch" style="position:relative; display:inline-block; width:44px; height:24px; margin:0;">
                                        <input type="checkbox" id="req-birthday" checked style="opacity:0; width:0; height:0;">
                                        <span class="slider round" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#10b981; transition:.4s; border-radius:34px;"></span>
                                        <span class="knob" id="req-birthday-knob" style="position:absolute; content:''; height:18px; width:18px; left:22px; bottom:3px; background-color:white; transition:.4s; border-radius:50%; box-shadow:0 2px 4px rgba(0,0,0,0.2);"></span>
                                    </label>"""
replacement_bday = """<label class="toggle-switch">
                                        <input type="checkbox" id="req-birthday" checked>
                                        <span class="slider"></span>
                                    </label>"""
html = html.replace(target_bday, replacement_bday)

# Bump CSS
html = re.sub(r'href="styles\.css\?v=\d+"', 'href="styles.css?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
