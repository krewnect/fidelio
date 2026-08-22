const sharp = require('sharp');
const fs = require('fs');

async function generateStampsStrip(total, earned, color) {
    const width = 1125;
    const height = total > 6 ? 480 : 300;
    
    let circlesSvg = '';
    
    if (total > 6) {
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = 150;
        const y2 = 330;
        
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="${color}" stroke="${color}" stroke-width="4"/>
                <circle cx="${x}" cy="${y}" r="55" fill="${color}" />
                <path d="M${x-22} ${y} L${x-6} ${y+18} L${x+26} ${y-22}" fill="none" stroke="white" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="#f8fafc" stroke="#e2e8f0" stroke-width="6"/>
                <text x="${x}" y="${y+18}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="52" font-weight="700" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        const spacing = width / (total + 1);
        const y = height / 2;
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="${color}" stroke="${color}" stroke-width="4"/>
                <circle cx="${x}" cy="${y}" r="55" fill="${color}" />
                <path d="M${x-22} ${y} L${x-6} ${y+18} L${x+26} ${y-22}" fill="none" stroke="white" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="#f8fafc" stroke="#e2e8f0" stroke-width="6"/>
                <text x="${x}" y="${y+18}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="52" font-weight="700" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    }

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#ffffff" />
        ${circlesSvg}
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg)).png().toBuffer();
    fs.writeFileSync('test_strip.png', buffer);
    console.log("Done");
}

generateStampsStrip(10, 3, '#111827').catch(console.error);
