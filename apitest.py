import requests

a = requests.get("http://localhost:8766")

print(a.json())