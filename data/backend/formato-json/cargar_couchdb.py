import requests
import json
from config import url_base

URL = url_base

with open("mundial_2026.json", "r", encoding="utf-8") as f:
    data = json.load(f)

r = requests.post(URL, json=data)

print(r.status_code)
print(r.json())