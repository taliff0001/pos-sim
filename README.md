# pos-sim

Generates a plausible point-of-sale export for a fictional restaurant, with a **sealed answer key**, so an analysis method can be tested blind before a real restaurant's data goes through it.

- **The numbers come from code.** Every effect (weekday pattern, seasonality, rain, snow, holidays, festivals, games) is drawn from published ranges in [`restaurant-weather-demo/research/effect-sizes.md`](https://github.com/taliff0001/restaurant-weather-demo/blob/main/research/effect-sizes.md); some optional effects are switched off at random. The weather (KROA) and the event calendar are real.
- **The restaurant's shape is hidden**: hours profile, patio or not, bar or not. The analyst works it out from the timestamps.
- **Wildcards** come from a fixed catalog (closure, equipment failure, private party, price increase, renamed dish, brunch trial, street construction, one huge day, staff shortage); the code picks dates and magnitudes.
- **Not built yet: an optional LLM "flavor" layer.** The plan is for it to invent the restaurant (name, menu, prices inside per-category ranges, server names) and a one-line story for each wildcard, as schema-validated JSON, never touching a number. For now every run uses the built-in default restaurant, and wildcard stories come from templates. Leave the `llm` setting off; turning it on fails.
- **Same seed and settings, same export**, every time.

```
pos-sim run --seed 42 --format toast --noise 0.10 --effect-jitter 0.3 --zero-chance 0.25 --wildcards 2
pos-sim reveal runs/seed-42        # only after the analysis is written
```

Output: the export files (Toast: `ItemSelectionDetails.csv` + `OrderDetails.csv`), `answer-key.sha256`, and `sealed/` holding the key (`answer-key.md`, `answer-key.json`) and the daily truth.

Levers: `--noise` (day-to-day variation), `--effect-jitter` (how far each effect may land from the research midpoint), `--zero-chance` (probability an optional effect is off this year), `--wildcards` / `--wildcard-intensity`, `--blind-shape`, `--format`, `--start` / `--end`, `--annual-sales`.

Needs the `restaurant-weather-demo` repo next to it (or `POS_SIM_DEMO_DIR`) for the weather and events.
