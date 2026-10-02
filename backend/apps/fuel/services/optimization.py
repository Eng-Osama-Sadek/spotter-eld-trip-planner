import math
import numpy as np
from scipy.spatial import cKDTree
from django.conf import settings
from apps.fuel.models import FuelStation


_INDEX_CACHE = {"tree": None, "stations": None}


def _build_index():
    qs = FuelStation.objects.exclude(latitude__isnull=True).values(
        "id", "opis_truckstop_id", "truckstop_name", "address", "city",
        "state", "retail_price", "latitude", "longitude",
    )
    stations = list(qs)
    if not stations:
        _INDEX_CACHE["tree"] = None
        _INDEX_CACHE["stations"] = []
        return
    coords = np.array([[s["latitude"], s["longitude"]] for s in stations])
    _INDEX_CACHE["tree"] = cKDTree(coords)
    _INDEX_CACHE["stations"] = stations


def get_index():
    if _INDEX_CACHE["tree"] is None:
        _build_index()
    return _INDEX_CACHE["tree"], _INDEX_CACHE["stations"]


def find_stations_near_route(route_coordinates, buffer_miles=10.0):
    tree, stations = get_index()
    if tree is None or not stations:
        return []
    route_latlon = np.array([[c[1], c[0]] for c in route_coordinates])
    buffer_deg = buffer_miles / 69.0
    indices = set()
    batch = 1000
    for i in range(0, len(route_latlon), batch):
        chunk = route_latlon[i:i + batch]
        for hits in tree.query_ball_point(chunk, r=buffer_deg):
            indices.update(hits)
    return [stations[i] for i in indices]


def optimize_fuel_stops(total_distance_miles, nearby_stations, max_range_miles=None):
    if not nearby_stations:
        return []
    max_range = max_range_miles or settings.MAX_VEHICLE_RANGE_MILES
    needed = max(1, math.ceil(total_distance_miles / max_range))
    sorted_stations = sorted(nearby_stations, key=lambda s: s["retail_price"])
    return sorted_stations[: max(needed * 3, 10)]


def reset_index_cache():
    _INDEX_CACHE["tree"] = None
    _INDEX_CACHE["stations"] = None
