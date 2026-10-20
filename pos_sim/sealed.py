"""
The sealed answer key. answer-key.json is written by code from the scenario (numbers), with a
SHA-256 hash published alongside so the key can be verified later. answer-key.md is a plain-English
rendering (LLM paraphrase when llm=True; a template otherwise).
"""
from __future__ import annotations
import hashlib, json, os
from .research import EFFECTS


def render_story(wc: dict) -> str:
    return wc["story_template"].format(**wc["fill"])


def write_key(sc: dict, rest, cfg, out_dir: str) -> str:
    sealed = os.path.join(out_dir, "sealed")
    os.makedirs(sealed, exist_ok=True)
    key = dict(config=cfg.model_dump(), scenario=sc, restaurant=rest.model_dump())
    for wc in key["scenario"]["wildcards"]:
        wc["story"] = render_story(wc)
    raw = json.dumps(key, indent=1, default=str)
    with open(os.path.join(sealed, "answer-key.json"), "w") as f:
        f.write(raw)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    with open(os.path.join(out_dir, "answer-key.sha256"), "w") as f:
        f.write(digest + "  sealed/answer-key.json\n")

    e = sc["effects"]
    lines = [f"# Answer key: seed {sc['seed']}", "",
             f"**{rest.name}**, {rest.concept}. Hours profile **{sc['hours_profile']}**; patio: **{'yes' if sc['patio'] else 'no'}**; "
             f"bar: **{'yes' if sc['bar'] else 'no'}**. Target net sales ${sc['annual_sales']:,.0f}; day-to-day noise {sc['noise']:.0%}; "
             f"takeout {sc['takeout_share']:.0%} of dollars.", "", "## Effects this year", "",
             "| effect | value | range in research | note |", "|---|---|---|---|"]
    for k, (lo, hi, opt, basis) in EFFECTS.items():
        v = e[k]
        note = "switched off this year" if k in sc["zeroed"] else ("no patio" if k == "patio_bonus" and not sc["patio"] else basis)
        lines.append(f"| {k} | {v} | {lo}–{hi} | {note} |")
    lines += ["", f"Switched off: {', '.join(sc['zeroed']) or 'none'}.", "",
              "The January 24–31, 2026 storm is real and always applied (closed Jan 25–26).", "", "## Wildcards", ""]
    for wc in sc["wildcards"]:
        lines.append(f"- **{wc['type']}** {wc['start']}" + (f" to {wc['end']}" if wc["end"] != wc["start"] else "") +
                     f" (×{wc['mult']} on {wc['touch']}): {wc['story']}")
    lines += ["", "## Weekday share", "", ", ".join(f"{k} {v:.0%}" for k, v in sc["weekday_share"].items()), "",
              "## Month index", "", ", ".join(f"{k}: {v}" for k, v in sc["month_index"].items())]
    with open(os.path.join(sealed, "answer-key.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return digest
