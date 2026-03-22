import os
 
BASE_URL = os.getenv("MODO_BASE_URL", "https://api.modoenergy.com/pub/v1").rstrip("/")
DEFAULT_TIMEOUT = float(os.getenv("MODO_HTTP_TIMEOUT", "30"))
USER_AGENT = "modo-indices-fastmcp/1.0"
 