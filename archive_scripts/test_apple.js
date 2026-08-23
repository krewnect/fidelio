const fetch = require('node-fetch');
async function run() {
    try {
        const url = 'http://localhost:3001/api/wallet/apple/d73dabae-0ac8-4305-97d7-3b6192c575ad/0b72b4a0-5681-482a-95d8-f8664497af99';
        const res = await fetch(url);
        console.log("Status:", res.status);
        if (!res.ok) {
            console.log("Error:", await res.text());
        } else {
            console.log("Success! Got a blob of size", (await res.buffer()).length);
        }
    } catch(e) {
        console.error(e);
    }
}
run();
