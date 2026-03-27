"""
P2 Parameter -- Notice Period, Company Brand, Work Mode & Partner Employment
=============================================================================
Calculates a P2 score (0-100) based on:
  - Notice period length + buyout situation
  - Current company brand + new company brand
  - Work mode preference vs offer
  - Partner employment status + relocation impact

Usage (when imported):
    from p2 import calculate_p2, display_p2
    score, breakdown = calculate_p2(
        notice_period_days=60,
        buyout_situation="not_available",
        current_brand="top",
        new_brand="average",
        work_mode_preference="hybrid",
        work_mode_offered="full_office",
        partner_profile="employed_jobs_available",
        relocation_type="diff_state"
    )
"""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BUYOUT_SITUATIONS = [
    "available_willing",
    "available_unsure",
    "not_available",
    "unwilling",
]

BRAND_TIERS = ["top", "average", "unknown"]

WORK_MODE_OPTIONS = [
    "full_remote",
    "hybrid",
    "full_office",
    "flexible",
]

WORK_MODE_PREFERENCES = [
    "prefers_remote",
    "prefers_hybrid",
    "prefers_office",
    "no_preference",
]

PARTNER_PROFILES = [
    "not_applicable",
    "not_employed",
    "employed_jobs_available",
    "employed_niche_role",
    "employed_no_jobs",
    "self_employed",
]

RELOCATION_TYPES = [
    "same_city",
    "diff_city_same_state",
    "diff_state",
    "abroad_with_family",
    "abroad_without_family",
]


# ---------------------------------------------------------------------------
# Section A -- Notice Period
# ---------------------------------------------------------------------------

def _notice_base_score(notice_period_days):
    """Map notice period in days to a base score."""
    if notice_period_days == 0:
        return 100
    elif notice_period_days <= 15:
        return 95
    elif notice_period_days <= 30:
        return 85
    elif notice_period_days <= 45:
        return 70
    elif notice_period_days <= 60:
        return 55
    elif notice_period_days <= 90:
        return 35
    else:
        return 15


BUYOUT_MODIFIER = {
    "available_willing": +20,
    "available_unsure" :  +5,
    "not_available"    :   0,
    "unwilling"        : -10,
}


# ---------------------------------------------------------------------------
# Section B -- Company Brand
# Base = 60, then apply leaving modifier + joining modifier
# ---------------------------------------------------------------------------

# Leaving current company -- how hard is it to leave?
LEAVING_BRAND_MODIFIER = {
    "top"    : -20,
    "average":   0,
    "unknown": +10,
}

# Joining new company -- how attractive is the destination?
JOINING_BRAND_MODIFIER = {
    "top"    : +20,
    "average":   0,
    "unknown": -15,
}

BRAND_BASE = 60


# ---------------------------------------------------------------------------
# Section C -- Work Mode Match
# Rows = preference, Cols = offered mode
# ---------------------------------------------------------------------------

WORK_MODE_SCORES = {
    "prefers_remote" : {"full_remote": 100, "hybrid": 55, "full_office": 20, "flexible": 80},
    "prefers_hybrid" : {"full_remote":  65, "hybrid":100, "full_office": 55, "flexible": 90},
    "prefers_office" : {"full_remote":  30, "hybrid": 70, "full_office":100, "flexible": 75},
    "no_preference"  : {"full_remote":  80, "hybrid": 85, "full_office": 80, "flexible":100},
}


# ---------------------------------------------------------------------------
# Section D -- Partner Employment Modifier
# Applied based on partner profile + relocation bucket
# ---------------------------------------------------------------------------

def _relocation_bucket(relocation_type):
    if relocation_type == "same_city":
        return "same_city"
    elif relocation_type in ("diff_city_same_state", "diff_state"):
        return "diff_city_or_state"
    else:
        return "abroad"


