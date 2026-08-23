import re
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update loadDataFromSupabase
target1 = """                let bCatDisp = state.category || "Profesional";
                if (bCatDisp === 'restaurant') bCatDisp = "Profesional";
                document.getElementById('header-business-category').textContent = bCatDisp;
        }"""

replacement1 = """                let bCatDisp = state.category || "Profesional";
                if (bCatDisp === 'restaurant') bCatDisp = "Profesional";
                document.getElementById('header-business-category').textContent = bCatDisp;

                const sbAvatarIcon = document.getElementById('header-business-icon');
                if (sbAvatarIcon && window.merchantData) {
                    if (window.merchantData.avatar_url) {
                        sbAvatarIcon.innerHTML = '';
                        sbAvatarIcon.style.backgroundImage = `url(${window.merchantData.avatar_url})`;
                        sbAvatarIcon.style.backgroundSize = 'cover';
                        sbAvatarIcon.style.backgroundPosition = 'center';
                        sbAvatarIcon.style.backgroundRepeat = 'no-repeat';
                    } else {
                        sbAvatarIcon.innerHTML = `<span style="font-weight:800; font-size:16px;">${bNameDisp.charAt(0).toUpperCase()}</span>`;
                        sbAvatarIcon.style.backgroundImage = 'none';
                    }
                }
        }"""

js = js.replace(target1, replacement1)

# Update the upload function
target2 = """                    if(avatarContainer) avatarContainer.style.backgroundImage = `url(${newAvatarUrl})`;"""

replacement2 = """                    if(avatarContainer) avatarContainer.style.backgroundImage = `url(${newAvatarUrl})`;
                    
                    const sbAvatarIcon = document.getElementById('header-business-icon');
                    if (sbAvatarIcon) {
                        sbAvatarIcon.innerHTML = '';
                        sbAvatarIcon.style.backgroundImage = `url(${newAvatarUrl})`;
                        sbAvatarIcon.style.backgroundSize = 'cover';
                        sbAvatarIcon.style.backgroundPosition = 'center';
                        sbAvatarIcon.style.backgroundRepeat = 'no-repeat';
                    }"""

js = js.replace(target2, replacement2)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Cache bust
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
