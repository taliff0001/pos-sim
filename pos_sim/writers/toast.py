"""
Toast-shaped export: ItemSelectionDetails.csv (one row per item line, 30 columns) and
OrderDetails.csv (one row per order, 24 columns), per Toast's data export field reference
(https://doc.toasttab.com/doc/platformguide/adminDataExportFieldReference.html).
Timestamps are wall-clock, like the real export; the business day is not a column.
"""
from __future__ import annotations
import pandas as pd

ISD_COLS = ["Location", "Order Id", "Order #", "Sent Date", "Order Date", "Check Id", "Server", "Table", "Dining Area",
            "Service", "Dining Option", "Item Selection Id", "Item Id", "Master Id", "SKU", "Menu Item", "Menu Subgroup(s)",
            "Menu Group", "Menu", "Sales Category", "Gross Price", "Discnt", "Net Price", "Qty", "Tax", "Void?", "Deferred",
            "Tax Exempt", "Tax Inclusion Option", "Dining Option Tax", "Tab Name"]
OD_COLS = ["Location", "Order Id", "Order #", "Checks", "Opened", "# of Guests", "Tab Names", "Server", "Table", "Revenue Center",
           "Dining Area", "Service", "Dining Options", "Discount Amount", "Amount", "Tax", "Tip", "Gratuity", "Total", "Voided",
           "Paid", "Closed", "Duration (Opened to Paid)", "Order Source"]
FOOD_GROUPS = {"Appetizers": "Food", "Entrees": "Food", "Sandwiches": "Food", "Salads": "Food", "Sides": "Food", "Desserts": "Food",
               "Brunch": "Food", "Late Night": "Food", "Beer": "Beer", "Wine": "Wine", "Cocktails": "Liquor", "Non-Alcoholic": "N/A Bev"}


def _service(ts: pd.Timestamp) -> str:
    h = ts.hour
    return "Lunch" if 10 <= h < 15 else "Dinner" if 15 <= h < 22 else "Late Night"


def _ts(ts: pd.Timestamp) -> str:
    return ts.strftime("%-m/%-d/%y %-I:%M %p")


def write(orders: list[dict], out_dir: str, location: str, menu_ids: dict):
    isd, od = [], []
    sel = 0
    for o in orders:
        table = "" if o["channel"] == "takeout" else str((hash(o["order_id"]) % 24) + 1)
        onum = o["order_id"].split("-")[1].lstrip("0") or "0"
        for it in o["items"]:
            sel += 1
            iid = menu_ids.setdefault(it["item"], 100000 + len(menu_ids))
            isd.append([location, o["order_id"], onum, _ts(o["opened"] + pd.Timedelta(minutes=2)), _ts(o["opened"]), o["order_id"] + "-1",
                        o["server"], table, o["area"], _service(o["opened"]), o["dining_option"], f"S{sel:07d}", iid, iid, "",
                        it["item"] + (" [" + ", ".join(it["modifiers"]) + "]" if it["modifiers"] else ""), it["category"],
                        FOOD_GROUPS[it["category"]], "Main Menu", FOOD_GROUPS[it["category"]], f'{it["gross"]:.2f}', f'{it["discount"]:.2f}',
                        f'{it["net"]:.2f}', it["qty"], f'{it["net"] * 0.053:.2f}', "true" if it["voided"] else "false", "false", "false",
                        "false", "0.00", ""])
        disc = round(sum(i["discount"] for i in o["items"]), 2)
        total = round(o["subtotal"] + o["tax"] + o["tip"], 2)
        paid = o["closed"]
        dur = paid - o["opened"]
        od.append([location, o["order_id"], onum, "1", _ts(o["opened"]), o["party"], "", o["server"], table,
                   "Bar" if o["area"] == "Bar" else "Restaurant", o["area"], _service(o["opened"]), o["dining_option"],
                   f"{disc:.2f}", f'{o["subtotal"]:.2f}', f'{o["tax"]:.2f}', f'{o["tip"]:.2f}', "0.00", f"{total:.2f}",
                   "true" if o["voided"] else "false", _ts(paid), _ts(paid), str(dur).split(" ")[-1][:8],
                   "In Store" if o["channel"] != "takeout" else ("Online" if hash(o["order_id"]) % 3 == 0 else "In Store")])
    pd.DataFrame(isd, columns=ISD_COLS).to_csv(f"{out_dir}/ItemSelectionDetails.csv", index=False)
    pd.DataFrame(od, columns=OD_COLS).to_csv(f"{out_dir}/OrderDetails.csv", index=False)
    return len(isd), len(od)
