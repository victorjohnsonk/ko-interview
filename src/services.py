from __future__ import annotations
 
import urllib.parse
from typing import Any, Literal, Optional
 
from .client import http_get
 
 
def _clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
 
 
def extract_cursor(page: dict[str, Any]) -> Optional[str]:
    direct_cursor = page.get("next_cursor") or page.get("cursor")
    if isinstance(direct_cursor, str) and direct_cursor:
        return direct_cursor
 
    next_url = page.get("next")
    if isinstance(next_url, str) and next_url:
        parsed = urllib.parse.urlparse(next_url)
        query = urllib.parse.parse_qs(parsed.query)
        cursor_values = query.get("cursor")
        if cursor_values:
            return cursor_values[0]
 
    return None
 
 
def list_indices(
    market_region: Optional[Literal["gb", "ercot", "nem", "caiso"]] = None,
    is_custom: Optional[bool] = None,
) -> dict[str, Any]:
    return http_get(
        "/indices",
        _clean_params(
            {
                "market_region": market_region,
                "is_custom": is_custom,
            }
        ),
    )
 
 
def get_index_revenue(
    index_id: int,
    date_from: str,
    date_to: str,
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[list[str]] = None,
) -> dict[str, Any]:
    return http_get(
        f"/indices/{index_id}/revenue",
        _clean_params(
            {
                "interval_start": date_from,
                "interval_end": date_to,
                "capacity_normalisation": capacity_normalisation,
                "time_basis": time_basis,
                "breakdown": breakdown,
                "markets": markets,
            }
        ),
    )
 
 
def get_index_revenue_timeseries(
    index_id: int,
    date_from: str,
    date_to: str,
    granularity: Optional[Literal["base", "daily", "weekly", "monthly"]] = None,
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[list[str]] = None,
    cursor: Optional[str] = None,
) -> dict[str, Any]:
    return http_get(
        f"/indices/{index_id}/revenue/timeseries",
        _clean_params(
            {
                "interval_start": date_from,
                "interval_end": date_to,
                "granularity": granularity,
                "capacity_normalisation": capacity_normalisation,
                "time_basis": time_basis,
                "breakdown": breakdown,
                "markets": markets,
                "cursor": cursor,
            }
        ),
    )
 
 
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    cursor: Optional[str] = None,
) -> dict[str, Any]:
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
    capacity_normalisation: Optional[Literal["mw", "mwh"]] = None,
    time_basis: Optional[Literal["hour", "year"]] = None,
    breakdown: Optional[Literal["market"]] = None,
    markets: Optional[list[str]] = None,
    max_pages: int = 20,
) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    combined_results: list[Any] = []
    cursor: Optional[str] = None
 
    for _ in range(max_pages):
        page = get_index_revenue_timeseries(
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
 
        pages.append(page)
 
        results = page.get("results", [])
        if isinstance(results, list):
            combined_results.extend(results)
 
        cursor = extract_cursor(page)
        if not cursor:
            break
 
    return {
        "count_pages_fetched": len(pages),
        "results_count": len(combined_results),
        "results": combined_results,
        "pages": pages,
    }
 
 
def get_all_index_capacity_timeseries_pages(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_pages: int = 20,
) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    combined_results: list[Any] = []
    cursor: Optional[str] = None
 
    for _ in range(max_pages):
        page = get_index_capacity_timeseries(
            index_id=index_id,
            date_from=date_from,
            date_to=date_to,
            cursor=cursor,
        )
 
        pages.append(page)
 
        results = page.get("results", [])
        if isinstance(results, list):
            combined_results.extend(results)
 
        cursor = extract_cursor(page)
        if not cursor:
            break
 
    return {
        "count_pages_fetched": len(pages),
        "results_count": len(combined_results),
        "results": combined_results,
        "pages": pages,
    }