import requests
r=requests.get("https://polarisgrids.com")
print(r.status_code)
print(r.text[:200])
