import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Remove the inner definition
inner_def = """    window.saveDesignToSupabase = async function saveDesignToSupabase() {
        alert("Ejecutando saveDesignToSupabase. tenantId: " + state.tenantId);
        if (!window.supabaseClient || !state.tenantId) return;
        
        const updates = {
            business_name: state.restaurantName,
            industry: state.category,
            color_primary: state.colorPrimary,
            color_accent: state.colorAccent,
            cashback_percent: state.cashbackPercent,
            stamps_total: state.stampsTotal,
            stamps_reward_text: state.stampsReward,
            logo_url: state.customLogoUrl,
            banner_url: state.customBannerUrl,
            branches: state.branches
        };

        try {
            const { error } = await window.supabaseClient
                .from('merchants')
                .update(updates)
                .eq('id', state.tenantId);
                
            if (!error) {
                showToast("Guardado automático en la nube ☁️", "success");
            } else {
                console.error("Supabase Save Error:", error);
                alert("SUPABASE DENEGADO: " + error.message);
                showToast("Error BD: " + error.message, "error");
            }
        } catch (ex) {
            alert("SUPABASE CRASH: " + ex.message + "\\n" + ex.stack);
        }
    }"""

js = js.replace(inner_def, "")

# Add it to the top of the file, completely global
global_def = """
window.saveDesignToSupabase = async function saveDesignToSupabase() {
    console.log("Global saveDesignToSupabase triggered!");
    if (!window.supabaseClient) {
        console.error("No supabase client!");
        return;
    }
    if (!state.tenantId) {
        console.error("No tenantId in state!");
        return;
    }
    
    const updates = {
        business_name: state.restaurantName,
        industry: state.category,
        color_primary: state.colorPrimary,
        color_accent: state.colorAccent,
        cashback_percent: state.cashbackPercent,
        stamps_total: state.stampsTotal,
        stamps_reward_text: state.stampsReward,
        logo_url: state.customLogoUrl,
        banner_url: state.customBannerUrl,
        branches: state.branches
    };

    try {
        const { error } = await window.supabaseClient
            .from('merchants')
            .update(updates)
            .eq('id', state.tenantId);
            
        if (!error) {
            console.log("Guardado automático exitoso");
            if (typeof showToast === 'function') showToast("Guardado automático en la nube ☁️", "success");
        } else {
            console.error("Supabase Save Error:", error);
            alert("SUPABASE DENEGADO: " + error.message);
            if (typeof showToast === 'function') showToast("Error BD: " + error.message, "error");
        }
    } catch (ex) {
        alert("SUPABASE CRASH: " + ex.message + "\\n" + ex.stack);
    }
}
"""

js = global_def + "\n" + js

with open('dashboard.js', 'w') as f:
    f.write(js)
