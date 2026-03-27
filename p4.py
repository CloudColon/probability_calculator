"""
P4 Parameter -- Counter-Offer Likelihood, Relationship Warmth & Candidate Stability
=====================================================================================
Calculates a P4 score (0-100) based on:
  - Counter-offer likelihood (company type + seniority + tenure at current company)
  - Relationship warmth with recruiter (1-5 self-rating + booster modifiers)
  - Candidate stability history (avg tenure base + context modifiers)

Usage (when imported):
    from p4 import calculate_p4, display_p4
    score, breakdown = calculate_p4(
        company_type="top_brand",
        seniority_level="senior_manager",
        current_tenure_years=5,
        warmth_rating=4,
        warmth_boosters=["referred_someone", "prior_placement"],
        avg_tenure_years=3.5,
        stability_modifiers=["recent_trend_stable"]
    )
"""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPANY_TYPES = [
    "top_brand",       # Top Brand / Large MNC / FAANG
    "mid_size",        # Mid-size known company (Series B-D+)
    "early_startup",   # Early-stage startup (Seed-Series A)
    "small_business",  # Small business / bootstrapped firm
]

SENIORITY_LEVELS = [
    "csuite_vp_director",      # C-Suite / VP / Director
    "senior_manager_lead",     # Senior Manager / Lead (8-15 yrs)
    "manager_senior_ic",       # Manager / Senior IC (5-8 yrs)
    "mid_level_ic",            # Mid-level IC (3-5 yrs)
    "junior_entry",            # Junior / Entry level (0-3 yrs)
]

# Valid warmth booster keys
WARMTH_BOOSTERS_VALID = [
    "referred_someone",        # Candidate proactively referred someone else
    "shared_personal_news",    # Candidate shared personal news (family, life events)
    "asked_joining_advice",    # Candidate asked recruiter for joining advice / tips
    "formalities_ahead_of_schedule",  # Candidate completed all formalities ahead of schedule
    "prior_placement",         # Candidate has worked with recruiter on a previous offer
]

# Valid stability context modifier keys
STABILITY_MODIFIERS_VALID = [
    "startups_shut_down",      # All short stints were at startups that shut down / pivoted
    "contract_roles",          # Candidate was on contract / project-based roles
    "early_career_only",       # Short stints were early career (first 1-2 jobs only)
    "recent_trend_stable",     # Mix of short and long stints -- recent trend is stable
    "multiple_offer_drops",    # Multiple offer drops or no-shows on record
    "left_within_3_months",    # Left multiple companies within 3 months of joining
    "current_role_5_plus_yrs", # Has been in current role 5+ yrs but avg tenure is low
]


# ---------------------------------------------------------------------------
# Section A -- Counter-Offer Likelihood
# Base = 80, apply three modifiers, clamp to 10-100
# ---------------------------------------------------------------------------

COUNTER_OFFER_BASE = 80

COMPANY_TYPE_MODIFIER = {
    "top_brand"     : -25,
    "mid_size"      : -15,
    "early_startup" :   0,
    "small_business":  +5,
}

SENIORITY_MODIFIER = {
    "csuite_vp_director"  : -20,
    "senior_manager_lead" : -15,
    "manager_senior_ic"   : -10,
    "mid_level_ic"        :  -5,
    "junior_entry"        :   0,
}

def _tenure_modifier(current_tenure_years):
    """Map current company tenure in years to modifier."""
    if current_tenure_years >= 7:
        return -15
    elif current_tenure_years >= 4:
        return -10
    elif current_tenure_years >= 2:
        return -5
    elif current_tenure_years >= 1:
        return 0
    else:
        return +5


# ---------------------------------------------------------------------------
# Section B -- Relationship Warmth
# Recruiter self-rating 1-5 -> base score, then add booster modifiers
# ---------------------------------------------------------------------------

WARMTH_RATING_SCORE = {
    5: 100,
    4:  80,
    3:  60,
    2:  35,
    1:  15,
}

WARMTH_BOOSTER_MODIFIER = {
    "referred_someone"           : +10,
    "shared_personal_news"       :  +5,
    "asked_joining_advice"       :  +5,
    "formalities_ahead_of_schedule": +5,
    "prior_placement"            : +10,
}


# ---------------------------------------------------------------------------
# Section C -- Candidate Stability History
# Avg tenure base score + sum of context modifiers, clamped to 10-100
# ---------------------------------------------------------------------------

def _avg_tenure_base(avg_tenure_years):
    """Map average tenure per company (years) to base score."""
    if avg_tenure_years >= 4:
        return 100
    elif avg_tenure_years >= 3:
        return 85
    elif avg_tenure_years >= 2:
        return 65
    elif avg_tenure_years >= 1:
        return 40
    else:
        return 20


