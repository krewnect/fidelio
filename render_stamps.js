const sharp = require('sharp');

async function generateStampsStrip(total, earned, color) {
    const width = 1000;
    const height = total > 6 ? 280 : 180;
    
    let circlesSvg = '';
    
    if (total > 6) {
        // Two rows
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = 80;
        const y2 = 200;
        
        // lines
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#d1d5db" stroke-width="6" />`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#d1d5db" stroke-width="6" />`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="45" fill="${color}" stroke="white" stroke-width="10"/>
                <path d="M${x-15} ${y} L${x-4} ${y+12} L${x+18} ${y-15}" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="45" fill="#f9fafb" stroke="#9ca3af" stroke-width="6"/>
                <text x="${x}" y="${y+12}" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="#4b5563" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        // One row
        const spacing = width / (total + 1);
        const y = height / 2;
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="#d1d5db" stroke-width="6" />`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="45" fill="${color}" stroke="white" stroke-width="10"/>
                <path d="M${x-15} ${y} L${x-4} ${y+12} L${x+18} ${y-15}" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="45" fill="#f9fafb" stroke="#9ca3af" stroke-width="6"/>
                <text x="${x}" y="${y+12}" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="#4b5563" text-anchor="middle">${i}</text>
                `;
            }
        }
    }

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="transparent" />
        ${circlesSvg}
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg))
        .png()
        .toBuffer();
        
    return buffer;
}

module.exports = { generateStampsStrip };
