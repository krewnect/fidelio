const { JSDOM } = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;
const window = dom.window;

window.merchantSession = { user: { email: 'hola@fideliorewards.com' } };

let toastMsg = null;
window.showToast = function(msg, type) {
    console.log("TOAST:", type, msg);
    toastMsg = msg;
}

window.supabaseClient = {
    from: function() {
        return {
            insert: async function(data) {
                console.log("Supabase insert called with:", data);
                return { error: null };
            }
        };
    }
};

const js = fs.readFileSync('dashboard.js', 'utf8');
try {
    eval(js);
} catch(e) {
    console.error("Eval Error:", e);
}

try {
    document.getElementById('promo-code-input').value = 'TEST2024';
    document.getElementById('promo-type-select').value = 'discount';
    document.getElementById('promo-target-plan').value = 'business';
    document.getElementById('promo-discount-input').value = '50';

    console.log("Calling generatePromoCode()...");
    window.generatePromoCode().catch(e => console.error("Crash inside generatePromoCode:", e));
} catch(e) {
    console.error("Setup Error:", e);
}
