with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('studioIframe.src = `/studio/index.html?rest_id=${restId}`;', 
                    'const tier = (window.merchantData && window.merchantData.business_type === "business") ? "business" : "basic";\n                studioIframe.src = `/studio/index.html?rest_id=${restId}&tier=${tier}`;')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()
js = js.replace('iframe.src = `/studio/index.html?rest_id=${restId}`;', 
                'const tier = (window.merchantData && window.merchantData.business_type === "business") ? "business" : "basic";\n            iframe.src = `/studio/index.html?rest_id=${restId}&tier=${tier}`;')
js = js.replace('studioIframe.src = `/studio/index.html?rest_id=${restId}`;', 
                'const tier = (window.merchantData && window.merchantData.business_type === "business") ? "business" : "basic";\n            studioIframe.src = `/studio/index.html?rest_id=${restId}&tier=${tier}`;')
with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Added tier variable to iframe src.")
