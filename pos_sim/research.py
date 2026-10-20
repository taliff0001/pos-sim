"""
Effect ranges from research/effect-sizes.md (restaurant-weather-demo). These are the ONLY
source of magnitudes. Each entry: (low, high, optional, basis). Optional effects may be zeroed
by a run; optional=False means the effect always exists.
"""

EFFECTS = {
    "rain_dine_in":     (0.90, 0.98, True,  "Foursquare/AccuWeather: light rain -1.6%, medium-heavy -7.4%, heavy -10%"),
    "rain_takeout":     (1.00, 1.20, True,  "guess: delivery/takeout bumps in rain are anecdotal"),
    "patio_bonus":      (0.04, 0.08, True,  "guess; Toast survey directional only"),
    "snow_2":           (0.50, 0.70, False, "one chain: -40% on a snowy weekend; Black Box"),
    "snow_1":           (0.85, 0.95, False, "guess"),
    "frozen_roads":     (0.80, 0.90, False, "guess"),
    "festival_big":     (1.10, 1.25, True,  "reasoned from Charlotte NFL +59%, scaled down"),
    "st_pats_parade":   (1.15, 1.30, True,  "guess"),
    "dickens":          (1.05, 1.15, True,  "guess"),
    "restaurant_week":  (0.98, 1.08, True,  "traffic +10-20%, check -10%"),
    "berglund_coliseum":(1.05, 1.15, True,  "guess"),
    "vt_watch":         (0.97, 1.15, True,  "no published figure; bar with TVs"),
    "vt_home_day":      (0.90, 1.05, True,  "no published figure; fans leave town"),
    "mothers_day":      (1.45, 1.65, False, "Toast +57% GMV vs avg Sunday"),
    "valentines":       (1.20, 1.40, False, "Toast +77% vs a Wednesday; Saturday in 2026"),
    "nye":              (1.15, 1.25, False, "Toast +20% vs Dec avg"),
    "nyd":              (0.70, 0.80, False, "Toast -24% vs Dec avg"),
    "xmas_eve":         (0.65, 0.75, False, "Toast -31% vs Dec avg"),
    "super_bowl_dine":  (0.75, 0.85, False, "Toast dine-in -20%"),
    "july4":            (0.75, 0.85, False, "Toast -21%"),
}

# Per-day seasonality index (Census NAICS 7221/722). Always on; jittered a little by the run.
MONTH_INDEX = {1: .88, 2: .97, 3: 1.02, 4: 1.00, 5: 1.04, 6: 1.05, 7: 1.01, 8: 1.03, 9: .98, 10: .98, 11: .98, 12: 1.03}

# Weekday share of weekly sales (inferred from Toast/Square). The run jitters these and renormalizes.
WEEKDAY_SHARE = {"Mon": .09, "Tue": .10, "Wed": .11, "Thu": .13, "Fri": .19, "Sat": .22, "Sun": .16}

# The January 24-31, 2026 storm: real and always on (local reporting). Multipliers per day.
STORM_2026 = {"2026-01-24": 0.60, "2026-01-25": 0.0, "2026-01-26": 0.0, "2026-01-27": 0.20,
              "2026-01-28": 0.40, "2026-01-29": 0.60, "2026-01-30": 0.75, "2026-01-31": 0.75}

# ---- Volume & shape (research/volume-benchmarks.md) ----
# Takeout share of dollars: reasoned 6-18%, default 11%. Drawn by the run.
TAKEOUT_SHARE = (0.08, 0.14)
# Alcohol share of dollars. NRA operator survey: 21% avg for full-service restaurants that serve alcohol
# (Nov-Dec 2022, n=3,000). Tommy (10/20): no higher than that for downtown Roanoke. Beer/wine only: reasoned.
ALCOHOL_SHARE_BAR = (0.15, 0.25)
ALCOHOL_SHARE_BEER_WINE = (0.03, 0.08)
# Dine-in party size (not published; reasoned, mean ~2.6, solo rare per Toast).
PARTY_SIZES = [1, 2, 3, 4, 5, 6]
PARTY_PROBS = [0.08, 0.52, 0.15, 0.18, 0.05, 0.02]   # mean 2.66
# Takeout: meals per order (not published; reasoned so takeout is ~15-20% of tickets at ~11% of dollars).
TAKEOUT_MEALS = [1, 2, 3, 4]
TAKEOUT_PROBS = [0.30, 0.35, 0.17, 0.18]
# Tips. Toast: FSR card tips 19.9% in Virginia (Q1 2025). Share tipped: reasoned.
TIP_MEAN, TIP_SD = 0.199, 0.04
TIP_SHARE_DINE, TIP_SHARE_TAKEOUT, TAKEOUT_TIP_MEAN = 0.95, 0.60, 0.10
CARD_SHARE = 0.85
# Voids ~1% of tickets; discounts ~2% of gross (vendor estimates, low confidence).
VOID_RATE = 0.01
DISCOUNT_TICKET_RATE = 0.12   # share of tickets with a 10-20% discount (happy hour, staff, promo) -> ~2% of gross
