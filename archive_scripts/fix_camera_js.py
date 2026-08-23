with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

target_populate = """        const avatarEl = document.getElementById('acc-avatar-letter');
        if (avatarEl) avatarEl.textContent = bName.charAt(0).toUpperCase();"""

replacement_populate = """        const avatarEl = document.getElementById('acc-avatar-letter');
        const avatarContainer = document.getElementById('acc-avatar-container');
        if (state.merchant.avatar_url) {
            if(avatarEl) avatarEl.style.display = 'none';
            if(avatarContainer) avatarContainer.style.backgroundImage = `url(${state.merchant.avatar_url})`;
        } else {
            if(avatarEl) {
                avatarEl.style.display = 'block';
                avatarEl.textContent = bName.charAt(0).toUpperCase();
            }
            if(avatarContainer) avatarContainer.style.backgroundImage = 'linear-gradient(135deg, var(--accent-violet), #c084fc)';
        }"""

js = js.replace(target_populate, replacement_populate)

# Now inject the upload logic somewhere around the btnSaveAccProfile
target_logic = """        const btnSaveAccProfile = document.getElementById('btn-save-acc-profile');"""

replacement_logic = """        const avatarUpload = document.getElementById('acc-avatar-upload');
        if (avatarUpload) {
            avatarUpload.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file || !window.merchantSession) return;
                
                const icon = document.getElementById('acc-camera-icon');
                const originalIcon = icon.className;
                icon.className = 'fa-solid fa-spinner fa-spin';
                
                try {
                    const ext = file.name.split('.').pop();
                    const filename = `avatar_${window.merchantSession.user.id}_${Date.now()}.${ext}`;
                    
                    const { data, error: uploadError } = await window.supabaseClient.storage.from('logos').upload(filename, file, { upsert: true });
                    if (uploadError) throw new Error('Error al subir: ' + uploadError.message);
                    
                    const { data: publicUrlData } = window.supabaseClient.storage.from('logos').getPublicUrl(filename);
                    const newAvatarUrl = publicUrlData.publicUrl;
                    
                    const { error: dbError } = await window.supabaseClient.from('merchants').update({ avatar_url: newAvatarUrl }).eq('id', window.merchantSession.user.id);
                    if (dbError) throw new Error('Error guardando en base de datos');
                    
                    window.merchantData.avatar_url = newAvatarUrl;
                    const avatarEl = document.getElementById('acc-avatar-letter');
                    const avatarContainer = document.getElementById('acc-avatar-container');
                    if(avatarEl) avatarEl.style.display = 'none';
                    if(avatarContainer) avatarContainer.style.backgroundImage = `url(${newAvatarUrl})`;
                    
                    if (typeof showToast === 'function') showToast('Foto de perfil actualizada', 'success');
                } catch (err) {
                    if (typeof showToast === 'function') showToast(err.message, 'error');
                } finally {
                    icon.className = originalIcon;
                }
            });
        }

        const btnSaveAccProfile = document.getElementById('btn-save-acc-profile');"""

js = js.replace(target_logic, replacement_logic)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
