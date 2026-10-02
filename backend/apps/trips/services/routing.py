from functools import lru_cache
import requests


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"
HEADERS = {"User-Agent": "SpotterELDApp/1.0 (assessment)"}


@lru_cache(maxsize=1000)
def get_route(start_lat: float, start_lng: float, end_lat: float, end_lng: float) -> dict:
    coords = f"{start_lng},{start_lat};{end_lng},{end_lat}"
    url = f"{OSRM_URL}/{coords}"
    params = {"overview": "full", "geometries": "geojson", "steps": "false"}
    r = requests.get(url, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != "Ok":
        raise ValueError(f"OSRM error: {data.get('message')}")
    route = data["routes"][0]
    return {
        "distance_miles": route["distance"] * 0.000621371,
        "duration_seconds": route["duration"],
        "geometry": route["geometry"],
        "coordinates": route["geometry"]["coordinates"],
    }
