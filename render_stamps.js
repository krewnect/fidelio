const sharp = require('sharp');

async function generateStampsStrip(total, earned, color) {
    const width = 1125;
    const height = total > 6 ? 400 : 220;
    
    let circlesSvg = '';
    
    if (total > 6) {
        // Two rows
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = 120;
        const y2 = 270;
        
        // lines
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#e2e8f0" stroke-width="8" stroke-dasharray="15, 10" />`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#e2e8f0" stroke-width="8" stroke-dasharray="15, 10" />`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="55" fill="${color}" stroke="${color}" stroke-width="4"/>
                <circle cx="${x}" cy="${y}" r="45" fill="${color}" />
                <path d="M${x-18} ${y} L${x-5} ${y+15} L${x+22} ${y-18}" fill="none" stroke="white" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="55" fill="#ffffff" stroke="#cbd5e1" stroke-width="6"/>
                <text x="${x}" y="${y+16}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" fill="#94a3b8" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        // One row
        const spacing = width / (total + 1);
        const y = 110;
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="#e2e8f0" stroke-width="8" stroke-dasharray="15, 10" />`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="55" fill="${color}" stroke="${color}" stroke-width="4"/>
                <circle cx="${x}" cy="${y}" r="45" fill="${color}" />
                <path d="M${x-18} ${y} L${x-5} ${y+15} L${x+22} ${y-18}" fill="none" stroke="white" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="55" fill="#ffffff" stroke="#cbd5e1" stroke-width="6"/>
                <text x="${x}" y="${y+16}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" fill="#94a3b8" text-anchor="middle">${i}</text>
                `;
            }
        }
    }

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="transparent" />
        ${circlesSvg}
        <text x="${width - 40}" y="${height - 20}" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" fill="#cbd5e1" text-anchor="end" letter-spacing="2">POWERED BY FIDELIO</text>
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg))
        .png()
        .toBuffer();
        
    return buffer;
}

module.exports = { generateStampsStrip };