STABILITY_CONTEXT_MODIFIER = {
    "startups_shut_down"       : +15,
    "contract_roles"           : +15,
    "early_career_only"        : +10,
    "recent_trend_stable"      : +10,
    "multiple_offer_drops"     : -20,
    "left_within_3_months"     : -15,
    "current_role_5_plus_yrs"  :  +5,
}


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _clamp(value, lo=10, hi=100):
    return max(lo, min(hi, value))


def _validate_inputs(company_type, seniority_level, current_tenure_years,
                     warmth_rating, warmth_boosters,
                     avg_tenure_years, stability_modifiers):

    if company_type not in COMPANY_TYPES:
        raise ValueError("company_type must be one of: {}".format(COMPANY_TYPES))

    if seniority_level not in SENIORITY_LEVELS:
        raise ValueError("seniority_level must be one of: {}".format(SENIORITY_LEVELS))

    if not isinstance(current_tenure_years, (int, float)) or current_tenure_years < 0:
        raise ValueError("current_tenure_years must be a non-negative number")

    if warmth_rating not in WARMTH_RATING_SCORE:
        raise ValueError("warmth_rating must be 1, 2, 3, 4, or 5")

    if not isinstance(warmth_boosters, list):
        raise ValueError("warmth_boosters must be a list (use [] if none)")
    for b in warmth_boosters:
        if b not in WARMTH_BOOSTERS_VALID:
            raise ValueError("warmth_boosters item '{}' must be one of: {}".format(
                b, WARMTH_BOOSTERS_VALID))

    if not isinstance(avg_tenure_years, (int, float)) or avg_tenure_years < 0:
        raise ValueError("avg_tenure_years must be a non-negative number")

    if not isinstance(stability_modifiers, list):
        raise ValueError("stability_modifiers must be a list (use [] if none)")
    for m in stability_modifiers:
        if m not in STABILITY_MODIFIERS_VALID:
            raise ValueError("stability_modifiers item '{}' must be one of: {}".format(
                m, STABILITY_MODIFIERS_VALID))


# ---------------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------------

