import re

with open('render_stamps.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_func = """function fetchImageAsBase64(url) {
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
}"""

new_func = """async function fetchImageAsBase64(url) {
    try {
        if (!url || (!url.startsWith('http') && !url.startsWith('https'))) return null;
        const res = await fetch(url);
        if (!res.ok) return null;
        const buffer = await res.arrayBuffer();
        const base64 = Buffer.from(buffer).toString('base64');
        const contentType = res.headers.get('content-type') || 'image/jpeg';
        return `data:${contentType};base64,${base64}`;
    } catch (e) {
        console.error("fetchImageAsBase64 error", e);
        return null;
    }
}"""

code = code.replace(old_func, new_func)

with open('render_stamps.js', 'w', encoding='utf-8') as f:
    f.write(code)
