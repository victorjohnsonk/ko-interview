from __future__ import annotations
 
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional
 
from .config import BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
 
 
class ModoAPIError(Exception):
    """Raised when the Modo API returns an error response."""
 
 
def clean_params(params: dict[str, Any]) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            cleaned[key] = "true" if value else "false"
        elif isinstance(value, list):
            continue
        else:
            cleaned[key] = str(value)
    return cleaned
 
 
def build_url(path: str, params: Optional[dict[str, Any]] = None) -> str:
    path = "/" + path.strip("/")
    url = f"{BASE_URL}{path}"
 
    if not params:
        return url + "/"
 
    scalar_params = clean_params(params)
    repeated_items: list[tuple[str, str]] = []
 
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            for item in value:
                repeated_items.append((key, str(item)))
 
    query_items = list(scalar_params.items()) + repeated_items
    if not query_items:
        return url + "/"
 
    query = urllib.parse.urlencode(query_items, doseq=True)
    return f"{url}/?{query}"
 
 
def http_get(path: str, params: Optional[dict[str, Any]] = None) -> Any:
    url = build_url(path, params)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
 
    context = ssl.create_default_context()
 
    try:
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT, context=context) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return {"ok": True, "status": response.status, "data": None}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"detail": body or exc.reason}
        raise ModoAPIError(
            json.dumps(
                {
                    "status": exc.code,
                    "url": url,
                    "error": payload,
                },
                indent=2,
            )
        ) from exc
    except urllib.error.URLError as exc:
        raise ModoAPIError(
            json.dumps(
                {
                    "url": url,
                    "error": str(exc.reason),
                },
                indent=2,
            )
        ) from exc
    except json.JSONDecodeError as exc:
        raise ModoAPIError(
            json.dumps(
                {
                    "url": url,
                    "error": "Response was not valid JSON",
                },
                indent=2,
            )
        ) from exc