"""
The math. Day → expected sales by channel → orders → item lines.

Business day: a ticket opened before the bar closes belongs to the day it was opened, even if
the clock has passed midnight. The export shows the wall-clock timestamp; the analyst has to
work the business day out.
"""
from __future__ import annotations
import numpy as np, pandas as pd
from .profiles import PROFILES, HOUR_WEIGHTS
from .menu import Restaurant, ALCOHOL
from . import research as R

WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
CROWD = {"festival_big", "st_pats_parade", "dickens", "berglund_coliseum", "vt_watch", "vt_home_day"}


def open_days(profile: str, start: str, end: str) -> pd.DatetimeIndex:
    days = pd.date_range(start, end, freq="D")
    closed = set(PROFILES[profile]["closed_days"])
    return days[[WD[d.weekday()] not in closed for d in days]]


def expected_day(d: pd.Timestamp, w, todays_effects: list[str], sc: dict, weekly_base: float) -> dict:
    """Expected sales by channel for one day, before noise. Mirrors the demo simulator's logic."""
    e = sc["effects"]; wd = WD[d.weekday()]
    base = weekly_base * sc["weekday_share"][wd] * sc["month_index"][d.month]
    dec_avg = weekly_base / 7 * sc["month_index"][12]
    exp = {"dine_in": base * (1 - sc["takeout_share"]), "takeout": base * sc["takeout_share"], "patio": 0.0}

    if "closed" in todays_effects:
        return {k: 0.0 for k in exp}
    storm = sc["storm_2026"].get(str(d.date()))
    if storm is not None:
        return {k: v * storm for k, v in exp.items()}

    dry = w.svc_precip_in < 0.01 and w.snow_level == 0
    if dry and 65 <= w.svc_mean_f <= 85:
        exp["patio"] = base * e["patio_bonus"]
    if w.svc_precip_in >= 0.10:
        exp["dine_in"] *= e["rain_dine_in"]; exp["takeout"] *= e["rain_takeout"]
    m = e["snow_2"] if w.snow_level == 2 else e["snow_1"] if w.snow_level == 1 else e["frozen_roads"] if w.frozen_roads else 1.0
    for k in exp: exp[k] *= m

    crowd = sorted([e[x] for x in todays_effects if x in CROWD], key=lambda v: -abs(v - 1))
    for i, v in enumerate(crowd):
        mm = 1 + (v - 1) * 0.5 ** i
        for k in exp: exp[k] *= mm
    for x in todays_effects:
        if x in ("mothers_day", "valentines", "july4", "restaurant_week"):
            for k in exp: exp[k] *= e[x]
        elif x in ("nye", "nyd", "xmas_eve"):
            scale = dec_avg * e[x] / base
            for k in exp: exp[k] *= scale
        elif x == "super_bowl":
            exp["dine_in"] *= e["super_bowl_dine"]; exp["patio"] *= e["super_bowl_dine"]
    return exp


def apply_wildcards(d: pd.Timestamp, exp: dict, sc: dict) -> tuple[dict, float]:
    """Returns (expected, price_multiplier) after any wildcard active on d."""
    price_mult = 1.0
    for wc in sc["wildcards"]:
        s, e2 = pd.Timestamp(wc["start"]), pd.Timestamp(wc["end"])
        if wc["type"] == "price_increase":
            if d >= s: price_mult *= wc["mult"]
            continue
        if wc["type"] == "menu_change" or not (s <= d <= e2):
            continue
        t = wc["touch"]
        if t == "all":
            exp = {k: v * wc["mult"] for k, v in exp.items()}
        elif t == "food":
            exp = {k: v * (wc["mult"] if k != "takeout" else 1.0) for k, v in exp.items()}
        elif t == "dine_in":
            exp["dine_in"] *= wc["mult"]; exp["patio"] = 0.0
        elif t == "weekend" and d.weekday() >= 5:
            exp = {k: v * wc["mult"] for k, v in exp.items()}
    return exp, price_mult


def _pick(rng, items, weights):
    w = np.array(weights, float); w /= w.sum()
    return items[rng.choice(len(items), p=w)]


