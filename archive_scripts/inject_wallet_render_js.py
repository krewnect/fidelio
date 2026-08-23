import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_render = """        const rBal = document.getElementById('render-balance');
        if (rBal) {
            const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
            rBal.textContent = `$${bal.toFixed(2)}`;
        }"""
        
new_render = """        const rBal = document.getElementById('render-balance');
        if (rBal) {
            const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
            rBal.textContent = `$${bal.toFixed(2)}`;
        }
        
        const rWalletBlock = document.getElementById('render-wallet-block');
        const rWalletBal = document.getElementById('render-wallet-balance');
        const rCashbackBlock = document.getElementById('render-cashback-block');
        
        // Show Wallet Block if Prepaid is Active
        if (state.prepaidActive === true) {
            if (rWalletBlock) {
                rWalletBlock.style.display = 'block';
                // Mock balance based on the bonus config
                const demoWallet = (state.prepaidAmount || 500) + (state.prepaidBonus || 100);
                if (rWalletBal) rWalletBal.textContent = `$${demoWallet.toFixed(2)}`;
            }
        } else {
            if (rWalletBlock) rWalletBlock.style.display = 'none';
        }
        
        // Hide Cashback Block if Cashback is false
        if (state.cashbackActive === false && pType !== 'cashback' && pType !== 'hybrid') {
            if (rCashbackBlock) rCashbackBlock.style.display = 'none';
        } else {
            if (rCashbackBlock) rCashbackBlock.style.display = 'block';
        }
"""
js = js.replace(old_render, new_render)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
    
print("Injected Wallet render JS logic.")
