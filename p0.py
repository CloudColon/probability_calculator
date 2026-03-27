"""
P0 Parameter -- Expected CTC (Compensation-Based Scoring)
==========================================================
Calculates a P0 score (0-100) based on:
  - Candidate's current CTC (LPA)
  - New CTC being offered (LPA)

Usage (when imported):
    from p0 import calculate_p0, display_p0
    score, breakdown = calculate_p0(current_ctc=8, new_ctc=13)
    display_p0(breakdown)
"""


# ---------------------------------------------------------------------------
# Slab Definitions
# Each entry: (max_ctc, label, hike_brackets)
# hike_brackets: [(min_hike_pct, score), ...] sorted highest first
# Rule: if hike% >= min_hike_pct -> award that score
# ---------------------------------------------------------------------------

SLABS = [
    (6, "Below 6 LPA", [
        (100, 100),
        (80,   90),
        (60,   80),
        (40,   65),
        (20,   50),
        (10,   35),
        (0,    20),
    ]),
    (10, "6 - 10 LPA", [
        (80,  100),
        (60,   90),
        (50,   80),
        (35,   65),
        (20,   50),
        (10,   35),
        (0,    20),
    ]),
    (15, "10 - 15 LPA", [
        (70,  100),
        (55,   90),
        (40,   80),
        (30,   65),
        (20,   50),
        (10,   35),
        (0,    20),
    ]),
    (20, "15 - 20 LPA", [
        (60,  100),
        (50,   90),
        (40,   80),
        (30,   65),
        (20,   50),
        (10,   35),
        (0,    20),
    ]),
    (30, "20 - 30 LPA", [
        (50,  100),
        (40,   90),
        (30,   80),
        (25,   70),
        (15,   55),
        (10,   40),
        (0,    20),
    ]),
    (40, "30 - 40 LPA", [
        (40,  100),
        (35,   90),
        (30,   80),
        (20,   70),
        (15,   55),
        (10,   40),
        (0,    20),
    ]),
    (50, "40 - 50 LPA", [
        (35,  100),
        (30,   90),
        (25,   80),
        (20,   70),
        (15,   55),
        (10,   40),
        (0,    20),
    ]),
    (60, "50 - 60 LPA", [
        (30,  100),
        (25,   90),
        (20,   80),
        (15,   70),
        (10,   55),
        (5,    35),
        (0,    15),
    ]),
    (float("inf"), "Above 60 LPA", [
        (30,  100),
        (25,   90),
        (20,   80),
        (15,   70),
        (10,   55),
        (5,    35),
        (0,    15),
    ]),
]


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _get_slab(current_ctc):
    for max_ctc, label, brackets in SLABS:
        if current_ctc < max_ctc:
            return label, brackets
    return SLABS[-1][1], SLABS[-1][2]


def _score_from_hike(hike_pct, brackets):
    for i, (min_hike, score) in enumerate(brackets):
        if hike_pct >= min_hike:
            if i == 0:
                label = ">= {}% hike".format(min_hike)
            else:
                upper = brackets[i - 1][0]
                label = "{}% to {}% hike".format(min_hike, upper - 1)
            return score, label
    return 10, "Below minimum threshold"


# def _joining_likelihood(score):
#     if score >= 90:
#         return "Very High -- Almost certain to join"
#     elif score >= 80:
#         return "High -- Likely to join"
#     elif score >= 70:
#         return "Moderate-High -- Good chance of joining"
#     elif score >= 55:
#         return "Moderate -- May join, needs follow-up"
#     elif score >= 40:
#         return "Low-Moderate -- At risk of declining"
#     elif score >= 25:
#         return "Low -- Unlikely unless other factors are strong"
#     else:
#         return "Very Low -- Will likely not join"


# ---------------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------------

def calculate_p0(current_ctc, new_ctc):
    """
    Calculate P0 score.

    Parameters
    ----------
    current_ctc : float  -- Current CTC in LPA
    new_ctc     : float  -- New offered CTC in LPA

    Returns
    -------
    score     : int   -- P0 score (0-100)
    breakdown : dict  -- Full calculation details
    """
    if current_ctc <= 0:
        raise ValueError("current_ctc must be greater than 0")
    if new_ctc <= 0:
        raise ValueError("new_ctc must be greater than 0")

    hike_pct = ((new_ctc - current_ctc) / current_ctc) * 100
    slab_label, brackets = _get_slab(current_ctc)
    score, bracket_label = _score_from_hike(hike_pct, brackets)

    breakdown = {
        "parameter"         : "P0 -- Expected CTC",
        "current_ctc_lpa"   : current_ctc,
        "new_ctc_lpa"       : new_ctc,
        "hike_pct"          : round(hike_pct, 2),
        "ctc_slab"          : slab_label,
        "hike_bracket"      : bracket_label,
        "p0_score"          : score,
        # "joining_likelihood": _joining_likelihood(score),
    }

    return score, breakdown


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_p0(breakdown):
    """Pretty-print the P0 breakdown."""
    print("\n" + "=" * 55)
    print("  P0 SCORE -- Expected CTC")
    print("=" * 55)
    print("  Current CTC       : {} LPA".format(breakdown["current_ctc_lpa"]))
    print("  New CTC Offered   : {} LPA".format(breakdown["new_ctc_lpa"]))
    print("  Hike              : {}%".format(breakdown["hike_pct"]))
    print("  CTC Slab          : {}".format(breakdown["ctc_slab"]))
    print("  Hike Bracket      : {}".format(breakdown["hike_bracket"]))
    print("-" * 55)
    print("  P0 SCORE          : {} / 100".format(breakdown["p0_score"]))
    # print("  Joining Likelihood: {}".format(breakdown["joining_likelihood"]))
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Quick Test (run directly: python p0.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        (5,   10,   "Below 6 LPA, 100% hike   -> expect 100"),
        (8,   12.8, "6-10 LPA,     60% hike   -> expect 90"),
        (12,  16.8, "10-15 LPA,    40% hike   -> expect 80"),
        (25,  32.5, "20-30 LPA,    30% hike   -> expect 80"),
        (55,  66,   "50-60 LPA,    20% hike   -> expect 80"),
        (35,  37.5, "30-40 LPA,  ~7.1% hike   -> expect 20"),
    ]

    for current, new, note in test_cases:
        print("Test: {}".format(note))
        score, breakdown = calculate_p0(current, new)
        display_p0(breakdown)