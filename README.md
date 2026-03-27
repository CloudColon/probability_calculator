# Candidate Joining Likelihood Model

A structured scoring framework for predicting whether a candidate will successfully join after accepting an offer. The model combines five weighted parameter groups — P0 through P4 — each capturing a distinct layer of joining risk.

---

## Table of Contents

- [Overview](#overview)
- [Required Inputs](#required-inputs)
- [P0 — CTC & Hike](#p0--ctc--hike)
- [P1 — Location, Family & Competing Offers](#p1--location-family--competing-offers)
- [P2 — Notice Period, Brand, Work Mode & Partner](#p2--notice-period-brand-work-mode--partner)
- [P3 — Interview Experience, Gap, Career & Motivation](#p3--interview-experience-gap-career--motivation)
- [P4 — Counter-Offer, Warmth & Stability](#p4--counter-offer-warmth--stability)
- [Score Interpretation](#score-interpretation)
- [Data Sources](#data-sources)

---

## Overview

The model scores each candidate on five parameters. Each parameter produces a score from 0–100, which is then combined into an overall joining likelihood signal.

| Priority | Parameter | Focus |
|----------|-----------|-------|
| P0 | CTC & Hike | Financial attractiveness of the offer |
| P1 | Location, Family & Competing Offers | Real-world friction and alternative choices |
| P2 | Notice Period, Brand, Work Mode & Partner | Soft friction during the joining window |
| P3 | Interview Experience, Gap, Career & Motivation | Motivation depth and experiential quality |
| P4 | Counter-Offer, Warmth & Stability | Risk of drop-off despite positive intent |

> P0 is the highest-weight parameter. A strong P0 does not guarantee joining — weak scores on any other parameter can override a good financial offer.

---

## Required Inputs

### Candidate Identification
- Name of candidate

### P0 inputs (2)
- Current CTC (in LPA)
- New CTC being offered (in LPA)

### P1 inputs (5)
- Relocation type — `same_city` / `diff_city_same_state` / `diff_state` / `abroad_with_family` / `abroad_without_family`
- City tier of new location — `1` / `2` / `3`
- Family profile — `single_no_children` / `single_with_children` / `married_no_children` / `married_school_children` / `married_preschool_children` / `married_adult_children`
- Number of competing offers — `0` / `1` / `2` / `3` / `4+`
- Offer strength vs others — `best` / `equal` / `weaker` / `weakest`

### P2 inputs (8)
- Notice period in days
- Buyout situation — `available_willing` / `available_unsure` / `not_available` / `unwilling`
- Current company brand — `top` / `average` / `unknown`
- New company brand — `top` / `average` / `unknown`
- Work mode preference — `prefers_remote` / `prefers_hybrid` / `prefers_office` / `no_preference`
- Work mode offered — `full_remote` / `hybrid` / `full_office` / `flexible`
- Partner profile — `not_applicable` / `not_employed` / `employed_jobs_available` / `employed_niche_role` / `employed_no_jobs` / `self_employed`
- Relocation type (reuse from P1)

### P3 inputs (8)
- Candidate interview self-rating — `1` to `5`
- Recruiter observations on 4 dimensions (each `low` / `medium` / `high`): engagement level, process speed & organisation, post-interview responsiveness, interviewer quality perceived by candidate
- Offer-to-joining gap in days
- Engagement level during gap — `strong` / `moderate` / `minimal` / `none`
- Career move type — `clear_promotion` / `stretch_role` / `lateral_move`
- Goal alignment — `perfect_match` / `partial_match` / `indifferent` / `does_not_match` / `compromise`
- Push factor — `toxic_environment` / `no_growth` / `company_instability` / `compensation_below_market` / `role_changed_against_will` / `personal_relocation` / `no_push`
- Pull factor — `dream_company` / `career_step_up` / `domain_passion` / `better_ctc` / `better_wlb` / `referred_by_network` / `no_pull`

### P4 inputs (7)
- Current company type — `top_brand` / `mid_size` / `early_startup` / `small_business`
- Seniority level — `csuite_vp_director` / `senior_manager_lead` / `manager_senior_ic` / `mid_level_ic` / `junior_entry`
- Tenure at current company in years
- Recruiter warmth self-rating — `1` to `5`
- Warmth boosters applicable (list, can be empty) — `referred_someone` / `shared_personal_news` / `asked_joining_advice` / `formalities_ahead_of_schedule` / `prior_placement`
- Average tenure per company across career in years
- Stability context modifiers applicable (list, can be empty) — `startups_shut_down` / `contract_roles` / `early_career_only` / `recent_trend_stable` / `multiple_offer_drops` / `left_within_3_months` / `current_role_5_plus_yrs`

---

## P0 — CTC & Hike

**Formula:** `Hike % = ((New CTC − Current CTC) / Current CTC) × 100`

P0 score is determined by two factors: the candidate's current CTC slab and the hike percentage offered. As current CTC increases, a lower hike percentage is needed to score maximum points.

### Scoring Matrix

| Current CTC Slab | Min. Hike for 100 pts | Hike % | Score |
|---|---|---|---|
| Below 6 LPA | ≥ 100% | ≥ 100% | 100 |
| | | 80–99% | 90 |
| | | 60–79% | 80 |
| | | 40–59% | 65 |
| | | 20–39% | 50 |
| | | 10–19% | 35 |
| | | < 10% | 20 |
| 6–10 LPA | ≥ 80% | ≥ 80% | 100 |
| | | 60–79% | 90 |
| | | 50–59% | 80 |
| | | 35–49% | 65 |
| | | 20–34% | 50 |
| | | 10–19% | 35 |
| | | < 10% | 20 |
| 10–15 LPA | ≥ 70% | ≥ 70% | 100 |
| | | 55–69% | 90 |
| | | 40–54% | 80 |
| | | 30–39% | 65 |
| | | 20–29% | 50 |
| | | 10–19% | 35 |
| | | < 10% | 20 |
| 15–20 LPA | ≥ 60% | ≥ 60% | 100 |
| | | 50–59% | 90 |
| | | 40–49% | 80 |
| | | 30–39% | 65 |
| | | 20–29% | 50 |
| | | 10–19% | 35 |
| | | < 10% | 20 |
| 20–30 LPA | ≥ 50% | ≥ 50% | 100 |
| | | 40–49% | 90 |
| | | 30–39% | 80 |
| | | 25–29% | 70 |
| | | 15–24% | 55 |
| | | 10–14% | 40 |
| | | < 10% | 20 |
| 30–40 LPA | ≥ 40% | ≥ 40% | 100 |
| | | 35–39% | 90 |
| | | 30–34% | 80 |
| | | 20–29% | 70 |
| | | 15–19% | 55 |
| | | 10–14% | 40 |
| | | < 10% | 20 |
| 40–50 LPA | ≥ 35% | ≥ 35% | 100 |
| | | 30–34% | 90 |
| | | 25–29% | 80 |
| | | 20–24% | 70 |
| | | 15–19% | 55 |
| | | 10–14% | 40 |
| | | < 10% | 20 |
| 50–60 LPA | ≥ 30% | ≥ 30% | 100 |
| | | 25–29% | 90 |
| | | 20–24% | 80 |
| | | 15–19% | 70 |
| | | 10–14% | 55 |
| | | 5–9% | 35 |
| | | < 5% | 15 |
| Above 60 LPA | ≥ 30% | ≥ 30% | 100 |
| | | 25–29% | 90 |
| | | 20–24% | 80 |
| | | 15–19% | 70 |
| | | 10–14% | 55 |
| | | 5–9% | 35 |
| | | < 5% | 15 |

> Scores below 35 on P0 are strong early indicators of drop-off risk and should trigger proactive engagement or re-evaluation of the offer.

---

## P1 — Location, Family & Competing Offers

**Formula:** `P1 = [(Location Base + Family Modifier) × 0.40] + [(Offers Base + Offer Strength Modifier) × 0.35]` — floor: 10

| Sub-Parameter | Weight |
|---|---|
| Location Base Score (A) | 40% |
| Family / Marital Modifier (B) | 25% |
| Competing Offers Score (C) | 35% |

### A — Location Scoring Matrix

| Relocation Scenario | Tier 1 City | Tier 2 City | Tier 3 City |
|---|---|---|---|
| Same City | 100 | 100 | 100 |
| Different City, Same State | 75 | 85 | 90 |
| Different State | 55 | 70 | 80 |
| Abroad (with family) | 35 | 50 | 60 |
| Abroad (without family) | 60 | 70 | 75 |

**City tier reference:**

| Tier | Cities |
|---|---|
| Tier 1 | Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Pune |
| Tier 2 | Kolkata, Ahmedabad, Kochi, Chandigarh, Jaipur, Surat, Vadodara, Indore, Coimbatore |
| Tier 3 | All other cities, small towns, semi-urban locations |

### B — Family Modifier

Applied on top of Location Base. Modifier is 0 for same-city roles regardless of family status.

| Family Profile | Same City | Diff City/State | Abroad |
|---|---|---|---|
| Single, no children | 0 | 0 | 0 |
| Single, has children | -5 | -10 | -20 |
| Married, no children | 0 | -5 | -10 |
| Married, school-age children | -5 | -20 | -35 |
| Married, pre-school children | 0 | -10 | -20 |
| Married, adult/independent children | 0 | -5 | -10 |

> Final Location Sub-Score = Location Base + Family Modifier (minimum: 10)

### C — Competing Offers

**Base score:**

| Competing Offers | Base Score |
|---|---|
| 0 (only this offer) | 100 |
| 1 | 80 |
| 2 | 60 |
| 3 | 40 |
| 4+ | 20 |

**Offer strength modifier:** Adjusted Score = Base + Modifier (minimum: 10)

| Offer Strength | Modifier |
|---|---|
| Clearly the best (highest CTC + best role) | +15 |
| Roughly equal to others | 0 |
| Weaker than at least one other | -15 |
| Weakest among all offers | -25 |

---

## P2 — Notice Period, Brand, Work Mode & Partner

**Formula:** `P2 = (Notice Score × 0.35) + (Brand Score × 0.30) + (Work Mode Score × 0.20) + (Partner Modifier × 0.15)` — floor: 10

| Sub-Parameter | Weight |
|---|---|
| Notice Period Score (A) | 35% |
| Company Brand Score (B) | 30% |
| Work Mode Match Score (C) | 20% |
| Partner Employment Modifier (D) | 15% |

### A — Notice Period

**Base score:**

| Notice Period | Score |
|---|---|
| Immediate / no notice | 100 |
| Up to 15 days | 95 |
| 15–30 days | 85 |
| 30–45 days | 70 |
| 45–60 days | 55 |
| 60–90 days | 35 |
| 90+ days | 15 |

**Buyout modifier:** Adjusted Score = Base + Modifier (max: 100, min: 10)

| Buyout Situation | Modifier |
|---|---|
| Available + candidate willing | +20 |
| Available, candidate unsure | +5 |
| Not available | 0 |
| Candidate unwilling to buy out | -10 |

### B — Company Brand

**Formula:** `Brand Score = 60 (base) + Leaving Modifier + Joining Modifier` (minimum: 10)

| Current Company | Modifier |
|---|---|
| Top brand (FAANG, Tier-1 MNC, known unicorn) | -20 |
| Average brand (mid-size known company, Series B+) | 0 |
| Unknown brand (startup, SME, bootstrapped) | +10 |

| New Company | Modifier |
|---|---|
| Top brand | +20 |
| Average brand | 0 |
| Unknown brand | -15 |

### C — Work Mode Match Matrix

| Candidate Preference | Full Remote | Hybrid | Full Office | Flexible |
|---|---|---|---|---|
| Prefers full remote | 100 | 55 | 20 | 80 |
| Prefers hybrid | 65 | 100 | 55 | 90 |
| Prefers full office | 30 | 70 | 100 | 75 |
| No strong preference | 80 | 85 | 80 | 100 |

### D — Partner Employment Modifier

| Partner Profile | Same City | Diff City/State | Abroad |
|---|---|---|---|
| Not applicable (single / no partner) | 0 | 0 | 0 |
| Partner not employed | 0 | -5 | -10 |
| Partner employed, jobs available | 0 | -10 | -20 |
| Partner employed, niche role / few jobs | 0 | -20 | -35 |
| Partner employed, no jobs available | 0 | -30 | -45 |
| Partner self-employed / freelancer | 0 | -10 | -15 |

---

## P3 — Interview Experience, Gap, Career & Motivation

**Formula:** `P3 = (Interview Experience × 0.25) + (Time Gap Score × 0.30) + (Career Growth Score × 0.25) + (Push vs Pull Score × 0.20)` — floor: 10

| Sub-Parameter | Weight |
|---|---|
| Interview Experience Score (A) | 25% |
| Time Gap Score (B) | 30% |
| Career Growth Score (C) | 25% |
| Push vs Pull Score (D) | 20% |

### A — Interview Experience

**Candidate self-rating:**

| Rating | Sub-Score |
|---|---|
| 5 — Excellent | 100 |
| 4 — Good | 80 |
| 3 — Neutral | 60 |
| 2 — Poor | 35 |
| 1 — Very Poor | 15 |

**Recruiter observation score** (average of 4 dimensions, each rated Low / Medium / High):

| Dimension | Low (25) | Medium (60) | High (100) |
|---|---|---|---|
| Engagement level during interviews | Low enthusiasm, short answers | Moderately engaged | Highly engaged, asked deep questions |
| Process speed & organisation | Multiple reschedules, long gaps | One or two minor delays | Smooth and fast |
| Post-interview responsiveness | Slow to respond, missed calls | Normal response time | Prompt, enthusiastic follow-ups |
| Interviewer quality perceived by candidate | Candidate seemed unimpressed | Mixed impression | Candidate explicitly praised interviewers |

**Final score:** `(Candidate Score × 0.5) + (Recruiter Score × 0.5)` — floor: 10

### B — Time Gap (Offer Date to Joining Date)

**Base score:**

| Gap | Score |
|---|---|
| 0–7 days | 100 |
| 1–2 weeks | 90 |
| 2–4 weeks | 80 |
| 1–2 months | 65 |
| 2–3 months | 45 |
| 3–4 months | 25 |
| 4+ months | 10 |

**Engagement modifier:** Adjusted Score = Base + Modifier (max: 100, floor: 10)

| Engagement Level | Modifier |
|---|---|
| Strong (weekly calls, site visits, team intros) | +15 |
| Moderate (bi-weekly check-ins) | +5 |
| Minimal (only joining formalities) | 0 |
| None (candidate feels forgotten) | -20 |

### C — Career Growth

**Move type base score:**

| Move Type | Base Score |
|---|---|
| Clear promotion (title + scope + reporting level up) | 95 |
| Stretch role (same title, larger scope/responsibility) | 80 |
| Lateral move (same level; CTC or brand is the primary driver) | 55 |

**Goal alignment modifier:** Career Growth Score = Move Base + Modifier (max: 100, floor: 10)

| Alignment | Modifier |
|---|---|
| Perfectly matches stated career goal | +15 |
| Partially matches; candidate sees it as a stepping stone | +5 |
| Candidate indifferent — growth not a priority | 0 |
| Does not match stated goal; candidate expected more | -15 |
| Candidate explicitly calls this a compromise | -25 |

### D — Push vs Pull

**Formula:** `Push vs Pull Score = 50 (base) + Push Modifier + Pull Modifier` (max: 100, floor: 10)

**Push factors:**

| Push Factor | Modifier |
|---|---|
| Toxic environment / bad manager | +20 |
| No growth / career stagnation | +20 |
| Company instability / layoff fears | +15 |
| Compensation below market | +10 |
| Role restructured against candidate's will | +15 |
| Personal relocation driver | +10 |
| No push factor / just exploring | -15 |

**Pull factors:**

| Pull Factor | Modifier |
|---|---|
| Dream company / brand aspiration | +20 |
| Significant career step up | +20 |
| Domain / technology passion | +15 |
| Significantly better CTC | +10 |
| Better work-life balance / work mode | +5 |
| Referred by trusted network | +10 |
| No strong pull / opportunistic | -20 |

---

## P4 — Counter-Offer, Warmth & Stability

**Formula:** `P4 = (Counter-Offer Score × 0.40) + (Warmth Score × 0.35) + (Stability Score × 0.25)` — floor: 10

| Sub-Parameter | Weight |
|---|---|
| Counter-Offer Likelihood Score (A) | 40% |
| Relationship Warmth Score (B) | 35% |
| Candidate Stability Score (C) | 25% |

### A — Counter-Offer Likelihood

**Formula:** `Counter-Offer Score = 80 (base) + Company Modifier + Seniority Modifier + Tenure Modifier` (max: 100, floor: 10)

**Company type modifier:**

| Company Type | Modifier |
|---|---|
| Top brand / large MNC / FAANG | -25 |
| Mid-size known company (Series B–D+) | -15 |
| Early-stage startup (Seed–Series A) | 0 |
| Small business / bootstrapped | +5 |

**Seniority modifier:**

| Seniority | Modifier |
|---|---|
| C-Suite / VP / Director | -20 |
| Senior Manager / Lead (8–15 yrs) | -15 |
| Manager / Senior IC (5–8 yrs) | -10 |
| Mid-level IC (3–5 yrs) | -5 |
| Junior / Entry level (0–3 yrs) | 0 |

**Tenure modifier:**

| Tenure at Current Company | Modifier |
|---|---|
| 7+ years | -15 |
| 4–7 years | -10 |
| 2–4 years | -5 |
| 1–2 years | 0 |
| Less than 1 year | +5 |

> A lower counter-offer score means higher counter-offer risk. Score of 20–30 = extreme risk; prepare a proactive close strategy.

### B — Relationship Warmth

**Recruiter self-rating:**

| Rating | Score |
|---|---|
| 5 — Very strong bond (trusted advisor, shares personal context) | 100 |
| 4 — Good rapport (proactive updates, warm tone) | 80 |
| 3 — Professional but neutral (transactional, responsive) | 60 |
| 2 — Distant / formal (slow to respond, minimal communication) | 35 |
| 1 — Cold / disengaged (missed calls, short answers) | 15 |

**Booster modifiers:** Adjusted Score = Base + Sum of applicable boosters (max: 100)

| Booster | Modifier |
|---|---|
| Candidate referred someone else to recruiter | +10 |
| Candidate shared personal news (family, life events) | +5 |
| Candidate asked recruiter for joining advice | +5 |
| Candidate completed all formalities ahead of schedule | +5 |
| Prior successful placement with same recruiter | +10 |

### C — Candidate Stability

**Average tenure per company base score:**

| Average Tenure per Company | Base Score |
|---|---|
| 4+ years | 100 |
| 3–4 years | 85 |
| 2–3 years | 65 |
| 1–2 years | 40 |
| Less than 1 year | 20 |

**Context modifiers:** Stability Score = Tenure Base + Sum of modifiers (max: 100, floor: 10)

| Context | Modifier |
|---|---|
| All short stints were startups that shut down / pivoted | +15 |
| Candidate was on contract / project-based roles | +15 |
| Short stints were early career (first 1–2 jobs only) | +10 |
| Mix of short and long stints — recent trend is stable | +10 |
| Multiple offer drops or no-shows on record | -20 |
| Left multiple companies within 3 months of joining | -15 |
| In current role 5+ yrs but avg tenure is otherwise low | +5 |

---

## Score Interpretation

The same band applies to all five parameters:

| Score Range | Joining Likelihood |
|---|---|
| 90–100 | Very High |
| 70–89 | High |
| 50–69 | Moderate |
| 20–49 | Low |
| < 20 | Very Low |

---

## Data Sources

| Data | Where to Get It |
|---|---|
| CTC, notice period, tenure | Resume + offer letter |
| Relocation, family, partner | Screening call |
| Competing offers, offer strength | Offer discussion call |
| Brand, work mode, seniority | Resume + JD |
| Push / pull factor | Offer discussion call |
| Interview self-rating | Post-process feedback form |
| Recruiter observations, warmth | Recruiter fills after each touchpoint |

---

## Usage Notes

- **P1, P2, P4 minimum floor is 10.** No parameter scores zero — there is always some base probability.
- **Reassess P1 every 2 weeks** during the offer-to-joining window. Competing offers and family decisions can change rapidly.
- **P2 should be reassessed at every check-in call** during the notice period.
- **P4 should be reassessed at offer release and 2 weeks before the joining date.**
- If `model_default_escaped` is a concern in any evaluation, the competing offers data should be validated through recruiter conversation notes — not assumed. If unknown, default to 1 competing offer.
- A candidate with P0 ≥ 90 but P4 < 30 is still high risk. Strong intent does not eliminate execution risk.
- Recruiter warmth (P4-B) is the most actionable dimension in the entire model — it can be improved significantly within two weeks through deliberate engagement.