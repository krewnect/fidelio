const puppeteer = require('puppeteer-core');

async function run() {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless: "new",
        args: ['--no-sandbox']
    });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.error('PAGE ERROR:', err));

    await page.goto('https://fideliorewards.com/demoprofessional?v=4');
    
    await page.waitForSelector('#register-form', { visible: true });
    
    // Attempt to submit WITHOUT filling anything to see what validation triggers
    console.log("Submitting form empty...");
    await page.click('#btn-submit');
    await new Promise(r => setTimeout(r, 1000));
    
    await page.type('#cust-name', 'Live Test');
    await page.type('#cust-email', 'livetest999@test.com');
    
    console.log("Submitting form partially filled...");
    await page.click('#btn-submit');
    await new Promise(r => setTimeout(r, 1000));
    
    // Check if phone or birthday are visible
    const phoneVis = await page.$eval('#phone-group', el => el.style.display !== 'none');
    console.log("Phone visible:", phoneVis);
    if (phoneVis) {
        await page.type('#cust-phone', '1234567890');
    }
    
    const bdayVis = await page.$eval('#birthday-group', el => el.style.display !== 'none');
    console.log("Bday visible:", bdayVis);
    if (bdayVis) {
        await page.type('#cust-birthday', '1990-01-01');
    }
    
    console.log("Submitting form fully filled...");
    await page.click('#btn-submit');
    await new Promise(r => setTimeout(r, 4000));
    
    console.log("FINAL URL:", page.url());
    
    const swalVisible = await page.evaluate(() => {
        const swal = document.querySelector('.swal2-container');
        return swal ? swal.innerText : null;
    });
    console.log("SWAL:", swalVisible);
    
    await browser.close();
}

run().catch(console.error);
