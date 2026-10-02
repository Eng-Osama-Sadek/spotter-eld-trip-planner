from functools import lru_cache
import requests
from django.core.cache import cache


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "SpotterELDApp/1.0 (assessment)"}


@lru_cache(maxsize=10000)
def geocode_address(address: str):
    if not address:
        return None, None

    cache_key = f"geo::{address.lower().strip()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    params = {"q": address, "format": "json", "limit": 1, "countrycodes": "us,ca,mx"}
    try:
        r = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=12)
        r.raise_for_status()
        data = r.json()
        if data:
            result = (float(data[0]["lat"]), float(data[0]["lon"]))
            cache.set(cache_key, result, timeout=60 * 60 * 24 * 30)
            return result
    except requests.RequestException:
        pass
    return None, None
