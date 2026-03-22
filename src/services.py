from typing import Optional, Literal
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
):
    path = f"/indices/{index_id}/revenue/timeseries"
    query = f"interval_start={date_from}&interval_end={date_to}"
 
    if granularity:
        query += f"&granularity={granularity}"
 
    return http_get(f"{path}?{query}")
 
 
def get_index_capacity_timeseries(
    index_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    path = f"/indices/{index_id}/capacity/timeseries"
 
    params = []
    if date_from:
        params.append(f"date_from={date_from}")
    if date_to:
        params.append(f"date_to={date_to}")
 
    query = "&".join(params)
 
    if query:
        return http_get(f"{path}?{query}")
 
    return http_get(path)