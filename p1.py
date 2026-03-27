"""
P1 Parameter -- Location, Marital Status & Competing Offers
============================================================
Calculates a P1 score (0-100) based on:
  - Relocation type (same city / diff city / diff state / abroad)
  - City expense tier (1 / 2 / 3)
  - Marital status and children profile
  - Number of competing offers in hand
  - Offer strength vs competing offers

Usage (when imported):
    from p1 import calculate_p1, display_p1
    score, breakdown = calculate_p1(
        relocation_type="diff_state",
        city_tier=1,
        family_profile="married_school_children",
        competing_offers=2,
        offer_strength="equal"
    )
"""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Valid values for each input
RELOCATION_TYPES = [
    "same_city",
    "diff_city_same_state",
    "diff_state",
    "abroad_with_family",
    "abroad_without_family",
]

CITY_TIERS = [1, 2, 3]

FAMILY_PROFILES = [
    "single_no_children",
    "single_with_children",
    "married_no_children",
    "married_school_children",
    "married_preschool_children",
    "married_adult_children",
]

OFFER_STRENGTHS = [
    "best",     # this offer is clearly the best
    "equal",    # roughly equal to others
    "weaker",   # weaker than at least one other
    "weakest",  # weakest among all offers
]


# ---------------------------------------------------------------------------
# Section A -- Location Base Score
# Rows = relocation type, Cols = city tier (1, 2, 3)
# ---------------------------------------------------------------------------

# {relocation_type: {tier: base_score}}
LOCATION_SCORES = {
    "same_city"            : {1: 100, 2: 100, 3: 100},
    "diff_city_same_state" : {1:  75, 2:  85, 3:  90},
    "diff_state"           : {1:  55, 2:  70, 3:  80},
    "abroad_with_family"   : {1:  35, 2:  50, 3:  60},
    "abroad_without_family": {1:  60, 2:  70, 3:  75},
}


# ---------------------------------------------------------------------------
# Section B -- Family / Marital Modifier
# {family_profile: {relocation_bucket: modifier}}
# relocation_bucket: "same_city" | "diff_city_or_state" | "abroad"
# ---------------------------------------------------------------------------

def _relocation_bucket(relocation_type):
    if relocation_type == "same_city":
        return "same_city"
    elif relocation_type in ("diff_city_same_state", "diff_state"):
        return "diff_city_or_state"
    else:
        return "abroad"


FAMILY_MODIFIERS = {
    "single_no_children"      : {"same_city":  0, "diff_city_or_state":   0, "abroad":   0},
    "single_with_children"    : {"same_city": -5, "diff_city_or_state": -10, "abroad": -20},
    "married_no_children"     : {"same_city":  0, "diff_city_or_state":  -5, "abroad": -10},
    "married_school_children" : {"same_city": -5, "diff_city_or_state": -20, "abroad": -35},
    "married_preschool_children":{"same_city":  0, "diff_city_or_state": -10, "abroad": -20},
    "married_adult_children"  : {"same_city":  0, "diff_city_or_state":  -5, "abroad": -10},
}


# ---------------------------------------------------------------------------
# Section C -- Competing Offers Score
# ---------------------------------------------------------------------------

# Base score by number of competing offers
OFFERS_BASE_SCORE = {
    0: 100,
    1:  80,
    2:  60,
    3:  40,
    4:  20,   # 4+ offers
}

def _offers_base(competing_offers):
    """Cap at 4 for scoring purposes (4+ all score 20)."""
    capped = min(competing_offers, 4)
    return OFFERS_BASE_SCORE[capped]


# Offer strength modifier
OFFER_STRENGTH_MODIFIER = {
    "best"   : +15,
    "equal"  :   0,
    "weaker" : -15,
    "weakest": -25,
}


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _validate_inputs(relocation_type, city_tier, family_profile,
                     competing_offers, offer_strength):
    if relocation_type not in RELOCATION_TYPES:
        raise ValueError("relocation_type must be one of: {}".format(RELOCATION_TYPES))
    if city_tier not in CITY_TIERS:
        raise ValueError("city_tier must be 1, 2, or 3")
    if family_profile not in FAMILY_PROFILES:
        raise ValueError("family_profile must be one of: {}".format(FAMILY_PROFILES))
    if not isinstance(competing_offers, int) or competing_offers < 0:
        raise ValueError("competing_offers must be a non-negative integer")
    if offer_strength not in OFFER_STRENGTHS:
        raise ValueError("offer_strength must be one of: {}".format(OFFER_STRENGTHS))


def _clamp(value, lo=10, hi=100):
    return max(lo, min(hi, value))


