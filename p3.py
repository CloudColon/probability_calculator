"""
P3 Parameter -- Interview Experience, Offer-to-Joining Gap, Career Growth & Motivation
========================================================================================
Calculates a P3 score (0-100) based on:
  - Interview experience (candidate self-rating + recruiter observation)
  - Offer-to-joining time gap + engagement level during gap
  - Career move type + goal alignment
  - Push vs Pull motivation

Usage (when imported):
    from p3 import calculate_p3, display_p3
    score, breakdown = calculate_p3(
        candidate_interview_rating=4,
        recruiter_observations={"engagement": "high", "process_speed": "medium",
                                 "responsiveness": "high", "interviewer_quality": "high"},
        offer_to_joining_days=45,
        engagement_during_gap="moderate",
        career_move_type="clear_promotion",
        goal_alignment="perfect_match",
        push_factor="no_growth",
        pull_factor="dream_company"
    )
"""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RECRUITER_OBSERVATION_DIMENSIONS = [
    "engagement",           # candidate engagement level during interviews
    "process_speed",        # how smooth and fast the process was
    "responsiveness",       # candidate's post-interview responsiveness
    "interviewer_quality",  # candidate's perceived impression of interviewers
]

OBSERVATION_LEVELS   = ["low", "medium", "high"]

ENGAGEMENT_LEVELS    = ["strong", "moderate", "minimal", "none"]

CAREER_MOVE_TYPES    = ["clear_promotion", "stretch_role", "lateral_move"]

GOAL_ALIGNMENTS      = [
    "perfect_match",
    "partial_match",
    "indifferent",
    "does_not_match",
    "compromise",
]

PUSH_FACTORS         = [
    "toxic_environment",
    "no_growth",
    "company_instability",
    "compensation_below_market",
    "role_changed_against_will",
    "personal_relocation",
    "no_push",
]

PULL_FACTORS         = [
    "dream_company",
    "career_step_up",
    "domain_passion",
    "better_ctc",
    "better_wlb",
    "referred_by_network",
    "no_pull",
]


# ---------------------------------------------------------------------------
# Section A -- Interview Experience
# ---------------------------------------------------------------------------

# Candidate self-rating 1-5 -> score
CANDIDATE_RATING_SCORE = {
    5: 100,
    4:  80,
    3:  60,
    2:  35,
    1:  15,
}

# Recruiter observation dimension scores
OBSERVATION_SCORE = {
    "low"   : 25,
    "medium": 60,
    "high"  : 100,
}


def _interview_score(candidate_rating, recruiter_observations):
    """
    Final interview score = candidate score (50%) + recruiter avg score (50%).
    recruiter_observations: dict of {dimension: level} for all 4 dimensions.
    """
    candidate_score  = CANDIDATE_RATING_SCORE[candidate_rating]
    recruiter_scores = [
        OBSERVATION_SCORE[recruiter_observations[dim]]
        for dim in RECRUITER_OBSERVATION_DIMENSIONS
    ]
    recruiter_avg    = sum(recruiter_scores) / len(recruiter_scores)
    return round((candidate_score * 0.50) + (recruiter_avg * 0.50))


# ---------------------------------------------------------------------------
# Section B -- Offer-to-Joining Time Gap
# ---------------------------------------------------------------------------

def _gap_base_score(offer_to_joining_days):
    """Map gap in days to a base score."""
    if offer_to_joining_days <= 7:
        return 100
    elif offer_to_joining_days <= 14:
        return 90
    elif offer_to_joining_days <= 30:
        return 80
    elif offer_to_joining_days <= 60:
        return 65
    elif offer_to_joining_days <= 90:
        return 45
    elif offer_to_joining_days <= 120:
        return 25
    else:
        return 10


ENGAGEMENT_MODIFIER = {
    "strong"  : +15,
    "moderate":  +5,
    "minimal" :   0,
    "none"    : -20,
}


# ---------------------------------------------------------------------------
# Section C -- Career Growth Alignment
# ---------------------------------------------------------------------------

CAREER_MOVE_BASE = {
    "clear_promotion": 95,
    "stretch_role"   : 80,
    "lateral_move"   : 55,
}

GOAL_ALIGNMENT_MODIFIER = {
    "perfect_match"  : +15,
    "partial_match"  :  +5,
    "indifferent"    :   0,
    "does_not_match" : -15,
    "compromise"     : -25,
}


# ---------------------------------------------------------------------------
# Section D -- Push vs Pull
# ---------------------------------------------------------------------------

PUSH_MODIFIER = {
    "toxic_environment"        : +20,
    "no_growth"                : +20,
    "company_instability"      : +15,
    "compensation_below_market": +10,
    "role_changed_against_will": +15,
    "personal_relocation"      : +10,
    "no_push"                  : -15,
}

PULL_MODIFIER = {
    "dream_company"    : +20,
    "career_step_up"   : +20,
    "domain_passion"   : +15,
    "better_ctc"       : +10,
    "better_wlb"       :  +5,
    "referred_by_network": +10,
    "no_pull"          : -20,
}

