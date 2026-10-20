"""
Code draws every hidden parameter for a run from the research ranges. Nothing numeric comes
from the LLM. The result is the sealed answer key's numeric half.
"""
from __future__ import annotations
import numpy as np
from .config import RunConfig
from . import research as R
from .profiles import PROFILES
from .wildcards import draw_wildcards


def draw_scenario(cfg: RunConfig, open_days_fn) -> dict:
    rng = np.random.default_rng(cfg.seed)

    if cfg.blind_shape:
        profile = str(rng.choice(list(PROFILES), p=[0.45, 0.2, 0.2, 0.15]))
        patio = bool(rng.random() < 0.6)
        bar = True if profile == "late-bar" else bool(rng.random() < 0.75)
    else:
        profile = cfg.hours_profile or "standard"
        patio = True if cfg.patio is None else cfg.patio
        bar = True if cfg.bar is None else cfg.bar

    effects, zeroed = {}, []
    for key, (lo, hi, optional, basis) in R.EFFECTS.items():
        mid, half = (lo + hi) / 2, (hi - lo) / 2
        v = float(mid + rng.uniform(-1, 1) * half * cfg.effect_jitter)
        if optional and rng.random() < cfg.zero_chance:
            v = 0.0 if key == "patio_bonus" else 1.0
            zeroed.append(key)
        if key == "patio_bonus" and not patio:
            v = 0.0
        if key == "vt_watch" and not bar and key not in zeroed:
            v = 1.0; zeroed.append("vt_watch (no bar)")
        effects[key] = round(v, 4)

    if effects["patio_bonus"] == 0.0:
        patio = False                      # a patio that never earns is, for the data's purposes, no patio

    wd = {k: v * float(rng.uniform(0.92, 1.08)) for k, v in R.WEEKDAY_SHARE.items()}
    for d in PROFILES[profile]["closed_days"]:
        wd[d] = 0.0
    s = sum(wd.values()); wd = {k: round(v / s, 4) for k, v in wd.items()}
    month = {m: round(v * float(rng.uniform(0.97, 1.03)), 3) for m, v in R.MONTH_INDEX.items()}
    takeout_share = round(float(rng.uniform(*R.TAKEOUT_SHARE)), 3)
    alcohol_share = round(float(rng.uniform(*(R.ALCOHOL_SHARE_BAR if bar else R.ALCOHOL_SHARE_BEER_WINE))), 3)

    wild = draw_wildcards(rng, cfg.wildcards, cfg.wildcard_intensity, cfg.start, cfg.end, open_days_fn(profile))

    return dict(seed=cfg.seed, window=[cfg.start, cfg.end], hours_profile=profile, patio=patio, bar=bar,
                annual_sales=cfg.annual_sales, noise=cfg.noise, effects=effects, zeroed=zeroed,
                weekday_share=wd, month_index=month, takeout_share=takeout_share, alcohol_share=alcohol_share,
                storm_2026=R.STORM_2026, wildcards=wild)
