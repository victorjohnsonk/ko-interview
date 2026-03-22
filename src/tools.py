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
 
 
@mcp.tool
def get_index_revenue(
    index_id: int,
    date_from: str,
    date_to: str,
):
    """Get index revenue."""
    return services.get_index_revenue(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
    )