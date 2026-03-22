import json
import urllib.request
 
BASE_URL = "https://api.modoenergy.com/pub/v1"
 
 
def http_get(path: str) -> dict:
    url = f"{BASE_URL}{path}/"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
    )
 
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))