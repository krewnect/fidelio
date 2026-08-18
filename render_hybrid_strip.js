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
    const height = 432; // EXACT Apple Wallet max height for coupon strips to prevent scaling
    
    let base64Banner = null;
    if (bannerUrl) {
        base64Banner = await fetchImageBuffer(bannerUrl);
    }
    
    let svgContent = '';

    // 1. Banner Image (Top portion)
    if (base64Banner) {
        svgContent += `
        <defs>
            <clipPath id="bannerClip">
                <rect x="40" y="20" width="1045" height="180" rx="25" ry="25" />
            </clipPath>
        </defs>
        <image href="${base64Banner}" x="40" y="20" width="1045" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#bannerClip)" />
        `;
    }

    // 2. Stamps Grid
    const startY = base64Banner ? 220 : 60; // Push down if banner exists
    let circlesSvg = '';
    
    if (total > 6) {
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = startY + 70;
        const y2 = startY + 160;
        const r = 32; // Circle radius
        
        // Connecting lines
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#f1f5f9" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#f1f5f9" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="${color}" stroke="${color}" stroke-width="3"/>
                <path d="M${x-12} ${y} L${x-4} ${y+10} L${x+14} ${y-12}" fill="none" stroke="white" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="#ffffff" stroke="#e2e8f0" stroke-width="4"/>
                <text x="${x}" y="${y+10}" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="900" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        const spacing = width / (total + 1);
        const y = startY + 110;
        const r = 45;
        
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="#f1f5f9" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="${color}" stroke="${color}" stroke-width="4"/>
                <path d="M${x-16} ${y} L${x-5} ${y+12} L${x+18} ${y-16}" fill="none" stroke="white" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="${r}" fill="#ffffff" stroke="#e2e8f0" stroke-width="6"/>
                <text x="${x}" y="${y+14}" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="900" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    }
    
    svgContent += circlesSvg;

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#ffffff" />
        ${svgContent}
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg)).png().toBuffer();
    return buffer;
}

module.exports = { generateHybridStrip };