# Per-guest mains by daypart: lunch leans sandwiches/salads, dinner leans entrees.
MAIN_WEIGHTS = {"lunch": {"Sandwiches": 5, "Salads": 3, "Entrees": 2, "Brunch": 6},
                "dinner": {"Entrees": 8, "Sandwiches": 1.5, "Salads": 1},
                "late": {"Late Night": 1}}


def _daypart(hour: int, h_kitchen: int) -> str:
    if hour >= h_kitchen:
        return "late"
    return "lunch" if hour < 16 else "dinner"


def _drink_lambda(sc: dict, rest: Restaurant, rng) -> dict:
    """Calibrate alcoholic drinks per adult guest so the run hits its alcohol share of dollars.
    Uses a quick dry run of the food side; returns lambdas by daypart (lunch is a fraction of dinner)."""
    target = sc["alcohol_share"]
    by_cat = {}
    for it in rest.items:
        by_cat.setdefault(it.category, []).append(it)
    def avg_price(cats):
        items = [it for c in cats for it in by_cat.get(c, [])]
        if not items: return 0.0
        w = np.array([it.popularity for it in items]); return float((np.array([it.price for it in items]) * w).sum() / w.sum())
    drink_cats = ("Beer", "Wine", "Cocktails") if sc["bar"] else ("Beer", "Wine")
    p_drink = avg_price(drink_cats)
    # food dollars per guest by daypart (main + share of app/side/dessert + NA drink)
    food = {"dinner": avg_price(["Entrees"]) * 0.7 + avg_price(["Sandwiches", "Salads"]) * 0.3 + 0.55 * avg_price(["Appetizers"]) / 2.6
                      + 0.3 * avg_price(["Sides"]) + 0.28 * avg_price(["Desserts"]) + 0.5 * avg_price(["Non-Alcoholic"]),
            "lunch": avg_price(["Sandwiches", "Salads"]) * 0.8 + avg_price(["Entrees"]) * 0.2 + 0.25 * avg_price(["Appetizers"]) / 2.4
                     + 0.35 * avg_price(["Sides"]) + 0.05 * avg_price(["Desserts"]) + 0.85 * avg_price(["Non-Alcoholic"])}
    # dinner carries ~73% of dine-in dollars; lunch drinks run at 25% of the dinner rate
    lunch_ratio, dinner_w, lunch_w = 0.25, 0.73, 0.27
    # alcohol $ / total $ = target, solved for dinner lambda (takeout has almost none, so scale by dine-in share)
    dine_target = target / (1 - sc["takeout_share"])
    f = dinner_w * food["dinner"] + lunch_w * food["lunch"]
    d_per = dinner_w * p_drink + lunch_w * p_drink * lunch_ratio
    lam = dine_target * f / ((1 - dine_target) * d_per) if p_drink else 0.0
    return {"dinner": lam, "lunch": lam * lunch_ratio, "late": max(lam * 1.6, 0.8), "bar": max(lam * 2.2, 1.2)}


