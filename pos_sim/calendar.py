"""Real inputs: KROA daily weather and the Roanoke event calendar, from the restaurant-weather-demo repo."""
from __future__ import annotations
import os, pandas as pd

DEMO = os.environ.get("POS_SIM_DEMO_DIR", os.path.expanduser("~/githubio/restaurant-weather-demo"))


def load_weather() -> pd.DataFrame:
    return pd.read_csv(f"{DEMO}/data/kroa_daily.csv", parse_dates=["date"]).set_index("date")


def load_events() -> pd.DataFrame:
    ev = pd.read_csv(f"{DEMO}/data/events.csv", parse_dates=["date"])
    return ev[~ev.effect.str.startswith("storm_day")]   # the storm is applied from research.STORM_2026
