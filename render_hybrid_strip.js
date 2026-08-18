const sharp = require('sharp');
const https = require('https');
const http = require('http');

async function fetchImageBuffer(url) {
    try {
        if (!url || (!url.startsWith('http') && !url.startsWith('https'))) return null;
        const res = await fetch(url);
        if (!res.ok) return null;
        const arrayBuffer = await res.arrayBuffer();
        const base64 = Buffer.from(arrayBuffer).toString('base64');
        const contentType = res.headers.get('content-type') || 'image/jpeg';
        return `data:${contentType};base64,${base64}`;
    } catch (e) {
        console.error("fetch error", e);
        return null;
    }
}

async function generateHybridStrip(total, earned, color, bannerUrl) {
    const width = 1125;
    const height = 432; // Maximum coupon strip height
    
    let base64Banner = null;
    if (bannerUrl) {
        base64Banner = await fetchImageBuffer(bannerUrl);
    }
    
    let svgContent = '';

    // 1. Full Background Image
    if (base64Banner) {
        // Draw the image filling the entire background
        svgContent += `
        <image href="${base64Banner}" x="0" y="0" width="${width}" height="${height}" preserveAspectRatio="xMidYMid slice" />
        <!-- Dark gradient overlay to make stamps pop -->
        <rect width="${width}" height="${height}" fill="black" fill-opacity="0.5" />
        `;
    } else {
        svgContent += `<rect width="${width}" height="${height}" fill="#111827" />`;
    }

    // 2. Title
    svgContent += `
        <text x="${width/2}" y="80" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="800" fill="#ffffff" letter-spacing="3" text-anchor="middle">ACUMULA ${total} SELLOS</text>
    `;

    // 3. Stamps Grid
    const startY = 100;
    let circlesSvg = '';
    
    if (total > 6) {
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = startY + 90;
        const y2 = startY + 220;
        const r = 40; 
        
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="rgba(255,255,255,0.2)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="rgba(255,255,255,0.2)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="${color}" stroke="#ffffff" stroke-width="3"/>
                <path d="M${x-12} ${y} L${x-4} ${y+10} L${x+14} ${y-12}" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="rgba(0,0,0,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="4"/>
                <text x="${x}" y="${y+12}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="900" fill="rgba(255,255,255,0.6)" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        const spacing = width / (total + 1);
        const y = startY + 160;
        const r = 55;
        
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="rgba(255,255,255,0.2)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="${color}" stroke="#ffffff" stroke-width="4"/>
                <path d="M${x-16} ${y} L${x-5} ${y+12} L${x+18} ${y-16}" fill="none" stroke="white" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="rgba(0,0,0,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="6"/>
                <text x="${x}" y="${y+16}" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="900" fill="rgba(255,255,255,0.6)" text-anchor="middle">${i}</text>
                `;
            }
        }
    }
    
    svgContent += circlesSvg;

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        ${svgContent}
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg)).png().toBuffer();
    return buffer;
}

module.exports = { generateHybridStrip };
