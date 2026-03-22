from typing import Optional, Literal
from fastmcp import FastMCP
 
from . import services
 
mcp = FastMCP("Modo Energy")
 
 
@mcp.tool
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
):
    """List indices."""
    return services.list_indices(market_region=market_region)