def build_orders(d: pd.Timestamp, exp: dict, rest: Restaurant, sc: dict, rng: np.random.Generator,
                 price_mult: float, renamed: dict, lam: dict) -> list[dict]:
    """Turn a day's expected dollars into orders with item lines whose net totals reach the day's dollars."""
    prof = PROFILES[sc["hours_profile"]]; wd = WD[d.weekday()]
    if wd not in prof["open"]:
        return []
    h_open, h_kitchen, h_bar = prof["open"][wd], prof["kitchen_close"][wd], prof["bar_close"][wd]
    brunch = wd in prof["brunch_days"]
    by_cat = {}
    for it in rest.items:
        by_cat.setdefault(it.category, []).append(it)
    hs = [h for h in range(h_open, h_bar) if h in HOUR_WEIGHTS]
    ws = [HOUR_WEIGHTS[h] for h in hs]
    drink_pool = [c for c in (("Beer", "Wine", "Cocktails") if sc["bar"] else ("Beer", "Wine")) if c in by_cat]
    rename_from = renamed.get("_from", pd.Timestamp("2100-01-01"))

    def add(lines, cat):
        if cat in by_cat: lines.append(cat)

    orders, oid = [], 0
    for channel, dollars in exp.items():
        if dollars <= 0 or (channel == "patio" and not sc["patio"]):
            continue
        running = 0.0
        while running < dollars:
            oid += 1
            hour = _pick(rng, hs, ws); minute = int(rng.integers(0, 60))
            opened = d + pd.Timedelta(hours=hour, minutes=minute)
            part = _daypart(hour, h_kitchen)
            if part == "late" and not prof["late_menu"]:
                part = "late-drinks"
            at_bar = channel == "dine_in" and sc["bar"] and (part.startswith("late") or rng.random() < 0.15)
            if channel == "takeout":
                party = int(rng.choice(R.TAKEOUT_MEALS, p=R.TAKEOUT_PROBS))
            elif at_bar:
                party = int(rng.choice([1, 2, 3], p=[0.45, 0.45, 0.10]))
            else:
                party = int(rng.choice(R.PARTY_SIZES, p=R.PARTY_PROBS))
            area = "Patio" if channel == "patio" else "Takeout" if channel == "takeout" else ("Bar" if at_bar else "Main Dining")
            lines = []
            # mains
            if part != "late-drinks":
                key = "late" if part == "late" else part
                mw = {c: w for c, w in MAIN_WEIGHTS[key].items() if c in by_cat and (c != "Brunch" or (brunch and hour < 15))}
                p_main = 0.97 if channel == "takeout" else (0.55 if at_bar else 0.95)
                for _g in range(party):
                    if mw and rng.random() < p_main:
                        add(lines, _pick(rng, list(mw), list(mw.values())))
            # shared and extras (kitchen hours only)
            if part in ("lunch", "dinner"):
                if rng.random() < (0.55 if part == "dinner" else 0.25) * (0.6 if channel == "takeout" else 1): add(lines, "Appetizers")
                if party >= 5 and rng.random() < 0.5: add(lines, "Appetizers")
                for _g in range(party):
                    if rng.random() < 0.3: add(lines, "Sides")
                    if channel != "takeout" and rng.random() < (0.28 if part == "dinner" else 0.05): add(lines, "Desserts")
            elif part == "late":
                if rng.random() < 0.4: add(lines, "Late Night")
            # drinks
            if channel == "takeout":
                for _g in range(party):
                    if rng.random() < 0.35: add(lines, "Non-Alcoholic")
            else:
                l = lam["bar"] if at_bar else lam["late"] if part.startswith("late") else lam[part]
                for _g in range(party):
                    n_alc = rng.poisson(l) if drink_pool else 0
                    for _k in range(n_alc):
                        lines.append(_pick(rng, drink_pool, [1] * len(drink_pool)))
                    if n_alc == 0 and rng.random() < (0.85 if part == "lunch" else 0.6): add(lines, "Non-Alcoholic")
            if not lines:
                add(lines, drink_pool[0] if (drink_pool and channel != "takeout") else "Non-Alcoholic")

            voided = rng.random() < R.VOID_RATE
            disc = float(rng.choice([0.10, 0.15, 0.20])) if rng.random() < R.DISCOUNT_TICKET_RATE else 0.0
            item_rows, subtotal = [], 0.0
            for cat in lines:
                pool = by_cat[cat]
                it = _pick(rng, pool, [x.popularity for x in pool])
                qty = 1
                mods = [m for m in it.modifiers if rng.random() < 0.25]
                price = round(it.price * price_mult, 2)
                gross = round((price + sum(m.price for m in mods)) * qty, 2)
                discount = round(gross * disc, 2)
                name = renamed.get(it.name, it.name) if d >= rename_from else it.name
                item_rows.append(dict(item=name, category=it.category, qty=qty, price=price, modifiers=[m.name for m in mods],
                                      gross=gross, discount=discount, net=round(gross - discount, 2), voided=voided,
                                      alcohol=it.category in ALCOHOL))
                subtotal += gross - discount
            # collapse duplicate items on one ticket into qty, like a POS does
            merged = {}
            for r in item_rows:
                k = (r["item"], tuple(r["modifiers"]))
                if k in merged:
                    m = merged[k]; m["qty"] += 1
                    for f in ("gross", "discount", "net"): m[f] = round(m[f] + r[f], 2)
                else:
                    merged[k] = dict(r)
            item_rows = list(merged.values())
            tax = round(subtotal * 0.053, 2)   # Virginia 5.3% state sales tax (Roanoke's 5.5% meals tax left out)
            tender = "Card" if rng.random() < R.CARD_SHARE else "Cash"
            tip = 0.0
            if tender == "Card" and not voided:
                if channel == "takeout":
                    if rng.random() < R.TIP_SHARE_TAKEOUT: tip = subtotal * max(0, rng.normal(R.TAKEOUT_TIP_MEAN, 0.04))
                elif rng.random() < R.TIP_SHARE_DINE:
                    tip = subtotal * max(0.05, rng.normal(R.TIP_MEAN, R.TIP_SD))
            tip = round(tip, 2)
            duration = int(rng.integers(8, 25)) if channel == "takeout" else (int(rng.integers(25, 75)) if part == "lunch" else int(rng.integers(55, 120)))
            if not voided:
                running += subtotal
            orders.append(dict(order_id=f"{d.strftime('%y%m%d')}-{oid:04d}", opened=opened, closed=opened + pd.Timedelta(minutes=duration),
                               business_date=d.date(), channel=channel, dining_option="Take Out" if channel == "takeout" else "Dine In",
                               area=area, party=party, server=str(rng.choice(rest.servers)), items=item_rows,
                               subtotal=round(subtotal, 2), tax=tax, tip=tip, tender=tender, voided=voided, discount_pct=disc))
    return orders


