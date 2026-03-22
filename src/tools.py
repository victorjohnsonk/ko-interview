from typing import Optional, Literal, List, Dict, Any
from fastmcp import FastMCP
 
from . import services
 
mcp = FastMCP("Modo Energy")
 
 
@mcp.tool
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
    is_custom: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Discover available Modo indices and find candidate index IDs before using any index-specific tool.
 
    This should usually be the FIRST tool called for open-ended questions where the user describes
    an index by region, technology, market, or theme instead of giving a numeric index_id.
    """
    return services.list_indices(
        market_region=market_region,
        is_custom=is_custom,
    )
 
 
@mcp.tool
def get_index_revenue(
    index_id: int,
    date_from: str,
    date_to: str,
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Get aggregated revenue for a single confirmed index over a specified date range.
    """
    return services.get_index_revenue(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        capacity_normalisation=capacity_normalisation,
        time_basis=time_basis,
        breakdown=breakdown,
        markets=markets,
    )
 
 
@mcp.tool
def get_index_revenue_timeseries(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[List[str]] = None,
    cursor: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get revenue for a single confirmed index as a time series.
    """
    return services.get_index_revenue_timeseries(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        granularity=granularity,
        capacity_normalisation=capacity_normalisation,
        time_basis=time_basis,
        breakdown=breakdown,
        markets=markets,
        cursor=cursor,
    )
 
 
@mcp.tool
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    cursor: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get MW and MWh capacity for a single confirmed index over time.
    """
    return services.get_index_capacity_timeseries(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        cursor=cursor,
    )
 
 
@mcp.tool
def get_all_index_revenue_timeseries_pages(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[List[str]] = None,
    max_pages: int = 20,
) -> Dict[str, Any]:
    """
    Fetch the COMPLETE revenue time series across all pages.
    """
    return services.get_all_index_revenue_timeseries_pages(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        granularity=granularity,
        capacity_normalisation=capacity_normalisation,
        time_basis=time_basis,
        breakdown=breakdown,
        markets=markets,
        max_pages=max_pages,
    )
 
 
@mcp.tool
def get_all_index_capacity_timeseries_pages(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_pages: int = 20,
) -> Dict[str, Any]:
    """
    Fetch the COMPLETE capacity time series across all pages.
    """
    return services.get_all_index_capacity_timeseries_pages(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        max_pages=max_pages,
    )