PARTNER_MODIFIERS = {
    "not_applicable"        : {"same_city":  0, "diff_city_or_state":   0, "abroad":   0},
    "not_employed"          : {"same_city":  0, "diff_city_or_state":  -5, "abroad": -10},
    "employed_jobs_available": {"same_city": 0, "diff_city_or_state": -10, "abroad": -20},
    "employed_niche_role"   : {"same_city":  0, "diff_city_or_state": -20, "abroad": -35},
    "employed_no_jobs"      : {"same_city":  0, "diff_city_or_state": -30, "abroad": -45},
    "self_employed"         : {"same_city":  0, "diff_city_or_state": -10, "abroad": -15},
}


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _clamp(value, lo=10, hi=100):
    return max(lo, min(hi, value))


def _validate_inputs(notice_period_days, buyout_situation, current_brand,
                     new_brand, work_mode_preference, work_mode_offered,
                     partner_profile, relocation_type):
    if not isinstance(notice_period_days, (int, float)) or notice_period_days < 0:
        raise ValueError("notice_period_days must be a non-negative number")
    if buyout_situation not in BUYOUT_SITUATIONS:
        raise ValueError("buyout_situation must be one of: {}".format(BUYOUT_SITUATIONS))
    if current_brand not in BRAND_TIERS:
        raise ValueError("current_brand must be one of: {}".format(BRAND_TIERS))
    if new_brand not in BRAND_TIERS:
        raise ValueError("new_brand must be one of: {}".format(BRAND_TIERS))
    if work_mode_preference not in WORK_MODE_PREFERENCES:
        raise ValueError("work_mode_preference must be one of: {}".format(WORK_MODE_PREFERENCES))
    if work_mode_offered not in WORK_MODE_OPTIONS:
        raise ValueError("work_mode_offered must be one of: {}".format(WORK_MODE_OPTIONS))
    if partner_profile not in PARTNER_PROFILES:
        raise ValueError("partner_profile must be one of: {}".format(PARTNER_PROFILES))
    if relocation_type not in RELOCATION_TYPES:
        raise ValueError("relocation_type must be one of: {}".format(RELOCATION_TYPES))


# ---------------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------------