def simulate(cfg, sc: dict, rest: Restaurant, wx: pd.DataFrame, ev: pd.DataFrame):
    rng = np.random.default_rng(cfg.seed + 1)
    days = open_days(sc["hours_profile"], cfg.start, cfg.end)
    sigma = np.sqrt(np.log(1 + cfg.noise ** 2))
    eff_by_day = ev.groupby("date").effect.apply(list).to_dict()

    renamed = {}
    for wc in sc["wildcards"]:
        if wc["type"] == "menu_change":
            it = max(rest.items, key=lambda x: x.popularity)
            new = it.name + " Deluxe" if "Burger" in it.name else "House " + it.name
            renamed = {it.name: new, "_from": pd.Timestamp(wc["start"])}
            wc["fill"]["old"], wc["fill"]["new"] = it.name, new

    def year_total(wb):
        return sum(sum(apply_wildcards(d, expected_day(d, wx.loc[d], eff_by_day.get(d, []), sc, wb), sc)[0].values()) for d in days)
    wb = cfg.annual_sales / 52
    wb *= cfg.annual_sales / year_total(wb)

    lam = _drink_lambda(sc, rest, rng)
    # Pilot: simulate a sample of days on a separate RNG, measure the alcohol share, and rescale the
    # drink rates (on the odds scale) so the run lands on its target. Two passes is plenty.
    if lam["dinner"] > 0:
        prng = np.random.default_rng(cfg.seed + 99)
        sample = days[prng.choice(len(days), size=min(60, len(days)), replace=False)]
        t = sc["alcohol_share"]
        for _pass in range(3):
            alc = tot = 0.0
            for d in sample:
                exp, pm = apply_wildcards(d, expected_day(d, wx.loc[d], eff_by_day.get(d, []), sc, wb), sc)
                for o in build_orders(d, exp, rest, sc, prng, pm, renamed, lam):
                    if o["voided"]: continue
                    for it in o["items"]:
                        tot += it["net"]; alc += it["net"] if it["alcohol"] else 0.0
            a = alc / tot if tot else t
            if a <= 0: break
            k = (t / (1 - t)) / (a / (1 - a))
            lam = {kk: v * k for kk, v in lam.items()}
    all_orders, daily = [], []
    for d in days:
        exp, pm = apply_wildcards(d, expected_day(d, wx.loc[d], eff_by_day.get(d, []), sc, wb), sc)
        noise = rng.lognormal(-sigma ** 2 / 2, sigma)
        exp = {k: v * noise for k, v in exp.items()}
        orders = build_orders(d, exp, rest, sc, rng, pm, renamed, lam)
        all_orders.extend(orders)
        daily.append(dict(date=d.date(), expected=round(sum(exp.values()), 2), orders=len(orders),
                          net=round(sum(o["subtotal"] for o in orders if not o["voided"]), 2)))
    return all_orders, pd.DataFrame(daily)
