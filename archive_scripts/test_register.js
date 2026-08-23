const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function run() {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: "new"
    });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    await page.goto('http://localhost:3001/demoprofessional');
    
    await new Promise(r => setTimeout(r, 2000));
    const bodyHTML = await page.evaluate(() => document.body.innerHTML);
    fs.writeFileSync('page_debug.html', bodyHTML);
    
    await browser.close();
}
run();
