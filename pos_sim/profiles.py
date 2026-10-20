"""Hours profiles. Times are hours after midnight on the business day (26 = 2 am next day)."""

PROFILES = {
    "standard": {
        "open": {"Mon": 11, "Tue": 11, "Wed": 11, "Thu": 11, "Fri": 11, "Sat": 11, "Sun": 11},
        "kitchen_close": {"Mon": 22, "Tue": 22, "Wed": 22, "Thu": 22, "Fri": 23, "Sat": 23, "Sun": 22},
        "bar_close": {"Mon": 22, "Tue": 22, "Wed": 22, "Thu": 22, "Fri": 24, "Sat": 24, "Sun": 22},
        "late_menu": False, "closed_days": [], "brunch_days": [],
    },
    "late-bar": {
        # Bar to 2 am (Virginia last call). A short late menu stays available while the bar is open
        # (food must be available, not ordered). Drinks-only tickets are fine at any hour.
        "open": {"Mon": 11, "Tue": 11, "Wed": 11, "Thu": 11, "Fri": 11, "Sat": 11, "Sun": 11},
        "kitchen_close": {"Mon": 22, "Tue": 22, "Wed": 22, "Thu": 22, "Fri": 23, "Sat": 23, "Sun": 22},
        "bar_close": {"Mon": 24, "Tue": 24, "Wed": 24, "Thu": 26, "Fri": 26, "Sat": 26, "Sun": 24},
        "late_menu": True, "closed_days": [], "brunch_days": [],
    },
    "brunch": {
        "open": {"Mon": 11, "Tue": 11, "Wed": 11, "Thu": 11, "Fri": 11, "Sat": 10, "Sun": 10},
        "kitchen_close": {"Mon": 22, "Tue": 22, "Wed": 22, "Thu": 22, "Fri": 23, "Sat": 23, "Sun": 21},
        "bar_close": {"Mon": 22, "Tue": 22, "Wed": 22, "Thu": 22, "Fri": 24, "Sat": 24, "Sun": 21},
        "late_menu": False, "closed_days": [], "brunch_days": ["Sat", "Sun"],
    },
    "closed-monday": {
        "open": {"Tue": 11, "Wed": 11, "Thu": 11, "Fri": 11, "Sat": 11, "Sun": 11},
        "kitchen_close": {"Tue": 22, "Wed": 22, "Thu": 22, "Fri": 23, "Sat": 23, "Sun": 22},
        "bar_close": {"Tue": 22, "Wed": 22, "Thu": 22, "Fri": 24, "Sat": 24, "Sun": 22},
        "late_menu": False, "closed_days": ["Mon"], "brunch_days": [],
    },
}

# Within-day ticket shape. Dinner: Toast reservation slots (6pm ~25-27%, 7pm ~25-28%) and the 7-8pm payment
# peak; lunch is ~25-30% of dollars (reasoned). Hours past 24 are after midnight (bar only).
HOUR_WEIGHTS = {
    10: 0.35, 11: 0.75, 12: 1.30, 13: 1.00, 14: 0.35, 15: 0.15, 16: 0.25, 17: 0.70,
    18: 1.75, 19: 1.95, 20: 1.50, 21: 0.75, 22: 0.30, 23: 0.25, 24: 0.20, 25: 0.12,
}