PUSH_PULL_BASE = 50


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _clamp(value, lo=10, hi=100):
    return max(lo, min(hi, value))


def _validate_inputs(candidate_interview_rating, recruiter_observations,
                     offer_to_joining_days, engagement_during_gap,
                     career_move_type, goal_alignment,
                     push_factor, pull_factor):

    if candidate_interview_rating not in CANDIDATE_RATING_SCORE:
        raise ValueError("candidate_interview_rating must be 1, 2, 3, 4, or 5")

    if not isinstance(recruiter_observations, dict):
        raise ValueError("recruiter_observations must be a dict")
    for dim in RECRUITER_OBSERVATION_DIMENSIONS:
        if dim not in recruiter_observations:
            raise ValueError("recruiter_observations missing key: '{}'".format(dim))
        if recruiter_observations[dim] not in OBSERVATION_LEVELS:
            raise ValueError("recruiter_observations['{}'] must be one of: {}".format(
                dim, OBSERVATION_LEVELS))

    if not isinstance(offer_to_joining_days, (int, float)) or offer_to_joining_days < 0:
        raise ValueError("offer_to_joining_days must be a non-negative number")

    if engagement_during_gap not in ENGAGEMENT_LEVELS:
        raise ValueError("engagement_during_gap must be one of: {}".format(ENGAGEMENT_LEVELS))

    if career_move_type not in CAREER_MOVE_TYPES:
        raise ValueError("career_move_type must be one of: {}".format(CAREER_MOVE_TYPES))

    if goal_alignment not in GOAL_ALIGNMENTS:
        raise ValueError("goal_alignment must be one of: {}".format(GOAL_ALIGNMENTS))

    if push_factor not in PUSH_FACTORS:
        raise ValueError("push_factor must be one of: {}".format(PUSH_FACTORS))

    if pull_factor not in PULL_FACTORS:
        raise ValueError("pull_factor must be one of: {}".format(PULL_FACTORS))


# ---------------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------------

def calculate_p3(candidate_interview_rating, recruiter_observations,
                 offer_to_joining_days, engagement_during_gap,
                 career_move_type, goal_alignment,
                 push_factor, pull_factor):
    """
    Calculate P3 score.

    Parameters
    ----------
    candidate_interview_rating : int   -- 1 to 5 (candidate self-rating post process)
    recruiter_observations     : dict  -- {dimension: level} for all 4 dimensions
                                         dimensions : engagement | process_speed |
                                                      responsiveness | interviewer_quality
                                         levels     : low | medium | high
    offer_to_joining_days      : int   -- days between offer date and joining date
    engagement_during_gap      : str   -- strong | moderate | minimal | none
    career_move_type           : str   -- clear_promotion | stretch_role | lateral_move
    goal_alignment             : str   -- perfect_match | partial_match | indifferent |
                                         does_not_match | compromise
    push_factor                : str   -- one of PUSH_FACTORS
    pull_factor                : str   -- one of PULL_FACTORS

    Returns
    -------
    score     : int   -- P3 score (0-100)
    breakdown : dict  -- full calculation details
    """
    _validate_inputs(candidate_interview_rating, recruiter_observations,
                     offer_to_joining_days, engagement_during_gap,
                     career_move_type, goal_alignment,
                     push_factor, pull_factor)

    # --- Section A: Interview experience
    interview_score  = _clamp(_interview_score(
        candidate_interview_rating, recruiter_observations))

    # --- Section B: Time gap
    gap_base         = _gap_base_score(offer_to_joining_days)
    engagement_mod   = ENGAGEMENT_MODIFIER[engagement_during_gap]
    gap_final        = _clamp(gap_base + engagement_mod)

    # --- Section C: Career growth
    move_base        = CAREER_MOVE_BASE[career_move_type]
    alignment_mod    = GOAL_ALIGNMENT_MODIFIER[goal_alignment]
    career_score     = _clamp(move_base + alignment_mod)

    # --- Section D: Push vs pull
    push_mod         = PUSH_MODIFIER[push_factor]
    pull_mod         = PULL_MODIFIER[pull_factor]
    push_pull_score  = _clamp(PUSH_PULL_BASE + push_mod + pull_mod)

    # --- P3 composite
    # Weights: Interview 25%, Gap 30%, Career 25%, Push/Pull 20%
    p3_raw   = (interview_score  * 0.25) + \
               (gap_final        * 0.30) + \
               (career_score     * 0.25) + \
               (push_pull_score  * 0.20)
    p3_score = _clamp(round(p3_raw))

    breakdown = {
        "parameter"                  : "P3 -- Interview, Gap, Career Growth & Motivation",
        # inputs
        "candidate_interview_rating" : candidate_interview_rating,
        "recruiter_observations"     : recruiter_observations,
        "offer_to_joining_days"      : offer_to_joining_days,
        "engagement_during_gap"      : engagement_during_gap,
        "career_move_type"           : career_move_type,
        "goal_alignment"             : goal_alignment,
        "push_factor"                : push_factor,
        "pull_factor"                : pull_factor,
        # section scores
        "interview_score"            : interview_score,
        "gap_base_score"             : gap_base,
        "engagement_modifier"        : engagement_mod,
        "gap_final_score"            : gap_final,
        "career_move_base"           : move_base,
        "goal_alignment_modifier"    : alignment_mod,
        "career_score"               : career_score,
        "push_modifier"              : push_mod,
        "pull_modifier"              : pull_mod,
        "push_pull_score"            : push_pull_score,
        # final
        "p3_score"                   : p3_score,
    }

    return p3_score, breakdown


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_p3(breakdown):
    """Pretty-print the P3 breakdown."""
    obs = breakdown["recruiter_observations"]
    print("\n" + "=" * 55)
    print("  P3 SCORE -- Interview, Gap, Career & Motivation")
    print("=" * 55)
    print("  Candidate Rating  : {} / 5".format(breakdown["candidate_interview_rating"]))
    print("  Recruiter Obs     : engagement={}, process_speed={}, responsiveness={}, interviewer_quality={}".format(
        obs["engagement"], obs["process_speed"],
        obs["responsiveness"], obs["interviewer_quality"]))
    print("  Offer-Join Gap    : {} days".format(breakdown["offer_to_joining_days"]))
    print("  Engagement Level  : {}".format(breakdown["engagement_during_gap"]))
    print("  Career Move       : {}".format(breakdown["career_move_type"]))
    print("  Goal Alignment    : {}".format(breakdown["goal_alignment"]))
    print("  Push Factor       : {}".format(breakdown["push_factor"]))
    print("  Pull Factor       : {}".format(breakdown["pull_factor"]))
    print("-" * 55)
    print("  Interview Score   : {}".format(breakdown["interview_score"]))
    print("  Gap Score         : {}  (Base: {}  Engagement Mod: {})".format(
        breakdown["gap_final_score"],
        breakdown["gap_base_score"],
        breakdown["engagement_modifier"]))
    print("  Career Score      : {}  (Base: {}  Alignment Mod: {})".format(
        breakdown["career_score"],
        breakdown["career_move_base"],
        breakdown["goal_alignment_modifier"]))
    print("  Push/Pull Score   : {}  (Push: {}  Pull: {})".format(
        breakdown["push_pull_score"],
        breakdown["push_modifier"],
        breakdown["pull_modifier"]))
    print("-" * 55)
    print("  P3 SCORE          : {} / 100".format(breakdown["p3_score"]))
    print("=" * 55 + "\n")


