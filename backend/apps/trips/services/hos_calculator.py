from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


MAX_DRIVING_HOURS = 11.0
MAX_WINDOW_HOURS = 14.0
BREAK_AFTER_DRIVING = 8.0
BREAK_DURATION = 0.5
MAX_CYCLE_HOURS = 70.0
RESET_HOURS = 34.0
FUEL_INTERVAL_MILES = 1000.0
PICKUP_HOURS = 1.0
DROPOFF_HOURS = 1.0
FUEL_HOURS = 0.5


@dataclass
class Event:
    status: str
    start: datetime
    end: datetime
    location: str = ""
    note: str = ""

    @property
    def hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600.0


@dataclass
class DayLog:
    date: datetime
    events: List[Event] = field(default_factory=list)

    def add(self, status, start, end, location, note=""):
        self.events.append(Event(status, start, end, location, note))

    def totals(self) -> dict:
        t = {"off_duty": 0.0, "sleeper": 0.0, "driving": 0.0, "on_duty": 0.0}
        for e in self.events:
            t[e.status] += e.hours
        return {k: round(v, 2) for k, v in t.items()}

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "events": [
                {
                    "status": e.status,
                    "start": e.start.isoformat(),
                    "end": e.end.isoformat(),
                    "hours": round(e.hours, 2),
                    "location": e.location,
                    "note": e.note,
                }
                for e in self.events
            ],
            "totals": self.totals(),
        }


class HOSCalculator:
    def __init__(self, start_time: datetime, cycle_used: float):
        self.current_time = start_time
        self.cycle_used = float(cycle_used)
        self.days = []
        self.daily_driving = 0.0
        self.daily_window_start = None
        self.driving_since_break = 0.0
        self._new_day()

    def _new_day(self):
        date = self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        self.days.append(DayLog(date=date))
        self.daily_driving = 0.0
        self.daily_window_start = None
        self.driving_since_break = 0.0

    def _ensure_day(self, when):
        if when.date() != self.days[-1].date.date():
            self._new_day()

    def _log(self, status, hours, location, note=""):
        if hours <= 0:
            return
        end = self.current_time + timedelta(hours=hours)
        self._ensure_day(self.current_time)
        self.days[-1].add(status, self.current_time, end, location, note)
        if status == "driving":
            self.daily_driving += hours
            self.driving_since_break += hours
        if status in ("driving", "on_duty"):
            self.cycle_used += hours
        self.current_time = end

    def _window_elapsed(self) -> float:
        if self.daily_window_start is None:
            return 0.0
        return (self.current_time - self.daily_window_start).total_seconds() / 3600.0

    def _take_10h_reset(self, location):
        self._log("off_duty", 10.0, location, "10-hour reset")
        self.daily_driving = 0.0
        self.daily_window_start = None
        self.driving_since_break = 0.0

    def _take_30min_break(self, location):
        self._log("off_duty", BREAK_DURATION, location, "30-min break")
        self.driving_since_break = 0.0

    def _take_34h_restart_if_needed(self, location):
        if self.cycle_used >= MAX_CYCLE_HOURS:
            self._log("off_duty", RESET_HOURS, location, "34-hour restart")
            self.cycle_used = 0.0
            self.daily_driving = 0.0
            self.daily_window_start = None
            self.driving_since_break = 0.0

    def drive(self, distance_miles, avg_speed_mph, from_loc, to_loc):
        remaining_miles = distance_miles
        miles_since_fuel = 0.0
        while remaining_miles > 0.1:
            self._take_34h_restart_if_needed(from_loc)
            window_left = MAX_WINDOW_HOURS - self._window_elapsed()
            drive_left = MAX_DRIVING_HOURS - self.daily_driving
            break_left = BREAK_AFTER_DRIVING - self.driving_since_break
            fuel_left_hours = (FUEL_INTERVAL_MILES - miles_since_fuel) / avg_speed_mph
            hours_by_miles = remaining_miles / avg_speed_mph
            chunk = min(window_left, drive_left, break_left, fuel_left_hours, hours_by_miles)
            if chunk <= 0.01:
                if drive_left <= 0.01 or window_left <= 0.01:
                    self._take_10h_reset(from_loc)
                elif break_left <= 0.01:
                    self._take_30min_break(from_loc)
                else:
                    self._log("on_duty", FUEL_HOURS, from_loc, "Fueling")
                    miles_since_fuel = 0.0
                continue
            if self.daily_window_start is None:
                self.daily_window_start = self.current_time
            miles_this_chunk = chunk * avg_speed_mph
            self._log("driving", chunk, from_loc, f"Driving toward {to_loc}")
            remaining_miles -= miles_this_chunk
            miles_since_fuel += miles_this_chunk
            if miles_since_fuel >= FUEL_INTERVAL_MILES - 0.5 and remaining_miles > 0.5:
                self._log("on_duty", FUEL_HOURS, from_loc, "Fueling")
                miles_since_fuel = 0.0

    def pickup(self, location):
        self._log("on_duty", PICKUP_HOURS, location, "Pickup")

    def dropoff(self, location):
        self._log("on_duty", DROPOFF_HOURS, location, "Dropoff")

    def result(self):
        return [day.to_dict() for day in self.days]
