"""pos-sim run | validate | reveal"""
from __future__ import annotations
import argparse, json, os, sys
import pandas as pd
from .config import RunConfig
from .scenario import draw_scenario
from .engine import open_days, simulate
from .menu import DEFAULT, Restaurant
from .calendar import load_weather, load_events
from .sealed import write_key
from .validate import validate_orders
from .writers import toast as toast_writer


def cmd_run(a):
    cfg = RunConfig(**{k: v for k, v in vars(a).items() if k in RunConfig.model_fields and v is not None})
    out = os.path.join(cfg.out_dir, f"seed-{cfg.seed}")
    os.makedirs(out, exist_ok=True)
    sc = draw_scenario(cfg, lambda p: open_days(p, cfg.start, cfg.end))
    rest = DEFAULT
    if cfg.llm:
        from .flavor import invent_restaurant, add_wildcard_stories
        rest = invent_restaurant(cfg, sc) or DEFAULT
        add_wildcard_stories(cfg, sc)
    wx, ev = load_weather(), load_events()
    orders, daily = simulate(cfg, sc, rest, wx, ev)
    names = {it.name for it in rest.items}
    for wc in sc["wildcards"]:
        if wc["type"] == "menu_change" and wc["fill"]["new"]:
            names.add(wc["fill"]["new"])
    problems = validate_orders(orders, sc, names)
    if problems:
        print("VALIDATION FAILED:", *problems[:20], sep="\n  "); sys.exit(1)
    menu_ids = {}
    if cfg.format == "toast":
        n_lines, n_orders = toast_writer.write(orders, out, rest.name, menu_ids)
    else:
        raise SystemExit("square writer: waiting on the real export to match")
    daily.to_csv(os.path.join(out, "sealed", "daily-truth.csv"), index=False) if os.path.isdir(os.path.join(out, "sealed")) else None
    digest = write_key(sc, rest, cfg, out)
    daily.to_csv(os.path.join(out, "sealed", "daily-truth.csv"), index=False)
    with open(os.path.join(out, "README.txt"), "w") as f:
        f.write(f"pos-sim run, seed {cfg.seed}, format {cfg.format}, window {cfg.start} to {cfg.end}.\n"
                f"Export files are in this folder. The answer key is in sealed/ (do not open until the analysis is written);\n"
                f"its SHA-256 is in answer-key.sha256 so it can be verified afterwards.\n")
    print(f"{out}: {n_orders:,} orders, {n_lines:,} item lines, net ${daily.net.sum():,.0f}; key sha256 {digest[:12]}…")


def cmd_reveal(a):
    p = os.path.join(a.run_dir, "sealed", "answer-key.md")
    print(open(p).read())


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pos-sim")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    for name, field in RunConfig.model_fields.items():
        t = field.annotation
        kw = {}
        if t is bool or str(t).startswith("bool"):
            kw = dict(type=lambda s: s.lower() in ("1", "true", "yes"))
        elif t is int:
            kw = dict(type=int)
        elif t is float:
            kw = dict(type=float)
        r.add_argument(f"--{name.replace('_', '-')}", dest=name, default=None, help=field.description or "", **kw)
    r.set_defaults(fn=cmd_run)
    v = sub.add_parser("reveal"); v.add_argument("run_dir"); v.set_defaults(fn=cmd_reveal)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
