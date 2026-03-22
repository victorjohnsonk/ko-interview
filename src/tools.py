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
 
 
@mcp.tool
def get_index_revenue_timeseries(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
):
    """Get index revenue timeseries."""
    return services.get_index_revenue_timeseries(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        granularity=granularity,
    )
 
 
@mcp.tool
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    """Get index capacity timeseries."""
    return services.get_index_capacity_timeseries(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
    )
 
 
@mcp.tool
def get_all_index_revenue_timeseries_pages(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    max_pages: int = 10,
):
    """Get all revenue timeseries pages."""
    return services.get_all_index_revenue_timeseries_pages(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        granularity=granularity,
        max_pages=max_pages,
    )