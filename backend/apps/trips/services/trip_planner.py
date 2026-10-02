from datetime import datetime
from django.conf import settings
from apps.trips.services.geocoding import geocode_address
from apps.trips.services.routing import get_route
from apps.trips.services.hos_calculator import HOSCalculator
from apps.fuel.services.optimization import (
    find_stations_near_route,
    optimize_fuel_stops,
    reset_index_cache,
)


def plan_trip(current_location, pickup_location, dropoff_location, cycle_used_hours, start_time=None):
    start_time = start_time or datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    cur_lat, cur_lng = geocode_address(current_location)
    p_lat, p_lng = geocode_address(pickup_location)
    d_lat, d_lng = geocode_address(dropoff_location)

    if None in (cur_lat, cur_lng, p_lat, p_lng, d_lat, d_lng):
        raise ValueError("Could not geocode one or more locations.")

    leg1 = get_route(cur_lat, cur_lng, p_lat, p_lng)
    leg2 = get_route(p_lat, p_lng, d_lat, d_lng)

    total_miles = leg1["distance_miles"] + leg2["distance_miles"]
    avg_speed = settings.AVG_SPEED_MPH

    calc = HOSCalculator(start_time=start_time, cycle_used=cycle_used_hours)
    calc.drive(leg1["distance_miles"], avg_speed, current_location, pickup_location)
    calc.pickup(pickup_location)
    calc.drive(leg2["distance_miles"], avg_speed, pickup_location, dropoff_location)
    calc.dropoff(dropoff_location)

    combined_coords = leg1["coordinates"] + leg2["coordinates"]
    reset_index_cache()
    nearby = find_stations_near_route(combined_coords)
    selected = optimize_fuel_stops(total_miles, nearby)

    return {
        "summary": {
            "current_location": current_location,
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "total_miles": round(total_miles, 1),
            "total_days": len(calc.days),
            "cycle_used_start": round(cycle_used_hours, 2),
            "cycle_used_end": round(calc.cycle_used, 2),
            "start_time": start_time.isoformat(),
            "end_time": calc.current_time.isoformat(),
            "avg_speed_mph": avg_speed,
        },
        "route": {"leg1": leg1["geometry"], "leg2": leg2["geometry"]},
        "fuel_stations": [
            {
                "id": s["id"],
                "name": s["truckstop_name"],
                "address": s["address"],
                "city": s["city"],
                "state": s["state"],
                "price": round(s["retail_price"], 3),
                "lat": s["latitude"],
                "lng": s["longitude"],
            }
            for s in selected[:30]
        ],
        "daily_logs": calc.result(),
    }
