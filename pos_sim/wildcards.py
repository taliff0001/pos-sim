"""
The wildcard catalog. The code decides type, dates and magnitude from these rules; the LLM
(when on) only supplies the one-line story. Magnitudes scale with intensity.
"""
from __future__ import annotations
import numpy as np, pandas as pd

INTENSITY = {"low": 0.6, "medium": 1.0, "high": 1.5}

CATALOG = {
    "closure":        dict(days=(1, 3),   mult=(0.0, 0.0),   touch="all",     story="closed: {reason}"),
    "equipment":      dict(days=(2, 6),   mult=(0.55, 0.8),  touch="food",    story="short menu while {thing} was out"),
    "private_party":  dict(days=(1, 1),   mult=(1.4, 1.9),   touch="all",     story="a private party of {n} on an off night"),
    "price_increase": dict(days=(0, 0),   mult=(1.04, 1.09), touch="prices",  story="menu prices raised about {pct}% from this date on"),
    "menu_change":    dict(days=(0, 0),   mult=(1.0, 1.0),   touch="menu",    story="a dish renamed ({old} became {new}), so its history splits"),
    "brunch_trial":   dict(days=(35, 56), mult=(1.08, 1.18), touch="weekend", story="tried weekend brunch for {weeks} weeks, then dropped it"),
    "construction":   dict(days=(21, 45), mult=(0.82, 0.92), touch="all",     story="street work out front for {weeks} weeks"),
    "big_day":        dict(days=(1, 1),   mult=(1.6, 2.2),   touch="all",     story="one huge day: {reason}"),
    "staff_shortage": dict(days=(7, 14),  mult=(0.85, 0.93), touch="dine_in", story="short-staffed for {weeks} weeks; patio closed"),
}
CLOSURE_REASONS = ["a kitchen fire inspection", "a burst pipe", "a family funeral", "a power outage on the block", "a deep clean"]
THINGS = ["the walk-in cooler", "the fryer", "the hood vent", "the dish machine", "the ice machine"]
BIG_DAY_REASONS = ["a wedding rehearsal dinner that took the whole dining room", "a reunion that booked every table",
                   "a conference lunch next door with no reservation", "a food-blog post that went around"]


def draw_wildcards(rng: np.random.Generator, n: int, intensity: str, start: str, end: str, open_days: pd.DatetimeIndex) -> list[dict]:
    """Pick n distinct wildcard types with dates inside the window. Returns dicts the engine applies."""
    types = list(CATALOG)
    chosen = list(rng.choice(types, size=min(n, len(types)), replace=False))
    k = INTENSITY[intensity]
    out = []
    for t in chosen:
        c = CATALOG[t]
        lo, hi = c["mult"]
        mult = float(rng.uniform(lo, hi))
        if t not in ("closure", "menu_change"):
            mult = 1 + (mult - 1) * k
        ndays = int(rng.integers(c["days"][0], c["days"][1] + 1)) if c["days"][1] else 0
        latest = pd.Timestamp(end) - pd.Timedelta(days=max(ndays, 1))
        cands = open_days[(open_days >= pd.Timestamp(start) + pd.Timedelta(days=14)) & (open_days <= latest)]
        if t == "private_party":
            cands = cands[cands.weekday < 4]            # Mon-Thu
        if t == "brunch_trial":
            cands = cands[(cands.month >= 3) & (cands.month <= 5)]
        d0 = pd.Timestamp(rng.choice(cands.values)) if len(cands) else pd.Timestamp(start)
        d1 = d0 + pd.Timedelta(days=max(ndays - 1, 0))
        fill = {"reason": str(rng.choice(CLOSURE_REASONS)), "thing": str(rng.choice(THINGS)), "n": int(rng.integers(30, 70)),
                "pct": round((mult - 1) * 100), "old": "", "new": "", "weeks": max(1, round(ndays / 7))}
        if t == "big_day":
            fill["reason"] = str(rng.choice(BIG_DAY_REASONS))
        out.append(dict(type=t, start=str(d0.date()), end=str(d1.date()), mult=round(mult, 3), touch=c["touch"],
                        story_template=c["story"], fill=fill))
    return out
