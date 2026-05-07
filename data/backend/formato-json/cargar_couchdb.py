import requests
import json

URL = "http://admin:admin@localhost:5985/jugadores/_bulk_docs"

with open("mundial_2026.json", "r", encoding="utf-8") as f:
    data = json.load(f)

r = requests.post(URL, json=data)

print(r.status_code)
print(r.json())