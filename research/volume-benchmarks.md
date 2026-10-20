# Volume & shape benchmarks: independent full-service restaurant, mid-cost mid-sized US city (Roanoke, VA class)

Compiled 2026-10-20 for pos-sim generator defaults. Reliability grades: **A** government / peer-reviewed; **B** large POS/platform dataset; **C** trade press, survey, or single case; **D** no published figure, reasoned range. Where a number is derived, the math is shown. Nothing below is invented; gaps are flagged.

## 1. Annual sales

| Figure | Value | Grade | Source |
|---|---|---|---|
| US mean receipts per employer full-service restaurant (NAICS 722511), 2022 Economic Census | $372.8B / 254,201 estabs = **$1.47M** (mean, pulled up by chains) | A (figures) / C (third-party tabulation) | [BusinessNES tabulation of 2022 ECNBASIC](https://businessnes.com/business-data/restaurant/) |
| US FSR establishments (CBP 2023) | 258,626 employer estabs, 21 employees avg | A | [naicscodes.org citing CBP 2023](https://naicscodes.org/code/722511-full-service-restaurants/) |
| US FSR revenue, Service Annual Survey (all employer estabs) | $424.4B (2022) | A | [FRED FRRAEEF2722511](https://fred.stlouisfed.org/data/FRRAEEF2722511) |
| Boulder County CO FSR (only county-level 722511 example Census published in its release) | $556.1M / 345 = $1.61M mean | A | [Census story, Apr 2025](https://census.gov/library/stories/2025/04/economic-census-geographic-stats.html) |
| Virginia, all eating & drinking places (NRA, 2022) | $24.4B / 17,257 locations = **$1.41M** mean (includes QSR and chains) | C (NRA estimate) | [NRA Virginia fact sheet](https://restaurant.org/getmedia/345b93e9-cc0b-40fe-af72-db94b01a26a2/Virginia.pdf) |
| Roanoke city, accommodation & food services receipts, 2022 Economic Census | **$403.1M** | A | [Census QuickFacts Roanoke city](https://www.census.gov/quickfacts/fact/table/roanokecityvirginia/INC110223) |
| Roanoke city NAICS 72 employer establishments (CBP 2023) | 289 | A (via aggregator) | [mytownview citing CBP](https://mytownview.com/virginia/roanoke-city/roanoke/business/overview) |
| Roanoke derived mean per NAICS 72 establishment | $403.1M / 289 = **$1.39M** (includes hotels, QSR, chains) | derived | above |
| NRA Operations Data Abstract 2025: FSR bands used | "under $2M" vs "$2M+" only; below-$2M FSRs had 33.7% food cost and 1.1% median pre-tax income | C (survey, 900+ operators) | [NRA analysis, Oct 2025](https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/higher-volume-restaurants-reported-lower-food-cost-ratios-in-2024/) |
| Listings proxy (BizBuySell VA, Oct 2026): non-NoVA full-service | Richmond FSR $875–900k revenue; Leesburg FSR+bar $2.1M; Arlington R&B $440k; only Roanoke listing was a froyo shop ($285.7k) | C | [BizBuySell VA restaurants](https://www.bizbuysell.com/virginia/miscellaneous-restaurant-and-bars-for-sale/) |
| Top-100 independents floor | $11M+ (irrelevant tail; "most indie leaders $1–3M") | C | [NRN](https://nrn.com/independent-restaurants/did-your-independent-restaurant-earn-more-than-11-m-last-year-you-could-make-the-top-100-list), [FSR](https://www.fsrmagazine.com/feature/bright-future-ahead-independents/) |

**No published median for independent FSR sales exists** (D). The Census means ($1.4–1.5M) include chains and multi-unit operators, which skew the mean up; the NRA abstract's own split at $2M implies a large share of FSRs sit under $2M. Reasoned range for a single-unit independent FSR in a Roanoke-class market: **$0.6M–$1.8M, central $1.0–1.2M** (D). Note the Census API now requires a key; state-level 722511 receipts were not retrievable without one (data.census.gov table EC2200BASIC, NAICS 722511, geo Virginia, would give it).

## 2. Covers per day / week

| Figure | Value | Grade | Source |
|---|---|---|---|
| Table turns per meal period | Family dining ~3 at dinner; fine dining 1–2 (Toast) / 2–3 (Katalyst); fast casual 3–5; casual dining: no figure | C | [Toast table turnover](https://pos.toasttab.com/blog/on-the-line/table-turnover-rate), [Katalyst](https://www.katalystos.com/blog/the-restaurant-metrics-that-actually-matter) |
| Implied dinner duration | ~1.5–1.7 h per turn (family dinner, 5–10pm, 3 turns) | C | Toast, above |
| Guest patience | 72% of guests will wait no more than 30 min for a table | B | Toast, above |
| Seats per independent FSR | **No published distribution found** (D). Toast's worked example uses 60 seats (15 four-tops). HB 975 uses "<30 table seats / occupancy <60" as its small-venue threshold, which is a useful floor marker. | D | [Toast](https://pos.toasttab.com/blog/on-the-line/table-turnover-rate), [Williams Mullen on HB 975](https://www.williamsmullen.com/insights/news/legal-news/changes-virginias-food-beverage-ratio-set-take-effect-july-1-2026) |
| Published cover counts for mid-sized-city restaurants | None found (D). Roanoke Rambler and WDBJ coverage of downtown restaurants gives menu prices and hours, not seats or covers. | D | [Roanoke Rambler, Aug 2026](https://www.roanokerambler.com/downtown-roanokes-ledger-some-resteruants-open-as-others-close/) |

Derived (D): 80 seats × 70% dinner occupancy × 1.6 turns ≈ 90 dinner covers on a weekday; Saturday at ~2.3 turns ≈ 130 covers. Cross-check against sales: $1.1M/yr ÷ 360 days ÷ ~$38 blended PPA ≈ 80 covers/day average, consistent with the Toast day-of-week skew in section 5.

## 3. Average check per person (PPA) and alcohol share

| Figure | Value | Grade | Source |
|---|---|---|---|
| Valentine's dinner for two, FSR, national (food+drink, pre-tip, pre-tax) | $102 (2023), $107 (2022), $69 (2018) → ~$51/person 2023 | B | [Toast, Mar 2023](https://www.businesswire.com/news/home/20230302005804/en/New-Toast-data-finds-the-Average-Date-Night-at-a-Restaurant-Costs-121-up-more-than-75-in-5-Years) |
| Online/takeout order vs in-store check | +23% larger online (Toast, 2016, all segments) | B (dated) | [Toast, 2016](https://pos.toasttab.com/news/restaurants-online-ordering-23-percent-larger-check-size) |
| Lunch vs dinner PPA, mid-cost market | No published split found (D). Roanoke price points: The Haven apps $10–14, sandwiches $12–16, entrees to $34; Dorothy lunch soup $7.50, dinner sirloin $38. | C (menu prices only) | [Roanoke Rambler](https://www.roanokerambler.com/downtown-roanokes-ledger-some-resteruants-open-as-others-close/) |
| Alcohol share of sales, FSRs that serve alcohol | **21%** average (limited-service with alcohol: 6%) | C (NRA operator survey, n=3,000, Nov–Dec 2022) | [NRA Alcohol Trends PDF](https://go.restaurant.org/rs/078-ZLA-461/images/National-Restaurant-Association-Alcohol-Trends.pdf) |
| Alcohol share, regulatory ceiling (VA mixed-beverage licensees) | Alcohol ≤55% of gross sales (pre-July 2026); tiered after | A | [VA ABC MBAR](https://www.abc.virginia.gov/licenses/retail-resources/mbar) |

Reasoned PPA for Roanoke-class upscale-casual (D): lunch $16–22 (little alcohol), dinner $38–55 food+drink; 2023 national $51/person on a date night supports the upper-middle of that. Alcohol share: 15–25% with a bar (NRA 21% central), 3–8% beer/wine only.

## 4. Tickets vs guests, party size, takeout

| Figure | Value | Grade | Source |
|---|---|---|---|
| Average party size, dine-in FSR | **Not published** by Toast or OpenTable in any release found (D). Toast: solo bookings <1% of reservations (Q3 2025). | D | [Toast solo-diner post](https://pos.toasttab.com/blog/data/solo-diner-reservations-full-service-restaurant-trends) |
| Off-premises share of all restaurant traffic | ~75% (all segments, QSR-dominated) | C (NRA 2025) | [NRA press release, Apr 2025](https://restaurant.org/research-and-media/media/press-releases/from-trend-to-transformation-off-premises-dining-now-essential-for-restaurant-consumers,-operators/) |
| FSR operators reporting larger off-prem share than 2019 | 41% (2025); 43% (2024 SOI) | C | NRA above; [Restaurant Dive](https://www.restaurantdive.com/news/how-off-premise-diner-demand-is-evolving-what-the-data-shows/708564/) |
| Online ordering share of FSR sales | 8–10% (Toast, 2016; pre-pandemic) | B (dated) | [Toast 2016](https://pos.toasttab.com/news/restaurants-online-ordering-23-percent-larger-check-size) |
| Online platform share of business, operators using platforms | ~23% (TouchBistro 2024, all segments) | C | Restaurant Dive, above |
| Takeout check vs dine-in | +23% online vs in-store (Toast 2016); Technomic: 30% of regular takeout users say they buy more when ordering out | B/C | Toast 2016; [Technomic via Meatingplace](https://meatingplace.com/takeout-customers-buy-more-food-than-dine-in-technomic/) |
| Reservation cancellation rate, FSR | 17% (Q3 2024) | B | [Toast Q3 2024](https://pos.toasttab.com/news/2024-reservation-trends) |

Reasoned (D): dine-in party size mean 2.4–2.8 (mode 2, long tail of 4–6); takeout 10–18% of tickets and 8–14% of dollars for a dinner-house independent (takeout tickets are often 1–2 entrees so per-ticket is below a dine-in table but above a dine-in per-person).

## 5. Hourly / daily shape

| Figure | Value | Grade | Source |
|---|---|---|---|
| Reservations by day, FSR (share of week, Q3 2024) | Sat 27%, Fri 21%, Sun 15%, Thu 11%, Wed 10%, Tue 8%, Mon 6% → **Sat/Tue = 3.4×** (reservation volume, not dollars) | B | [Toast Q3 2024](https://pos.toasttab.com/news/2024-reservation-trends) |
| Dining days vs weekly average (Q3 2023) | Sat +85%, Fri +54%, Sun +8%, Thu −12% | B | [Toast Q3 2023](https://pos.toasttab.com/news/full-service-restaurant-reservation-booking-trends) |
| Dinner reservation slot share | 6pm ~27%, 7pm ~25% (Q3 2024); 6pm 37%, 7pm 26%, 5pm 22% (Q3 2023) | B | same two |
| Payment-time peak (17 metros, 4pm–midnight) | 7–8pm ≈ 17% of transactions; 9–10pm peaks only in Miami/SF | B | Toast Q3 2023 |
| Weekday lunch (11–2) share of transactions, all food & drink | 21% (2019) → 18% (2023); weekend (Sat+Sun) 30% → 35%; weekday happy hour 7% → 8% | B (Square) | [Axios on Square, May 2024](https://www.axios.com/2024/05/14/restaurants-eating-out-rates-weekend-weekday) |
| Lunch vs dinner dollar split, FSR dinner house | **No published figure** (D) | D | — |

Reasoned (D): for a dinner-house independent open lunch Tue–Sat, lunch ≈ 25–30% of dollars, dinner 70–75%. Day weights (dollars) Mon 0.6, Tue 0.7, Wed 0.8, Thu 1.0, Fri 1.5, Sat 1.7, Sun 0.9 (Sat/Tue ≈ 2.4× in dollars; walk-ins and lunch flatten the 3.4× reservation ratio). Dinner hourly: ramp from 5pm, peak 6–8pm (~55–60% of dinner tickets), tail to 9–10pm.

## 6. Tips, discounts, voids

| Figure | Value | Grade | Source |
|---|---|---|---|
| FSR card/digital tip %, national | 19.2% (Q3 2025), 19.1% (Q2 2025), 19.4% (Q1 2025 and Q3 2023), 19.6% (Q4 2022); historical high 19.8% (2021) | B | [KTVU on Toast Q3 2025](https://www.ktvu.com/news/states-tipping-toast-report), [LendingTree on Toast Q1 2025](https://www.lendingtree.com/debt-consolidation/tipping-rates-study/), [Toast Q3 2023](https://pos.toasttab.com/news/full-service-restaurant-reservation-booking-trends) |
| FSR tip %, Q1 2025, by state | **VA 19.9%**, NC 19.9%, TN 20.0%, SC 20.7%, KY 20.9% (QSR: VA 15.7%) | B | LendingTree/Toast, above |
| Share of card transactions with a tip | 66.6% (Q3 2023, all segments) | B | Toast Q3 2023 |
| Comps | "typically 3–5% of sales" (unsourced vendor blog) | C- | [Katalyst](https://www.katalystos.com/blog/the-restaurant-metrics-that-actually-matter) |
| Voids | "should stay under 1–2%" (unsourced vendor blog) | C- | Katalyst, above |
| Discounts as % of sales | **No published POS-dataset figure found** (D). Restaurant365 and TouchBistro document the reports but publish no benchmarks. | D | [Restaurant365](https://www.restaurant365.com/blog/how-to-reduce-restaurant-comps-and-voids/) |

## 7. Roanoke-specific

| Figure | Value | Grade | Source |
|---|---|---|---|
| Roanoke city meals tax rate | 5.5% (since FY16); 7% proposed for FY2026 (council debated Apr 2025; +$6M/yr expected) | A | [City FY2026 revenue projections](https://www.roanokeva.gov/DocumentCenter/View/20823/FY2026-Budget-Revenue-Projections-Feb-3-2025-Council), [Cardinal News](https://cardinalnews.org/2025/04/21/city-restaurant-owners-clash-over-proposed-meals-tax-increase/) |
| Meals tax collections | FY2024 actual **$21,662,618**; FY2025 adopted $22.25M; FY2026 projected $22.824M | A | City doc, above |
| Implied taxable prepared-food sales, FY2024 | $21,662,618 / 0.055 = **$393.9M** | derived | — |
| Roanoke city accommodation & food services receipts, 2022 Econ Census | $403.1M (consistent with the meals-tax derivation) | A | [QuickFacts](https://www.census.gov/quickfacts/fact/table/roanokecityvirginia/INC110223) |
| Roanoke city NAICS 72 employer establishments | 289 (CBP 2023) | A via aggregator | [mytownview](https://mytownview.com/virginia/roanoke-city/roanoke/business/overview) |
| Per-establishment mean | $393.9M / 289 = **$1.36M** (all prepared-food sellers incl. QSR chains, hotels, caterers; FSR-only count not retrieved) | derived | — |
| Health-district food permits | 1,072 (2022), Roanoke City & Alleghany Health Districts, 7 jurisdictions, includes non-restaurants | A | [VDH RCAHD](https://www.vdh.virginia.gov/roanoke/2023/02/13/environmental-health-food-program/) |
| Downtown Roanoke restaurant count | Not published by DRI; Restaurant Week 2025 had 30 participants; 3 closures / 3 openings in 18 months to Aug 2026 | C | [WSLS Jan 2025](https://www.wsls.com/news/local/2025/01/17/downtown-roanoke-restaurant-week-returns-with-30-restaurants-ready-to-dish-out), [Roanoke Rambler](https://www.roanokerambler.com/downtown-roanokes-ledger-some-resteruants-open-as-others-close/), [WDBJ Mar 2026](https://www.wdbj7.com/2026/03/06/downtown-roanoke-inc-working-attract-more-restaurants/) |
| Roanoke restaurant revenue or seat counts | None published (D) | D | — |
| VA mixed-beverage food ratio, through 30 Jun 2026 | Food + non-alcoholic bev ≥45% of gross sales; ≥$4,000/mo food prepared & consumed on premises, ≥$2,000 of it from meals with substantial entrees; cocktails-to-go excluded; checked at MBAR | A | [VA ABC MBAR](https://www.abc.virginia.gov/licenses/retail-resources/mbar) |
| VA HB 975, effective 1 Jul 2026 | Tiered by avg monthly food sales: ≥$48k no ratio; $25k–<$48k food ≥30%; $4k–<$25k food ≥45% (30% if <30 table seats and occupancy <60); table seats must ≥ counter seats; ABC reports to GA by 1 Nov 2027 | A (law) / C (law-firm summary) | [Williams Mullen](https://www.williamsmullen.com/insights/news/legal-news/changes-virginias-food-beverage-ratio-set-take-effect-july-1-2026), [JD Supra](https://www.jdsupra.com/legalnews/changes-virginia-s-food-to-beverage-6933652/) |

Implication for the generator: a Roanoke FSR with a bar must keep alcohol ≤55% (≤70% if food ≥$25k/mo, unconstrained if food ≥$48k/mo ≈ $576k/yr). A $1.1M restaurant at 21% alcohol has ~$72k/mo food and is unconstrained under HB 975.

## Recommended generator defaults

| Parameter | Default | Range | Confidence |
|---|---|---|---|
| Annual net sales | $1.1M | $0.6M–$1.8M | Medium (Census means A, independent median D) |
| Seats | 80 | 50–120 | Low (D) |
| Covers, weekday (Tue–Thu) | 85/day (lunch 30, dinner 55) | 50–130 | Low-Medium |
| Covers, Saturday | 150/day (lunch 40, dinner 110) | 100–220 | Low-Medium |
| Day weights (dollars) | Mon .6 Tue .7 Wed .8 Thu 1.0 Fri 1.5 Sat 1.7 Sun .9 | Sat/Tue 2–3.4× | Medium (Toast B for reservations) |
| PPA lunch | $19 | $15–24 | Low-Medium |
| PPA dinner (food+drink, pre-tax/tip) | $46 | $35–60 | Medium (Toast $51 national 2023, B) |
| Dinner-hour ticket shape | 5pm 10%, 6pm 25%, 7pm 28%, 8pm 22%, 9pm 11%, 10pm 4% | — | Medium (Toast B) |
| Lunch share of dollars | 27% | 20–35% | Low (D) |
| Party size, dine-in | mean 2.6; dist 1:6%, 2:45%, 3:16%, 4:22%, 5+:11% | mean 2.3–2.9 | Low (D) |
| Takeout share of tickets / dollars | 15% / 11% | 8–25% / 6–18% | Low-Medium (Toast 8–10% B, dated) |
| Takeout ticket vs dine-in per-person | 1.2× PPA (1–2 entrees per ticket) | — | Low |
| Alcohol share of sales (with bar) | 21% | 15–30% | Medium (NRA C; VA ABC ceiling A) |
| Card tip % (FSR, VA) | 19.9% mean, sd ~4 | 15–25% | High (Toast B, state-level) |
| Share of card tickets tipped | 95% dine-in, 60% takeout | — | Low-Medium (66.6% all-segment B) |
| Comps | 2.5% of gross | 1–5% | Low (C-) |
| Voids | 1.0% of tickets | 0.5–2% | Low (C-) |
| Discounts | 2% of gross | 1–4% | Low (D) |
| Reservation cancellation | 17% | — | Medium (Toast B) |

## Sources

- Census QuickFacts, Roanoke city VA (2022 Econ Census receipts): https://www.census.gov/quickfacts/fact/table/roanokecityvirginia/INC110223
- Census, Economic Census geographic stats story (Boulder County 722511; 772,441 sector-72 estabs): https://census.gov/library/stories/2025/04/economic-census-geographic-stats.html
- FRED, SAS revenue FSR 722511: https://fred.stlouisfed.org/data/FRRAEEF2722511
- BusinessNES tabulation of 2022 ECNBASIC 722511: https://businessnes.com/business-data/restaurant/
- naicscodes.org, CBP 2023 722511: https://naicscodes.org/code/722511-full-service-restaurants/
- mytownview, CBP 2023 Roanoke city: https://mytownview.com/virginia/roanoke-city/roanoke/business/overview
- NRA Virginia fact sheet: https://restaurant.org/getmedia/345b93e9-cc0b-40fe-af72-db94b01a26a2/Virginia.pdf
- NRA, higher-volume restaurants food cost (2025 Ops Data Abstract): https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/higher-volume-restaurants-reported-lower-food-cost-ratios-in-2024/
- NRA 2025 Ops Data Abstract release: https://restaurant.org/research-and-media/media/press-releases/new-resource-from-national-restaurant-association-provides-insights-into-operational-realities/
- NRA Alcohol Trends (21% alcohol share): https://go.restaurant.org/rs/078-ZLA-461/images/National-Restaurant-Association-Alcohol-Trends.pdf
- NRA off-premises 2025 release: https://restaurant.org/research-and-media/media/press-releases/from-trend-to-transformation-off-premises-dining-now-essential-for-restaurant-consumers,-operators/
- Restaurant Dive, off-premise data roundup: https://www.restaurantdive.com/news/how-off-premise-diner-demand-is-evolving-what-the-data-shows/708564/
- Toast Q3 2024 reservation trends: https://pos.toasttab.com/news/2024-reservation-trends
- Toast Q3 2023 reservation/booking trends: https://pos.toasttab.com/news/full-service-restaurant-reservation-booking-trends
- Toast solo-diner (Q3 2025): https://pos.toasttab.com/blog/data/solo-diner-reservations-full-service-restaurant-trends
- Toast date-night check (Q4 2022): https://www.businesswire.com/news/home/20230302005804/en/New-Toast-data-finds-the-Average-Date-Night-at-a-Restaurant-Costs-121-up-more-than-75-in-5-Years
- Toast online ordering +23% (2016): https://pos.toasttab.com/news/restaurants-online-ordering-23-percent-larger-check-size
- Toast table turnover: https://pos.toasttab.com/blog/on-the-line/table-turnover-rate
- LendingTree on Toast Q1 2025 tips by state: https://www.lendingtree.com/debt-consolidation/tipping-rates-study/
- KTVU on Toast Q3 2025 tips: https://www.ktvu.com/news/states-tipping-toast-report
- Axios on Square weekday/weekend shift: https://www.axios.com/2024/05/14/restaurants-eating-out-rates-weekend-weekday
- Technomic via Meatingplace, takeout order size: https://meatingplace.com/takeout-customers-buy-more-food-than-dine-in-technomic/
- Katalyst comps/voids/turns (unsourced): https://www.katalystos.com/blog/the-restaurant-metrics-that-actually-matter
- Restaurant365 comps & voids: https://www.restaurant365.com/blog/how-to-reduce-restaurant-comps-and-voids/
- BizBuySell Virginia restaurant listings: https://www.bizbuysell.com/virginia/miscellaneous-restaurant-and-bars-for-sale/
- Sunbelt Roanoke/Lynchburg listings: https://www.sunbeltnetwork.com/roanoke-va/buy-a-business/listings/i-restaurants-food-for-sale-14/
- City of Roanoke FY2026 revenue projections: https://www.roanokeva.gov/DocumentCenter/View/20823/FY2026-Budget-Revenue-Projections-Feb-3-2025-Council
- Cardinal News, meals tax debate: https://cardinalnews.org/2025/04/21/city-restaurant-owners-clash-over-proposed-meals-tax-increase/
- VDH RCAHD food program (1,072 permits): https://www.vdh.virginia.gov/roanoke/2023/02/13/environmental-health-food-program/
- WSLS, Restaurant Week 2025 (30 restaurants): https://www.wsls.com/news/local/2025/01/17/downtown-roanoke-restaurant-week-returns-with-30-restaurants-ready-to-dish-out
- Roanoke Rambler, downtown restaurant ledger: https://www.roanokerambler.com/downtown-roanokes-ledger-some-resteruants-open-as-others-close/
- WDBJ, DRI attracting restaurants: https://www.wdbj7.com/2026/03/06/downtown-roanoke-inc-working-attract-more-restaurants/
- VA ABC MBAR page: https://www.abc.virginia.gov/licenses/retail-resources/mbar
- Williams Mullen on HB 975: https://www.williamsmullen.com/insights/news/legal-news/changes-virginias-food-beverage-ratio-set-take-effect-july-1-2026
- JD Supra on HB 975: https://www.jdsupra.com/legalnews/changes-virginia-s-food-to-beverage-6933652/
