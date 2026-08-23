import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """app.post('/api/appointments/request', apiLimiter, async (req, res) => {
    const { customerId, campaignId, date, time, notes } = req.body;
    if (!customerId || !campaignId || !date || !time) {"""

replacement = """app.post('/api/appointments/request', apiLimiter, async (req, res) => {
    const customerId = req.body.customerId || req.body.customer_id;
    const campaignId = req.body.campaignId || req.body.campaign_id;
    const { date, time, notes } = req.body;
    
    if (!customerId || !campaignId || !date || !time) {"""

if target in js:
    js = js.replace(target, replacement)
    print("Fixed payload mismatch")
else:
    print("Warning: Target not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
