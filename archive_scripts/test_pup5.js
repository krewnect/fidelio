const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: "new", args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  await page.goto('https://fideliorewards.com/demoprofessional', { waitUntil: 'networkidle0' });
  
  const innerHTML = await page.$eval('#campaign-grid', el => el.innerHTML);
  console.log('Grid content:', innerHTML.trim() ? 'Has content' : 'Empty');
  
  await browser.close();
})();
