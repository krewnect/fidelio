import urllib.request
import json

url = 'http://localhost:8080/api/campaigns'
data = {
    "id": "12345678-1234-1234-1234-123456789012",
    "type": "hybrid",
    "name": "Campaña de Studio",
    "description": "Generada desde Fidelio Studio",
    "color_primary": "#000000",
    "color_accent": "#ffffff",
    "custom_cta_label": "Recompensa Exclusiva",
    "rules_config": {"stamps_total": 5}
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer asdf'})
try:
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode('utf-8')}")
