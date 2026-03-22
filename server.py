import json
import urllib.request
from typing import Optional, Literal
 
from fastmcp import FastMCP
 
mcp = FastMCP("Modo Energy")
 
BASE_URL = "https://api.modoenergy.com/pub/v1"
 
 
def http_get(path: str) -> dict:
    url = f"{BASE_URL}{path}/"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
    )
 
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))
 
 
@mcp.tool
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
):
    """List indices."""
    path = "/indices"
    if market_region:
        path += f"?market_region={market_region}"
    return http_get(path)
 
 
def main():
    mcp.run(transport="http", host="0.0.0.0", port=8005)
 
 
if __name__ == "__main__":
    main()