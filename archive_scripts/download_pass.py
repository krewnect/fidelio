import urllib.request
import zipfile
import io

url = "https://fideliorewards.com/api/wallet/apple/159d4487-95e3-449e-a8aa-fbbc9d8d470d/0b72b4a0-5681-482a-95d8-f8664497af99"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req)
    data = response.read()
    with open("pass.pkpass", "wb") as f:
        f.write(data)
    
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        print("Files in pass:")
        print(z.namelist())
except Exception as e:
    print("Error:", e)