# ---------------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------------

def calculate_p1(relocation_type, city_tier, family_profile,
                 competing_offers, offer_strength):
    """
    Calculate P1 score.

    Parameters
    ----------
    relocation_type  : str  -- one of RELOCATION_TYPES
    city_tier        : int  -- 1 (high expense), 2 (mid), 3 (low)
    family_profile   : str  -- one of FAMILY_PROFILES
    competing_offers : int  -- number of other offers candidate holds (0, 1, 2, ...)
    offer_strength   : str  -- one of OFFER_STRENGTHS

    Returns
    -------
    score     : int   -- P1 score (0-100)
    breakdown : dict  -- full calculation details
    """
    _validate_inputs(relocation_type, city_tier, family_profile,
                     competing_offers, offer_strength)

    # --- Section A: Location base
    location_base = LOCATION_SCORES[relocation_type][city_tier]

    # --- Section B: Family modifier
    bucket = _relocation_bucket(relocation_type)
    family_modifier = FAMILY_MODIFIERS[family_profile][bucket]
    location_final = _clamp(location_base + family_modifier)

    # --- Section C: Competing offers
    offers_base = _offers_base(competing_offers)
    strength_modifier = OFFER_STRENGTH_MODIFIER[offer_strength]
    offers_final = _clamp(offers_base + strength_modifier)

    # --- P1 composite (weights: location 40%, offers 35%; family already baked in)
    # Remaining 25% is the family modifier's direct impact absorbed into location_final
    p1_raw = (location_final * 0.40) + (offers_final * 0.35) + (location_base * 0.25)
    p1_score = _clamp(round(p1_raw))

    breakdown = {
        "parameter"              : "P1 -- Location, Family & Competing Offers",
        # inputs
        "relocation_type"        : relocation_type,
        "city_tier"              : city_tier,
        "family_profile"         : family_profile,
        "competing_offers"       : competing_offers,
        "offer_strength"         : offer_strength,
        # section scores
        "location_base_score"    : location_base,
        "family_modifier"        : family_modifier,
        "location_final_score"   : location_final,
        "offers_base_score"      : offers_base,
        "offer_strength_modifier": strength_modifier,
        "offers_final_score"     : offers_final,
        # final
        "p1_score"               : p1_score,
    }

    return p1_score, breakdown


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_p1(breakdown):
    """Pretty-print the P1 breakdown."""
    print("\n" + "=" * 55)
    print("  P1 SCORE -- Location, Family & Competing Offers")
    print("=" * 55)
    print("  Relocation Type   : {}".format(breakdown["relocation_type"]))
    print("  City Tier         : {}".format(breakdown["city_tier"]))
    print("  Family Profile    : {}".format(breakdown["family_profile"]))
    print("  Competing Offers  : {}".format(breakdown["competing_offers"]))
    print("  Offer Strength    : {}".format(breakdown["offer_strength"]))
    print("-" * 55)
    print("  Location Base     : {}".format(breakdown["location_base_score"]))
    print("  Family Modifier   : {}".format(breakdown["family_modifier"]))
    print("  Location Final    : {}".format(breakdown["location_final_score"]))
    print("  Offers Base       : {}".format(breakdown["offers_base_score"]))
    print("  Strength Modifier : {}".format(breakdown["offer_strength_modifier"]))
    print("  Offers Final      : {}".format(breakdown["offers_final_score"]))
    print("-" * 55)
    print("  P1 SCORE          : {} / 100".format(breakdown["p1_score"]))
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Quick Test (run directly: python p1.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        # (relocation_type, city_tier, family_profile, competing_offers, offer_strength, note)
        ("same_city",             1, "single_no_children",       0, "best",    "Same city, no family, no competition -> expect ~100"),
        ("diff_state",            1, "married_school_children",  2, "equal",   "Diff state, school kids, 2 offers    -> expect low"),
        ("abroad_with_family",    1, "married_school_children",  3, "weaker",  "Abroad, school kids, 3 offers weaker -> expect very low"),
        ("diff_city_same_state",  2, "married_no_children",      1, "best",    "Diff city tier2, married no kids     -> expect moderate"),
        ("same_city",             1, "married_school_children",  0, "best",    "Same city, school kids, 0 offers     -> expect high"),
        ("abroad_without_family", 3, "single_no_children",       1, "equal",   "Abroad no family, tier3, 1 offer     -> expect decent"),
    ]

    for reloc, tier, family, offers, strength, note in test_cases:
        print("Test: {}".format(note))
        score, breakdown = calculate_p1(reloc, tier, family, offers, strength)
        display_p1(breakdown)