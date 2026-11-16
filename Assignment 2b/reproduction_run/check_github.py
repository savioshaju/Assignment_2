import requests

url = "https://api.github.com/repos/savioshaju/Multimodal-Emotion-Recognition/contents"
r = requests.get(url)
print("Status:", r.status_code)
if r.status_code == 200:
    for item in r.json():
        print(item["name"], item["type"])
else:
    print(r.text)
