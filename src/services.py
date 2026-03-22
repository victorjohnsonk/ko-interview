from typing import Optional, Literal, Any
from .client import http_get
 
 
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
):
    path = "/indices"
    if market_region:
        path += f"?market_region={market_region}"
    return http_get(path)
 
 
def get_index_revenue(
    index_id: int,
    date_from: str,
    date_to: str,
):
    path = f"/indices/{index_id}/revenue"
    path += f"?interval_start={date_from}&interval_end={date_to}"
    return http_get(path)
 
 
def get_index_revenue_timeseries(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    cursor: Optional[str] = None,
):
    path = f"/indices/{index_id}/revenue/timeseries"
    params = [
        f"interval_start={date_from}",
        f"interval_end={date_to}",
    ]
 
    if granularity:
        params.append(f"granularity={granularity}")
    if cursor:
        params.append(f"cursor={cursor}")
 
    query = "&".join(params)
    return http_get(f"{path}?{query}")
 
 
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    cursor: Optional[str] = None,
):
    path = f"/indices/{index_id}/capacity/timeseries"
 
    params = []
    if date_from:
        params.append(f"date_from={date_from}")
    if date_to:
        params.append(f"date_to={date_to}")
    if cursor:
        params.append(f"cursor={cursor}")
 
    query = "&".join(params)
 
    if query:
        return http_get(f"{path}?{query}")
 
    return http_get(path)
 
 
def get_all_index_revenue_timeseries_pages(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    max_pages: int = 10,
) -> dict[str, Any]:
    all_results: list[Any] = []
    cursor: Optional[str] = None
 
    for _ in range(max_pages):
        page = get_index_revenue_timeseries(
            index_id=index_id,
            date_from=date_from,
            date_to=date_to,
            granularity=granularity,
            cursor=cursor,
        )
 
        results = page.get("results", [])
        if isinstance(results, list):
            all_results.extend(results)
 
        cursor = page.get("next_cursor")
        if not cursor:
            break
 
    return {
        "results_count": len(all_results),
        "results": all_results,
    }
 
 
def get_all_index_capacity_timeseries_pages(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_pages: int = 10,
) -> dict[str, Any]:
    all_results: list[Any] = []
    cursor: Optional[str] = None
 
    for _ in range(max_pages):
        page = get_index_capacity_timeseries(
            index_id=index_id,
            date_from=date_from,
            date_to=date_to,
            cursor=cursor,
        )
 
        results = page.get("results", [])
        if isinstance(results, list):
            all_results.extend(results)
 
        cursor = page.get("next_cursor")
        if not cursor:
            break
 
    return {
        "results_count": len(all_results),
        "results": all_results,
    }