def calculate_p2(notice_period_days, buyout_situation, current_brand,
                 new_brand, work_mode_preference, work_mode_offered,
                 partner_profile, relocation_type):
    """
    Calculate P2 score.

    Parameters
    ----------
    notice_period_days  : int/float -- notice period in days (0 = immediate)
    buyout_situation    : str       -- one of BUYOUT_SITUATIONS
    current_brand       : str       -- one of BRAND_TIERS (top/average/unknown)
    new_brand           : str       -- one of BRAND_TIERS (top/average/unknown)
    work_mode_preference: str       -- one of WORK_MODE_PREFERENCES
    work_mode_offered   : str       -- one of WORK_MODE_OPTIONS
    partner_profile     : str       -- one of PARTNER_PROFILES
    relocation_type     : str       -- one of RELOCATION_TYPES

    Returns
    -------
    score     : int   -- P2 score (0-100)
    breakdown : dict  -- full calculation details
    """
    _validate_inputs(notice_period_days, buyout_situation, current_brand,
                     new_brand, work_mode_preference, work_mode_offered,
                     partner_profile, relocation_type)

    # --- Section A: Notice period
    notice_base     = _notice_base_score(notice_period_days)
    buyout_mod      = BUYOUT_MODIFIER[buyout_situation]
    notice_final    = _clamp(notice_base + buyout_mod)

    # --- Section B: Brand
    leaving_mod     = LEAVING_BRAND_MODIFIER[current_brand]
    joining_mod     = JOINING_BRAND_MODIFIER[new_brand]
    brand_score     = _clamp(BRAND_BASE + leaving_mod + joining_mod)

    # --- Section C: Work mode match
    work_mode_score = WORK_MODE_SCORES[work_mode_preference][work_mode_offered]

    # --- Section D: Partner modifier applied to weighted base
    bucket          = _relocation_bucket(relocation_type)
    partner_mod     = PARTNER_MODIFIERS[partner_profile][bucket]

    # Weighted base before partner modifier
    weighted_base   = (notice_final * 0.35) + (brand_score * 0.30) + (work_mode_score * 0.20)
    # Partner modifier scaled to its 15% weight and applied
    partner_impact  = partner_mod * 0.15
    p2_raw          = weighted_base + (weighted_base * 0.15) + partner_impact
    # Normalise back to 0-100
    p2_raw          = (notice_final * 0.35) + (brand_score * 0.30) + \
                      (work_mode_score * 0.20) + (_clamp(50 + partner_mod * 2) * 0.15)
    p2_score        = _clamp(round(p2_raw))

    breakdown = {
        "parameter"             : "P2 -- Notice Period, Brand, Work Mode & Partner",
        # inputs
        "notice_period_days"    : notice_period_days,
        "buyout_situation"      : buyout_situation,
        "current_brand"         : current_brand,
        "new_brand"             : new_brand,
        "work_mode_preference"  : work_mode_preference,
        "work_mode_offered"     : work_mode_offered,
        "partner_profile"       : partner_profile,
        "relocation_type"       : relocation_type,
        # section scores
        "notice_base_score"     : notice_base,
        "buyout_modifier"       : buyout_mod,
        "notice_final_score"    : notice_final,
        "leaving_brand_modifier": leaving_mod,
        "joining_brand_modifier": joining_mod,
        "brand_score"           : brand_score,
        "work_mode_score"       : work_mode_score,
        "partner_modifier"      : partner_mod,
        # final
        "p2_score"              : p2_score,
    }

    return p2_score, breakdown


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_p2(breakdown):
    """Pretty-print the P2 breakdown."""
    print("\n" + "=" * 55)
    print("  P2 SCORE -- Notice, Brand, Work Mode & Partner")
    print("=" * 55)
    print("  Notice Period     : {} days".format(breakdown["notice_period_days"]))
    print("  Buyout Situation  : {}".format(breakdown["buyout_situation"]))
    print("  Current Brand     : {}".format(breakdown["current_brand"]))
    print("  New Brand         : {}".format(breakdown["new_brand"]))
    print("  Work Mode Pref    : {}".format(breakdown["work_mode_preference"]))
    print("  Work Mode Offered : {}".format(breakdown["work_mode_offered"]))
    print("  Partner Profile   : {}".format(breakdown["partner_profile"]))
    print("  Relocation Type   : {}".format(breakdown["relocation_type"]))
    print("-" * 55)
    print("  Notice Base       : {}  Buyout Mod: {}  Final: {}".format(
        breakdown["notice_base_score"],
        breakdown["buyout_modifier"],
        breakdown["notice_final_score"]))
    print("  Brand Score       : {}  (Leaving: {}  Joining: {})".format(
        breakdown["brand_score"],
        breakdown["leaving_brand_modifier"],
        breakdown["joining_brand_modifier"]))
    print("  Work Mode Score   : {}".format(breakdown["work_mode_score"]))
    print("  Partner Modifier  : {}".format(breakdown["partner_modifier"]))
    print("-" * 55)
    print("  P2 SCORE          : {} / 100".format(breakdown["p2_score"]))
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Quick Test (run directly: python p2.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        # (notice_days, buyout, curr_brand, new_brand, wm_pref, wm_offered, partner, reloc, note)
        (0,   "not_available",    "unknown", "top",     "prefers_hybrid",  "hybrid",      "not_applicable",         "same_city",   "Immediate, unknown->top, perfect wm, no partner -> expect high"),
        (90,  "not_available",    "top",     "average", "prefers_remote",  "full_office", "employed_niche_role",     "diff_state",  "90d notice, top->avg, wm mismatch, niche partner -> expect low"),
        (30,  "available_willing","average", "top",     "prefers_hybrid",  "hybrid",      "not_applicable",         "same_city",   "30d buyout, avg->top, perfect wm, single -> expect high"),
        (60,  "unwilling",        "top",     "unknown", "prefers_remote",  "full_office", "employed_no_jobs",        "abroad_with_family", "60d unwilling, top->unknown, mismatch, partner no jobs abroad -> expect very low"),
        (45,  "available_unsure", "average", "average", "no_preference",   "hybrid",      "not_employed",           "diff_city_same_state", "45d, avg->avg, flexible pref, not employed partner diff city -> moderate"),
    ]

    for (nd, buyout, cb, nb, wmp, wmo, partner, reloc, note) in test_cases:
        print("Test: {}".format(note))
        score, breakdown = calculate_p2(nd, buyout, cb, nb, wmp, wmo, partner, reloc)
        display_p2(breakdown)