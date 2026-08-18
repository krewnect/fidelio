const sharp = require('sharp');
const https = require('https');
const http = require('http');

async function fetchImageBuffer(url) {
    try {
        if (!url || (!url.startsWith('http') && !url.startsWith('https'))) return null;
        const res = await fetch(url);
        if (!res.ok) return null;
        const arrayBuffer = await res.arrayBuffer();
        return Buffer.from(arrayBuffer);
    } catch (e) {
        console.error("fetchImageBuffer error", e);
        return null;
    }
}

async function generatePremiumBanner(bannerUrl) {
    if (!bannerUrl) return null;
    
    const buffer = await fetchImageBuffer(bannerUrl);
    if (!buffer) return null;
    
    // Resize and crop to exactly match Apple Wallet strip dimensions
    // Apple Wallet usually likes 1125x432 for maximum edge-to-edge width without letterboxing.
    try {
        const processed = await sharp(buffer)
            .resize(1125, 432, {
                fit: 'cover',
                position: 'center'
            })
            .png()
            .toBuffer();
        return processed;
    } catch (err) {
        console.error("sharp error", err);
        return null;
    }
}

module.exports = { generatePremiumBanner };