def calculate_p4(company_type, seniority_level, current_tenure_years,
                 warmth_rating, warmth_boosters,
                 avg_tenure_years, stability_modifiers):
    """
    Calculate P4 score.

    Parameters
    ----------
    company_type           : str        -- one of COMPANY_TYPES
    seniority_level        : str        -- one of SENIORITY_LEVELS
    current_tenure_years   : float      -- years at current company
    warmth_rating          : int        -- recruiter self-rating 1 to 5
    warmth_boosters        : list[str]  -- list of applicable WARMTH_BOOSTERS_VALID keys
                                          (pass [] if none)
    avg_tenure_years       : float      -- average tenure per company across career
    stability_modifiers    : list[str]  -- list of applicable STABILITY_MODIFIERS_VALID keys
                                          (pass [] if none)

    Returns
    -------
    score     : int   -- P4 score (0-100)
    breakdown : dict  -- full calculation details
    """
    _validate_inputs(company_type, seniority_level, current_tenure_years,
                     warmth_rating, warmth_boosters,
                     avg_tenure_years, stability_modifiers)

    # --- Section A: Counter-offer likelihood
    company_mod         = COMPANY_TYPE_MODIFIER[company_type]
    seniority_mod       = SENIORITY_MODIFIER[seniority_level]
    tenure_mod          = _tenure_modifier(current_tenure_years)
    counter_offer_score = _clamp(
        COUNTER_OFFER_BASE + company_mod + seniority_mod + tenure_mod)

    # --- Section B: Relationship warmth
    warmth_base         = WARMTH_RATING_SCORE[warmth_rating]
    booster_total       = sum(WARMTH_BOOSTER_MODIFIER[b] for b in warmth_boosters)
    warmth_score        = _clamp(warmth_base + booster_total)

    # --- Section C: Candidate stability
    tenure_base         = _avg_tenure_base(avg_tenure_years)
    context_total       = sum(STABILITY_CONTEXT_MODIFIER[m] for m in stability_modifiers)
    stability_score     = _clamp(tenure_base + context_total)

    # --- P4 composite
    # Weights: Counter-offer 40%, Warmth 35%, Stability 25%
    p4_raw   = (counter_offer_score * 0.40) + \
               (warmth_score        * 0.35) + \
               (stability_score     * 0.25)
    p4_score = _clamp(round(p4_raw))

    breakdown = {
        "parameter"              : "P4 -- Counter-Offer, Relationship Warmth & Stability",
        # inputs
        "company_type"           : company_type,
        "seniority_level"        : seniority_level,
        "current_tenure_years"   : current_tenure_years,
        "warmth_rating"          : warmth_rating,
        "warmth_boosters"        : warmth_boosters,
        "avg_tenure_years"       : avg_tenure_years,
        "stability_modifiers"    : stability_modifiers,
        # section A
        "company_modifier"       : company_mod,
        "seniority_modifier"     : seniority_mod,
        "tenure_modifier"        : tenure_mod,
        "counter_offer_score"    : counter_offer_score,
        # section B
        "warmth_base_score"      : warmth_base,
        "booster_total"          : booster_total,
        "warmth_score"           : warmth_score,
        # section C
        "avg_tenure_base_score"  : tenure_base,
        "context_total"          : context_total,
        "stability_score"        : stability_score,
        # final
        "p4_score"               : p4_score,
    }

    return p4_score, breakdown


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_p4(breakdown):
    """Pretty-print the P4 breakdown."""
    print("\n" + "=" * 55)
    print("  P4 SCORE -- Counter-Offer, Warmth & Stability")
    print("=" * 55)
    print("  Company Type       : {}".format(breakdown["company_type"]))
    print("  Seniority Level    : {}".format(breakdown["seniority_level"]))
    print("  Current Tenure     : {} yrs".format(breakdown["current_tenure_years"]))
    print("  Warmth Rating      : {} / 5".format(breakdown["warmth_rating"]))
    print("  Warmth Boosters    : {}".format(breakdown["warmth_boosters"] or "none"))
    print("  Avg Tenure         : {} yrs".format(breakdown["avg_tenure_years"]))
    print("  Stability Mods     : {}".format(breakdown["stability_modifiers"] or "none"))
    print("-" * 55)
    print("  Counter-Offer Score: {}  (Base: {}  Co: {}  Sen: {}  Ten: {})".format(
        breakdown["counter_offer_score"],
        COUNTER_OFFER_BASE,
        breakdown["company_modifier"],
        breakdown["seniority_modifier"],
        breakdown["tenure_modifier"]))
    print("  Warmth Score       : {}  (Base: {}  Boosters: {})".format(
        breakdown["warmth_score"],
        breakdown["warmth_base_score"],
        breakdown["booster_total"]))
    print("  Stability Score    : {}  (Base: {}  Context: {})".format(
        breakdown["stability_score"],
        breakdown["avg_tenure_base_score"],
        breakdown["context_total"]))
    print("-" * 55)
    print("  P4 SCORE           : {} / 100".format(breakdown["p4_score"]))
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Quick Test (run directly: python p4.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        # Doc example 1: Top Brand + Director + 8 yrs -> counter = 20
        {
            "company_type"        : "top_brand",
            "seniority_level"     : "csuite_vp_director",
            "current_tenure_years": 8,
            "warmth_rating"       : 2,
            "warmth_boosters"     : [],
            "avg_tenure_years"    : 4.5,
            "stability_modifiers" : [],
            "note"                : "Top Brand + Director + 8 yrs, cold relationship -> expect low",
        },
        # Doc example 5: Small biz + Junior + <1 yr -> counter = 90
        {
            "company_type"        : "small_business",
            "seniority_level"     : "junior_entry",
            "current_tenure_years": 0.5,
            "warmth_rating"       : 5,
            "warmth_boosters"     : ["referred_someone", "prior_placement"],
            "avg_tenure_years"    : 3.5,
            "stability_modifiers" : ["recent_trend_stable"],
            "note"                : "Small biz + Junior + <1yr, strong warmth -> expect high",
        },
        # High instability, no relationship
        {
            "company_type"        : "mid_size",
            "seniority_level"     : "mid_level_ic",
            "current_tenure_years": 1.5,
            "warmth_rating"       : 1,
            "warmth_boosters"     : [],
            "avg_tenure_years"    : 0.8,
            "stability_modifiers" : ["multiple_offer_drops", "left_within_3_months"],
            "note"                : "Mid-size, cold, serial quitter -> expect very low",
        },
        # Moderate -- startup background, good warmth, decent stability
        {
            "company_type"        : "early_startup",
            "seniority_level"     : "manager_senior_ic",
            "current_tenure_years": 3,
            "warmth_rating"       : 4,
            "warmth_boosters"     : ["asked_joining_advice", "shared_personal_news"],
            "avg_tenure_years"    : 2.0,
            "stability_modifiers" : ["startups_shut_down"],
            "note"                : "Startup, good warmth, context explains short stints -> expect moderate-high",
        },
        # Doc example 6: Mid-size + Senior IC + 6 yrs -> counter = 45
        {
            "company_type"        : "mid_size",
            "seniority_level"     : "manager_senior_ic",
            "current_tenure_years": 6,
            "warmth_rating"       : 3,
            "warmth_boosters"     : ["formalities_ahead_of_schedule"],
            "avg_tenure_years"    : 3.2,
            "stability_modifiers" : [],
            "note"                : "Mid-size + Senior IC + 6 yrs, neutral warmth -> expect moderate",
        },
    ]

    for tc in test_cases:
        note = tc.pop("note")
        print("Test: {}".format(note))
        score, breakdown = calculate_p4(**tc)
        display_p4(breakdown)