const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 800 });
    await page.goto('file://' + __dirname + '/index.html', { waitUntil: 'networkidle0' });
    
    await page.evaluate(() => {
        document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
        document.getElementById('tab-builder').style.display = 'block';
        if(window.updatePassRender) {
            document.getElementById('stamps-total').value = '10';
            document.getElementById('program-type-select').value = 'stamps';
            document.getElementById('color-primary').value = '#8b5cf6';
            window.updatePassRender();
        }
    });
    
    await new Promise(r => setTimeout(r, 1000));
    const element = await page.$('#pass-render');
    if (element) {
        await element.screenshot({ path: 'dashboard_card.png' });
    }
    
    await browser.close();
})();
