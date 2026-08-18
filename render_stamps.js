const sharp = require('sharp');
const https = require('https');
const http = require('http');

function fetchImageAsBase64(url) {
    return new Promise((resolve) => {
        if (!url || (!url.startsWith('http') && !url.startsWith('https'))) {
            resolve(null);
            return;
        }
        const client = url.startsWith('https') ? https : http;
        client.get(url, (res) => {
            if (res.statusCode !== 200) {
                resolve(null);
                return;
            }
            const data = [];
            res.on('data', chunk => data.push(chunk));
            res.on('end', () => {
                const buffer = Buffer.concat(data);
                const base64 = buffer.toString('base64');
                const contentType = res.headers['content-type'] || 'image/jpeg';
                resolve(`data:${contentType};base64,${base64}`);
            });
        }).on('error', () => resolve(null));
    });
}

async function generateStampsStrip(total, earned, color, bannerUrl) {
    const width = 1125;
    let base64Banner = null;
    
    if (bannerUrl) {
        base64Banner = await fetchImageAsBase64(bannerUrl);
    }
    
    const hasBanner = !!base64Banner;
    
    // Layout parameters
    const bannerHeight = hasBanner ? 480 : 0;
    const bannerMarginBottom = hasBanner ? 80 : 0;
    const titleHeight = 80;
    const stampsHeight = total > 6 ? 400 : 200;
    const footerHeight = 60;
    
    const height = bannerHeight + bannerMarginBottom + titleHeight + stampsHeight + footerHeight;
    
    let svgContent = '';

    // 1. Banner Image
    if (hasBanner) {
        svgContent += `
        <defs>
            <clipPath id="bannerClip">
                <rect x="50" y="0" width="1025" height="${bannerHeight}" rx="40" ry="40" />
            </clipPath>
        </defs>
        <image href="${base64Banner}" x="50" y="0" width="1025" height="${bannerHeight}" preserveAspectRatio="xMidYMid slice" clip-path="url(#bannerClip)" />
        `;
    }

    // 2. Title Text
    const titleY = bannerHeight + bannerMarginBottom;
    svgContent += `
        <text x="60" y="${titleY}" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#64748b" letter-spacing="3">ACUMULA ${total} SELLOS</text>
        <text x="60" y="${titleY + 40}" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="600" fill="#94a3b8" letter-spacing="1">Y OBTÉN TU RECOMPENSA</text>
    `;

    // 3. Stamps Grid
    const startY = titleY + 80;
    let circlesSvg = '';
    
    if (total > 6) {
        const cols = Math.ceil(total / 2);
        const spacingX = width / (cols + 1);
        const y1 = startY + 80;
        const y2 = startY + 260;
        
        circlesSvg += `<line x1="${spacingX}" y1="${y1}" x2="${spacingX * cols}" y2="${y1}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        circlesSvg += `<line x1="${spacingX}" y1="${y2}" x2="${spacingX * Math.ceil((total - cols))}" y2="${y2}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const isRow2 = i > cols;
            const x = isRow2 ? spacingX * (i - cols) : spacingX * i;
            const y = isRow2 ? y2 : y1;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="${color}" stroke="${color}" stroke-width="4"/>
                <path d="M${x-22} ${y} L${x-6} ${y+18} L${x+26} ${y-22}" fill="none" stroke="white" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="#ffffff" stroke="#e2e8f0" stroke-width="8"/>
                <text x="${x}" y="${y+18}" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    } else {
        const spacing = width / (total + 1);
        const y = startY + 100;
        circlesSvg += `<line x1="${spacing}" y1="${y}" x2="${spacing * total}" y2="${y}" stroke="#f1f5f9" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`;
        
        for(let i=1; i<=total; i++) {
            const x = spacing * i;
            
            if (i <= earned) {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="${color}" stroke="${color}" stroke-width="4"/>
                <path d="M${x-22} ${y} L${x-6} ${y+18} L${x+26} ${y-22}" fill="none" stroke="white" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                circlesSvg += `
                <circle cx="${x}" cy="${y}" r="65" fill="#ffffff" stroke="#e2e8f0" stroke-width="8"/>
                <text x="${x}" y="${y+18}" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#cbd5e1" text-anchor="middle">${i}</text>
                `;
            }
        }
    }
    
    svgContent += circlesSvg;

    // 4. Footer Logo
    // We draw Fidelio logo directly if possible, or just text.
    svgContent += `<text x="${width - 50}" y="${height - 10}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="800" fill="#94a3b8" text-anchor="end" letter-spacing="2">POWERED BY FIDELIO</text>`;

    const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#ffffff" />
        ${svgContent}
    </svg>
    `;
    
    const buffer = await sharp(Buffer.from(svg)).png().toBuffer();
    return buffer;
}

module.exports = { generateStampsStrip };