# ---------------------------------------------------------------------------
# Quick Test (run directly: python p3.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        # Best case -- everything positive
        {
            "candidate_interview_rating": 5,
            "recruiter_observations"    : {"engagement": "high", "process_speed": "high",
                                           "responsiveness": "high", "interviewer_quality": "high"},
            "offer_to_joining_days"     : 7,
            "engagement_during_gap"     : "strong",
            "career_move_type"          : "clear_promotion",
            "goal_alignment"            : "perfect_match",
            "push_factor"               : "toxic_environment",
            "pull_factor"               : "dream_company",
            "note"                      : "Best case -- expect ~100",
        },
        # Worst case -- everything negative
        {
            "candidate_interview_rating": 1,
            "recruiter_observations"    : {"engagement": "low", "process_speed": "low",
                                           "responsiveness": "low", "interviewer_quality": "low"},
            "offer_to_joining_days"     : 150,
            "engagement_during_gap"     : "none",
            "career_move_type"          : "lateral_move",
            "goal_alignment"            : "compromise",
            "push_factor"               : "no_push",
            "pull_factor"               : "no_pull",
            "note"                      : "Worst case -- expect ~10",
        },
        # Moderate -- mixed signals
        {
            "candidate_interview_rating": 3,
            "recruiter_observations"    : {"engagement": "medium", "process_speed": "medium",
                                           "responsiveness": "medium", "interviewer_quality": "high"},
            "offer_to_joining_days"     : 45,
            "engagement_during_gap"     : "moderate",
            "career_move_type"          : "stretch_role",
            "goal_alignment"            : "partial_match",
            "push_factor"               : "no_growth",
            "pull_factor"               : "better_ctc",
            "note"                      : "Mixed signals -- expect moderate 55-70",
        },
        # Strong push, weak pull, long gap but strong engagement
        {
            "candidate_interview_rating": 4,
            "recruiter_observations"    : {"engagement": "high", "process_speed": "medium",
                                           "responsiveness": "high", "interviewer_quality": "medium"},
            "offer_to_joining_days"     : 80,
            "engagement_during_gap"     : "strong",
            "career_move_type"          : "lateral_move",
            "goal_alignment"            : "indifferent",
            "push_factor"               : "company_instability",
            "pull_factor"               : "referred_by_network",
            "note"                      : "Strong push, engagement saves long gap -- expect 60-70",
        },
    ]

    for tc in test_cases:
        note = tc.pop("note")
        print("Test: {}".format(note))
        score, breakdown = calculate_p3(**tc)
        display_p3(breakdown)