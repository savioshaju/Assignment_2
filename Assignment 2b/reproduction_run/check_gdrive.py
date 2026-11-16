import requests

url = "https://drive.google.com/drive/folders/1Y0OlP0rBU5A2lPE7DFwtUskw0kB71XmN?usp=sharing"
r = requests.get(url)
print("Status:", r.status_code)
if r.status_code == 200:
    for line in r.text.splitlines():
        if "data-item-id" in line or "aria-label" in line or "title=" in line:
            print(line[:200])
