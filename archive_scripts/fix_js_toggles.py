with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# The JS tries to style knob.parentElement.children[1] which might throw error if we removed the knob.
# Let's just comment out the animation part inside the event listener
import re

target1 = """    // Form fields toggles
    ['req-phone', 'req-birthday'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', (e) => {
                const knob = document.getElementById(id + '-knob');
                if (knob) {
                    knob.parentElement.children[1].style.backgroundColor = e.target.checked ? '#8b5cf6' : '#ccc';
                    knob.style.transform = e.target.checked ? 'translateX(14px)' : 'translateX(0)';
                }
            });
        }
    });"""

replacement1 = """    // Form fields toggles (now handled via pure CSS, no JS animation needed here)
"""
js = js.replace(target1, replacement1)

target2 = """            const reqPhone = document.getElementById('req-phone');
            const reqPhoneKnob = document.getElementById('req-phone-knob');
            if (reqPhone) {
                reqPhone.checked = prefs.require_phone !== false;
                if (reqPhoneKnob) {
                    reqPhoneKnob.parentElement.children[1].style.backgroundColor = reqPhone.checked ? '#8b5cf6' : '#ccc';
                    reqPhoneKnob.style.transform = reqPhone.checked ? 'translateX(14px)' : 'translateX(0)';
                }
            }
            
            const reqBday = document.getElementById('req-birthday');
            const reqBdayKnob = document.getElementById('req-birthday-knob');
            if (reqBday) {
                reqBday.checked = prefs.require_birthday !== false;
                if (reqBdayKnob) {
                    reqBdayKnob.parentElement.children[1].style.backgroundColor = reqBday.checked ? '#8b5cf6' : '#ccc';
                    reqBdayKnob.style.transform = reqBday.checked ? 'translateX(14px)' : 'translateX(0)';
                }
            }"""

replacement2 = """            const reqPhone = document.getElementById('req-phone');
            if (reqPhone) {
                reqPhone.checked = prefs.require_phone !== false;
            }
            
            const reqBday = document.getElementById('req-birthday');
            if (reqBday) {
                reqBday.checked = prefs.require_birthday !== false;
            }"""
js = js.replace(target2, replacement2)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
