const sharp = require('sharp');

async function generateStampsStrip(total, earned, color) {
    const width = 800;
    const height = total > 6 ? 240 : 150;
    
    let circlesSvg = '';
    
    if (total > 6) {
        // Two rows
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = 70;
        const y2 = 170;
        
        // lines
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#f3f4f6" stroke-width="4" />`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#f3f4f6" stroke-width="4" />`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="35" fill="${color}" stroke="white" stroke-width="8"/>
                <path d="M${x-10} ${y} L${x-3} ${y+8} L${x+12} ${y-10}" fill="none" stroke="white" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="35" fill="white" stroke="#e5e7eb" stroke-width="4"/>
                <text x="${x}" y="${y+8}" font-family="sans-serif" font-size="24" font-weight="bold" fill="#9ca3af" text-anchor="middle">${i}</text>
                <circle cx="${x}" cy="${y}" r="35" fill="none" stroke="white" stroke-width="8"/>
                `;
            }
        }
    } else {
        // One row
        const spacing = width / (total + 1);
        circlesSvg += `<line x1="${spacing}" y1="${height/2}" x2="${spacing * total}" y2="${height/2}" stroke="#f3f4f6" stroke-width="4" />`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            const y = height / 2;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="35" fill="${color}" stroke="white" stroke-width="8"/>
                <path d="M${x-10} ${y} L${x-3} ${y+8} L${x+12} ${y-10}" fill="none" stroke="white" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="35" fill="white" stroke="#e5e7eb" stroke-width="4"/>
                <text x="${x}" y="${y+8}" font-family="sans-serif" font-size="24" font-weight="bold" fill="#9ca3af" text-anchor="middle">${i}</text>
                <circle cx="${x}" cy="${y}" r="35" fill="none" stroke="white" stroke-width="8"/>
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
