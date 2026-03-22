from typing import Optional, Literal
from .client import http_get
 
 
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
):
    path = "/indices"
    if market_region:
        path += f"?market_region={market_region}"
    return http_get(path)