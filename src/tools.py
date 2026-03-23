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
 
    Use this tool when the user asks things like:
    - "How has battery capacity grown in ERCOT?"
    - "Show me CAISO solar revenues in 2025"
    - "What indices exist for GB?"
    - "Find a battery or storage index in ERCOT"
    - "Which index should I use for NEM batteries?"
 
    Use this tool whenever the user mentions:
    - a region like GB, ERCOT, NEM, or CAISO
    - an asset class or technology like battery, storage, solar, wind, gas, etc.
    - an index by description rather than by explicit numeric ID
 
    Important behavior guidance:
    - Do NOT guess an index_id from the user's wording.
    - First call this tool to inspect candidate indices.
    - Then, if needed, call get_index() on promising candidates to inspect definitions and confirm the best match.
    - Only after confirming the index should you call revenue or capacity tools that require index_id.
 
    Recommended usage pattern:
    1. Call list_indices(market_region=...) when the user mentions a region.
    2. Review returned names and metadata for likely matches.
    3. If multiple candidates exist, call get_index(index_id=...) on the best few.
    4. Use the confirmed index_id in downstream tools.
 
    Parameters:
    - market_region: Optional filter to narrow the search. One of "gb", "ercot", "nem", "caiso".
    - is_custom: Optional filter for whether the index is custom.
 
    Returns:
    - Raw parsed JSON from GET /indices/
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
 
    Use this tool when the user wants a summary or total revenue over a period rather than a full
    time series.
 
    Typical examples:
    - "What revenue did this index earn in 2025?"
    - "Compare total battery revenue in ERCOT for Jan-Dec 2025"
    - "Give me annualized revenue for this index"
    - "Break revenue down by market"
 
    Important behavior guidance:
    - This tool requires a confirmed index_id.
    - If the user describes an index in natural language, first call list_indices(), and optionally
      get_index(), to find and validate the correct index_id.
    - Always provide explicit date_from and date_to.
    - Convert vague time phrases into concrete ISO dates before calling:
      - "2025" -> date_from="2025-01-01", date_to="2025-12-31"
      - "January 2025" -> date_from="2025-01-01", date_to="2025-01-31"
      - "past year" -> convert into a concrete date range based on context before calling
    - Use breakdown="market" if the user asks for a market-level split.
    - Use markets=[...] only if the user explicitly wants a subset of markets.
    - Use capacity_normalisation and time_basis only when the user asks for normalized revenue
      or hourly / annual framing.
 
    Parameters:
    - index_id: Numeric Modo index ID.
    - date_from: Inclusive start date in ISO format YYYY-MM-DD.
    - date_to: Inclusive end date in ISO format YYYY-MM-DD.
    - capacity_normalisation: Optional normalization basis, "mw" or "mwh".
    - time_basis: Optional time basis, "hour" or "year".
    - breakdown: Optional breakdown mode. Use "market" for market-level split.
    - markets: Optional list of market filters.
 
    Returns:
    - Raw parsed JSON from GET /indices/{id}/revenue/
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
    Get revenue for a single confirmed index as a time series over a specified date range.
 
    Use this tool when the user wants revenue over time rather than a single aggregate number.
 
    Typical examples:
    - "Show monthly battery revenue in ERCOT during 2025"
    - "How did this index's revenue evolve over the last year?"
    - "Give me daily revenue time series"
    - "Plot revenue by month"
 
    Important behavior guidance:
    - This is a cursor-paginated endpoint.
    - If the user wants the full time series, prefer get_all_index_revenue_timeseries_pages()
      instead of manually paging.
    - Use this raw paginated tool only when you intentionally want one page or need explicit cursor control.
    - This tool requires a confirmed index_id. Use list_indices() first if the user did not provide one.
    - Translate natural-language periods into concrete ISO dates before calling.
    - Choose granularity based on the question:
      - "base" for the most granular API level
      - "daily" for day-level trends
      - "weekly" for week-level trends
      - "monthly" for month-level trends
    - Use breakdown="market" only if the user asks for market-split series.
    - Use markets=[...] only if the user requests a subset of markets.
 
    Parameters:
    - index_id: Numeric Modo index ID.
    - date_from: Inclusive start date in ISO format YYYY-MM-DD.
    - date_to: Inclusive end date in ISO format YYYY-MM-DD.
    - granularity: Optional time aggregation. One of "base", "daily", "weekly", "monthly".
    - capacity_normalisation: Optional normalization basis, "mw" or "mwh".
    - time_basis: Optional time basis, "hour" or "year".
    - breakdown: Optional revenue breakdown, such as "market".
    - markets: Optional list of market filters.
    - cursor: Optional pagination cursor from a previous response.
 
    Returns:
    - One page of raw parsed JSON from GET /indices/{id}/revenue/timeseries/
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
 
    Use this tool when the user asks about capacity growth, installed capacity, fleet evolution,
    or how MW / MWh changed over time for an index.
 
    Typical examples:
    - "How has battery capacity grown in ERCOT over the past year?"
    - "Show me capacity over time for this index"
    - "What was the change in MWh during 2025?"
    - "How did installed storage capacity evolve?"
 
    Important behavior guidance:
    - This tool requires a confirmed index_id.
    - If the user says something like "ERCOT battery capacity", do NOT guess the index_id.
      First call list_indices(market_region="ercot"), then inspect likely candidates with get_index().
    - This endpoint is cursor-paginated.
    - If the user wants the full period, prefer get_all_index_capacity_timeseries_pages()
      instead of paging manually.
    - Translate vague date language into explicit ISO dates before calling:
      - "2025" -> 2025-01-01 to 2025-12-31
      - "past year" -> convert into a concrete date range before calling
      - "last quarter" -> convert into exact dates before calling
 
    Parameters:
    - index_id: Numeric Modo index ID.
    - date_from: Optional inclusive start date in ISO format YYYY-MM-DD.
    - date_to: Optional inclusive end date in ISO format YYYY-MM-DD.
    - cursor: Optional pagination cursor from a previous response.
 
    Returns:
    - One page of raw parsed JSON from GET /indices/{id}/capacity/timeseries/
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
     Fetch the COMPLETE revenue time series across all cursor-paginated pages for one confirmed index.
 
    Prefer this tool over get_index_revenue_timeseries() when the user wants the full series rather
    than a single page.
 
    Typical examples:
    - "Show the full monthly revenue trend in 2025"
    - "How did revenue change over the year?"
    - "Get all daily revenue points for this date range"
 
    Important behavior guidance:
    - This tool automatically follows pagination and combines results.
    - Use this when the question is about trends, change over time, charting, or any full-period analysis.
    - This tool still requires a confirmed index_id; resolve it first with list_indices() and, if needed, get_index().
    - Convert vague periods into concrete ISO dates before calling.
    - Choose granularity deliberately:
      - "monthly" is often best for broad trend questions
      - "daily" is useful for shorter-term analysis
      - "base" is the most granular available level
 
    Parameters:
    - index_id: Numeric Modo index ID.
    - date_from: Inclusive start date in ISO format YYYY-MM-DD.
    - date_to: Inclusive end date in ISO format YYYY-MM-DD.
    - granularity: Optional time aggregation. One of "base", "daily", "weekly", "monthly".
    - capacity_normalisation: Optional normalization basis, "mw" or "mwh".
    - time_basis: Optional time basis, "hour" or "year".
    - breakdown: Optional revenue breakdown, such as "market".
    - markets: Optional list of market filters.
    - max_pages: Maximum number of pages to fetch before stopping.
 
    Returns:
    - A combined object containing:
      - count_pages_fetched
      - results_count
      - results
      - pages
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
    Fetch the COMPLETE capacity time series across all cursor-paginated pages for one confirmed index.
 
    Prefer this tool over get_index_capacity_timeseries() when the user wants the full period for
    trend, growth, or time-series analysis.
 
    Typical examples:
    - "How has battery capacity grown in ERCOT over the past year?"
    - "Show the full capacity trend for 2025"
    - "Get all capacity points for this index"
    - "How did MW and MWh evolve over time?"
 
    Important behavior guidance:
    - This tool automatically follows pagination and combines results.
    - Use this when the question is about growth, trend, fleet buildout, or change over time.
    - Do NOT guess the index_id from natural language. Resolve it with list_indices() first, and
      use get_index() if needed to validate the best match.
    - Convert vague time periods into concrete ISO dates before calling:
      - "2025" -> 2025-01-01 to 2025-12-31
      - "past year" -> convert into a concrete range before calling
      - "last quarter" -> convert into exact dates before calling
 
    Parameters:
    - index_id: Numeric Modo index ID.
    - date_from: Optional inclusive start date in ISO format YYYY-MM-DD.
    - date_to: Optional inclusive end date in ISO format YYYY-MM-DD.
    - max_pages: Maximum number of pages to fetch before stopping.
 
    Returns:
    - A combined object containing:
      - count_pages_fetched
      - results_count
      - results
      - pages
    """
    return services.get_all_index_capacity_timeseries_pages(
        index_id=index_id,
        date_from=date_from,
        date_to=date_to,
        max_pages=max_pages,
    )