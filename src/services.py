from typing import Optional, Literal, Any
from .client import http_get
 
 
def _clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
 
 
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
):
    return http_get(
        "/indices",
        _clean_params(
            {
                "market_region": market_region,
            }
        ),
    )
 
 
def get_index_revenue(
    index_id: int,
    date_from: str,
    date_to: str,
):
    return http_get(
        f"/indices/{index_id}/revenue",
        {
            "interval_start": date_from,
            "interval_end": date_to,
        },
    )
 
 
def get_index_revenue_timeseries(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    cursor: Optional[str] = None,
):
    return http_get(
        f"/indices/{index_id}/revenue/timeseries",
        _clean_params(
            {
                "interval_start": date_from,
                "interval_end": date_to,
                "granularity": granularity,
                "cursor": cursor,
            }
        ),
    )
 
 
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    cursor: Optional[str] = None,
):
    return http_get(
        f"/indices/{index_id}/capacity/timeseries",
        _clean_params(
            {
                "date_from": date_from,
                "date_to": date_to,
                "cursor": cursor,
            }
        ),
    )
 
 
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