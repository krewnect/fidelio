import re

with open('app.js', 'r') as f:
    content = f.read()

rfm_api = """
// ==========================================
// B2B: RFM SEGMENTATION & CHURN PREDICTION
// ==========================================
app.get('/api/merchant/crm-segmentation', requireMerchantAuth, async (req, res) => {
    try {
        const { data: customers, error } = await supabase
            .from('customers')
            .select('*')
            .eq('merchant_id', req.merchantId);
            
        if (error) throw error;
        
        const now = new Date();
        let totalLTV = 0;
        let totalVisits = 0;
        let atRiskCount = 0;
        let whalesCount = 0;
        
        // RFM Logic (Recency, Frequency, Monetary)
        const segmentedCustomers = customers.map(c => {
            let lastVisit = c.last_visit ? new Date(c.last_visit) : null;
            let daysSinceVisit = lastVisit ? Math.floor((now - lastVisit) / (1000 * 60 * 60 * 24)) : 999;
            
            totalLTV += c.lifetime_value || 0;
            totalVisits += c.visits || 0;
            
            // Predicción de Churn
            let risk = 'low';
            if (daysSinceVisit > 30 && c.visits > 1) {
                risk = 'high';
                atRiskCount++;
            } else if (daysSinceVisit > 15) {
                risk = 'medium';
            }
            
            // Ballenas (Whales)
            if (c.lifetime_value > 1000) {
                whalesCount++;
            }
            
            return {
                ...c,
                days_since_visit: daysSinceVisit,
                churn_risk: risk,
                is_whale: c.lifetime_value > 1000
            };
        });
        
        const avgLTV = customers.length ? (totalLTV / customers.length) : 0;
        const avgFreq = customers.length ? (totalVisits / customers.length) : 0;
        
        res.json({ 
            success: true, 
            metrics: {
                total_active: customers.length,
                avg_ltv: avgLTV,
                avg_visits: avgFreq,
                at_risk_count: atRiskCount,
                whales_count: whalesCount
            },
            customers: segmentedCustomers 
        });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});
"""

# Insert before "GEMINI CRM INSIGHTS"
content = content.replace("// ==========================================\n// GEMINI CRM INSIGHTS", rfm_api + "\n// ==========================================\n// GEMINI CRM INSIGHTS")

with open('app.js', 'w') as f:
    f.write(content)
print("RFM patched successfully")
