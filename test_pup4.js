const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: "new", args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  await page.goto('https://fideliorewards.com/demoprofessional', { waitUntil: 'networkidle0' });
  
  const loadingDisplay = await page.$eval('#loading-screen', el => el.style.display);
  console.log('Loading screen display:', loadingDisplay);
  
  const formDisplay = await page.$eval('#registration-form-container', el => el.style.display);
  console.log('Form display:', formDisplay);
  
  const campaignsDisplay = await page.$eval('#campaigns-container', el => el.style.display);
  console.log('Campaigns display:', campaignsDisplay);
  
  await browser.close();
})();
