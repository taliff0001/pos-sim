"""Self-check on a finished export. A run that fails doesn't ship."""
from __future__ import annotations
import pandas as pd
from .profiles import PROFILES, HOUR_WEIGHTS


def validate_orders(orders: list[dict], sc: dict, menu_names: set[str]) -> list[str]:
    problems = []
    if not orders:
        return ["no orders"]
    prof = PROFILES[sc["hours_profile"]]
    n_void = sum(o["voided"] for o in orders)
    if n_void / len(orders) > 0.03:
        problems.append(f"void rate {n_void / len(orders):.1%} > 3%")
    for o in orders:
        if o["closed"] < o["opened"]:
            problems.append(f"{o['order_id']}: closed before opened")
        wd = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][pd.Timestamp(o["business_date"]).weekday()]
        if wd not in prof["open"]:
            problems.append(f"{o['order_id']}: order on a closed day ({wd})")
        h = o["opened"].hour + (24 if o["opened"].date() != o["business_date"] else 0)
        if not (prof["open"][wd] <= h < prof["bar_close"][wd]):
            problems.append(f"{o['order_id']}: opened at hour {h} outside {prof['open'][wd]}-{prof['bar_close'][wd]}")
        food_ok_until = prof["bar_close"][wd] if prof["late_menu"] else prof["kitchen_close"][wd]
        for it in o["items"]:
            if it["qty"] <= 0 or it["net"] < 0:
                problems.append(f"{o['order_id']}: bad qty/net on {it['item']}")
            base = it["item"]
            if base not in menu_names:
                problems.append(f"{o['order_id']}: item not on menu: {base}")
            if not it["alcohol"] and it["category"] != "Non-Alcoholic" and h >= food_ok_until:
                problems.append(f"{o['order_id']}: food sold after the kitchen closed ({it['item']} at hour {h})")
        if abs(sum(i["net"] for i in o["items"]) - o["subtotal"]) > 0.05:
            problems.append(f"{o['order_id']}: lines don't sum to subtotal")
        if len(problems) > 50:
            problems.append("... (truncated)"); break
    return problems
