"""
Offer Acceptance Prediction Model — Master File
================================================
Combines P0 through P4 into a single joining probability score.

Weights:
    P0 (CTC)                        45%
    P1 (Location, Family, Offers)   22%
    P2 (Notice, Brand, Work, Partner) 17%
    P3 (Interview, Gap, Career, Motivation) 10%
    P4 (Counter-offer, Warmth, Stability)    6%

Formula:
    Final Score = (P0*0.45) + (P1*0.22) + (P2*0.17) + (P3*0.10) + (P4*0.06)

Usage:
    python main.py
"""

import sys
import os

# Allow importing from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from p0 import calculate_p0
from p1 import calculate_p1
from p2 import calculate_p2
from p3 import calculate_p3
from p4 import calculate_p4


# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

WEIGHTS = {
    "p0": 0.45,
    "p1": 0.22,
    "p2": 0.17,
    "p3": 0.10,
    "p4": 0.06,
}


# ---------------------------------------------------------------------------
# Joining Probability Interpretation
# ---------------------------------------------------------------------------

def _joining_probability(score):
    if score >= 85:
        return "Very High", ">85%", "Standard follow-up. Focus on onboarding experience."
    elif score >= 70:
        return "High", "65-85%", "Weekly check-ins. Confirm joining date and formalities."
    elif score >= 55:
        return "Moderate", "45-65%", "Bi-weekly calls. Identify weak parameter and address it."
    elif score >= 40:
        return "Low", "25-45%", "Escalate to hiring manager. Consider offer revision."
    else:
        return "Very Low", "<25%", "High drop risk. Start backup pipeline immediately."


def _risk_flag(p4_score):
    """Hard risk alert if P4 is critically low regardless of final score."""
    if p4_score < 30:
        return "RISK ALERT: P4 score is below 30 — counter-offer or ghost risk is high regardless of overall score."
    return None


# ---------------------------------------------------------------------------
# Master Calculator
# ---------------------------------------------------------------------------

def calculate_joining_probability(candidate_name, p0_inputs, p1_inputs,
                                   p2_inputs, p3_inputs, p4_inputs):
    """
    Calculate the final joining probability for a candidate.

    Parameters
    ----------
    candidate_name : str   -- candidate's name (for display)
    p0_inputs      : dict  -- inputs for calculate_p0()
    p1_inputs      : dict  -- inputs for calculate_p1()
    p2_inputs      : dict  -- inputs for calculate_p2()
    p3_inputs      : dict  -- inputs for calculate_p3()
    p4_inputs      : dict  -- inputs for calculate_p4()

    Returns
    -------
    result : dict  -- complete scoring result with all breakdowns
    """

    # --- Run all parameters
    p0_score, p0_breakdown = calculate_p0(**p0_inputs)
    p1_score, p1_breakdown = calculate_p1(**p1_inputs)
    p2_score, p2_breakdown = calculate_p2(**p2_inputs)
    p3_score, p3_breakdown = calculate_p3(**p3_inputs)
    p4_score, p4_breakdown = calculate_p4(**p4_inputs)

    # --- Weighted final score
    final_raw = (
        p0_score * WEIGHTS["p0"] +
        p1_score * WEIGHTS["p1"] +
        p2_score * WEIGHTS["p2"] +
        p3_score * WEIGHTS["p3"] +
        p4_score * WEIGHTS["p4"]
    )
    final_score = max(10, min(100, round(final_raw)))

    # --- Interpretation
    level, probability, action = _joining_probability(final_score)
    risk_flag = _risk_flag(p4_score)

    result = {
        "candidate_name"  : candidate_name,
        # individual scores
        "p0_score"        : p0_score,
        "p1_score"        : p1_score,
        "p2_score"        : p2_score,
        "p3_score"        : p3_score,
        "p4_score"        : p4_score,
        # weights applied
        "p0_weighted"     : round(p0_score * WEIGHTS["p0"], 2),
        "p1_weighted"     : round(p1_score * WEIGHTS["p1"], 2),
        "p2_weighted"     : round(p2_score * WEIGHTS["p2"], 2),
        "p3_weighted"     : round(p3_score * WEIGHTS["p3"], 2),
        "p4_weighted"     : round(p4_score * WEIGHTS["p4"], 2),
        # final
        "final_score"     : final_score,
        "joining_level"   : level,
        "joining_probability": probability,
        "recommended_action" : action,
        "risk_flag"       : risk_flag,
        # full breakdowns
        "p0_breakdown"    : p0_breakdown,
        "p1_breakdown"    : p1_breakdown,
        "p2_breakdown"    : p2_breakdown,
        "p3_breakdown"    : p3_breakdown,
        "p4_breakdown"    : p4_breakdown,
    }

    return result


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_result(result):
    """Pretty-print the full scoring result."""
    W = 60

    print("\n" + "=" * W)
    print("  OFFER ACCEPTANCE PREDICTION MODEL")
    print("  Candidate: {}".format(result["candidate_name"]))
    print("=" * W)

    # Parameter scores table
    print("\n  PARAMETER SCORES")
    print("  " + "-" * (W - 2))
    print("  {:<6}  {:<38}  {:>5}  {:>8}".format(
        "Param", "Description", "Score", "Weighted"))
    print("  " + "-" * (W - 2))

    rows = [
        ("P0", "CTC / Hike",                       "p0_score", "p0_weighted", "45%"),
        ("P1", "Location, Family & Offers",         "p1_score", "p1_weighted", "22%"),
        ("P2", "Notice, Brand, Work & Partner",     "p2_score", "p2_weighted", "17%"),
        ("P3", "Interview, Gap, Career & Motivation","p3_score", "p3_weighted","10%"),
        ("P4", "Counter-offer, Warmth & Stability", "p4_score", "p4_weighted", "6%"),
    ]
    for param, desc, score_key, weighted_key, weight in rows:
        print("  {:<6}  {:<38}  {:>5}  {:>8}".format(
            param + " (" + weight + ")",
            desc,
            str(result[score_key]) + "/100",
            str(result[weighted_key])
        ))

    print("  " + "-" * (W - 2))

    # Final score
    print("\n  FINAL SCORE       : {} / 100".format(result["final_score"]))
    print("  JOINING LEVEL     : {}".format(result["joining_level"]))
    print("  JOINING PROBABILITY: {}".format(result["joining_probability"]))
    print("\n  ACTION            : {}".format(result["recommended_action"]))

    # Risk flag
    if result["risk_flag"]:
        print("\n  *** {} ***".format(result["risk_flag"]))

    print("=" * W + "\n")


def display_detailed(result):
    """Print detailed per-parameter breakdown after the summary."""
    W = 60
    print("  DETAILED BREAKDOWN")
    print("=" * W)

    # P0
    b = result["p0_breakdown"]
    print("\n  P0 — CTC / Hike")
    print("  Current CTC: {} LPA  |  New CTC: {} LPA  |  Hike: {}%".format(
        b["current_ctc_lpa"], b["new_ctc_lpa"], b["hike_pct"]))
    print("  Slab: {}  |  Bracket: {}".format(b["ctc_slab"], b["hike_bracket"]))
    print("  Score: {}".format(b["p0_score"]))

    # P1
    b = result["p1_breakdown"]
    print("\n  P1 — Location, Family & Competing Offers")
    print("  Relocation: {}  |  City Tier: {}  |  Family: {}".format(
        b["relocation_type"], b["city_tier"], b["family_profile"]))
    print("  Location Base: {}  Family Mod: {}  Location Final: {}".format(
        b["location_base_score"], b["family_modifier"], b["location_final_score"]))
    print("  Competing Offers: {}  |  Strength: {}".format(
        b["competing_offers"], b["offer_strength"]))
    print("  Offers Base: {}  Strength Mod: {}  Offers Final: {}".format(
        b["offers_base_score"], b["offer_strength_modifier"], b["offers_final_score"]))
    print("  Score: {}".format(b["p1_score"]))

    # P2
    b = result["p2_breakdown"]
    print("\n  P2 — Notice, Brand, Work Mode & Partner")
    print("  Notice: {} days  |  Buyout: {}".format(
        b["notice_period_days"], b["buyout_situation"]))
    print("  Notice Base: {}  Buyout Mod: {}  Notice Final: {}".format(
        b["notice_base_score"], b["buyout_modifier"], b["notice_final_score"]))
    print("  Brand: {} -> {}  |  Brand Score: {}".format(
        b["current_brand"], b["new_brand"], b["brand_score"]))
    print("  Work Mode: {} vs {}  |  Work Mode Score: {}".format(
        b["work_mode_preference"], b["work_mode_offered"], b["work_mode_score"]))
    print("  Partner: {}  |  Partner Mod: {}".format(
        b["partner_profile"], b["partner_modifier"]))
    print("  Score: {}".format(b["p2_score"]))

    # P3
    b = result["p3_breakdown"]
    print("\n  P3 — Interview, Gap, Career & Motivation")
    print("  Interview Score: {}  (Candidate: {}/5)".format(
        b["interview_score"], b["candidate_interview_rating"]))
    print("  Gap: {} days  |  Engagement: {}  |  Gap Final: {}".format(
        b["offer_to_joining_days"], b["engagement_during_gap"], b["gap_final_score"]))
    print("  Career Move: {}  |  Alignment: {}  |  Career Score: {}".format(
        b["career_move_type"], b["goal_alignment"], b["career_score"]))
    print("  Push: {} (+{})  |  Pull: {} (+{})  |  Push/Pull Score: {}".format(
        b["push_factor"], b["push_modifier"],
        b["pull_factor"], b["pull_modifier"],
        b["push_pull_score"]))
    print("  Score: {}".format(b["p3_score"]))

    # P4
    b = result["p4_breakdown"]
    print("\n  P4 — Counter-offer, Warmth & Stability")
    print("  Company: {}  |  Seniority: {}  |  Tenure: {} yrs".format(
        b["company_type"], b["seniority_level"], b["current_tenure_years"]))
    print("  Counter-offer Score: {}  (Co: {}  Sen: {}  Ten: {})".format(
        b["counter_offer_score"], b["company_modifier"],
        b["seniority_modifier"], b["tenure_modifier"]))
    print("  Warmth Rating: {}/5  |  Boosters: {}  |  Warmth Score: {}".format(
        b["warmth_rating"],
        b["warmth_boosters"] if b["warmth_boosters"] else "none",
        b["warmth_score"]))
    print("  Avg Tenure: {} yrs  |  Context: {}  |  Stability Score: {}".format(
        b["avg_tenure_years"],
        b["stability_modifiers"] if b["stability_modifiers"] else "none",
        b["stability_score"]))
    print("  Score: {}".format(b["p4_score"]))

    print("\n" + "=" * W + "\n")


# ---------------------------------------------------------------------------
# Candidate Input Helper
# ---------------------------------------------------------------------------

def collect_candidate():
    """
    Interactive CLI to collect all 30 inputs for a candidate.
    Returns (candidate_name, p0_inputs, p1_inputs, p2_inputs, p3_inputs, p4_inputs)
    """

    print("\n" + "=" * 60)
    print("  OFFER ACCEPTANCE PREDICTION — INPUT COLLECTION")
    print("=" * 60)

    name = input("\nCandidate name: ").strip() or "Unknown"

    # --- P0
    print("\n--- P0: CTC ---")
    current_ctc = float(input("  Current CTC (LPA): "))
    new_ctc     = float(input("  New CTC offered (LPA): "))
    p0_inputs = {"current_ctc": current_ctc, "new_ctc": new_ctc}

    # --- P1
    print("\n--- P1: Location, Family & Competing Offers ---")
    print("  Relocation type options:")
    print("    same_city | diff_city_same_state | diff_state | abroad_with_family | abroad_without_family")
    reloc   = input("  Relocation type: ").strip()
    tier    = int(input("  City tier (1/2/3): "))
    print("  Family profile options:")
    print("    single_no_children | single_with_children | married_no_children")
    print("    married_school_children | married_preschool_children | married_adult_children")
    family  = input("  Family profile: ").strip()
    offers  = int(input("  Competing offers in hand (0,1,2,3,4+): "))
    print("  Offer strength options: best | equal | weaker | weakest")
    strength = input("  Offer strength: ").strip()
    p1_inputs = {
        "relocation_type" : reloc,
        "city_tier"       : tier,
        "family_profile"  : family,
        "competing_offers": offers,
        "offer_strength"  : strength,
    }

    # --- P2
    print("\n--- P2: Notice, Brand, Work Mode & Partner ---")
    notice  = float(input("  Notice period (days): "))
    print("  Buyout options: available_willing | available_unsure | not_available | unwilling")
    buyout  = input("  Buyout situation: ").strip()
    print("  Brand options: top | average | unknown")
    c_brand = input("  Current company brand: ").strip()
    n_brand = input("  New company brand: ").strip()
    print("  Work mode preference: prefers_remote | prefers_hybrid | prefers_office | no_preference")
    wm_pref = input("  Work mode preference: ").strip()
    print("  Work mode offered: full_remote | hybrid | full_office | flexible")
    wm_off  = input("  Work mode offered: ").strip()
    print("  Partner profile options:")
    print("    not_applicable | not_employed | employed_jobs_available")
    print("    employed_niche_role | employed_no_jobs | self_employed")
    partner = input("  Partner profile: ").strip()
    p2_inputs = {
        "notice_period_days"  : notice,
        "buyout_situation"    : buyout,
        "current_brand"       : c_brand,
        "new_brand"           : n_brand,
        "work_mode_preference": wm_pref,
        "work_mode_offered"   : wm_off,
        "partner_profile"     : partner,
        "relocation_type"     : reloc,   # reused from P1
    }

    # --- P3
    print("\n--- P3: Interview, Gap, Career & Motivation ---")
    rating  = int(input("  Candidate interview self-rating (1-5): "))
    print("  Recruiter observations — rate each as: low | medium | high")
    eng     = input("    Engagement level during interviews: ").strip()
    spd     = input("    Process speed & organisation: ").strip()
    resp    = input("    Post-interview responsiveness: ").strip()
    iq      = input("    Interviewer quality perceived: ").strip()
    gap     = float(input("  Offer-to-joining gap (days): "))
    print("  Engagement during gap: strong | moderate | minimal | none")
    eng_gap = input("  Engagement during gap: ").strip()
    print("  Career move type: clear_promotion | stretch_role | lateral_move")
    move    = input("  Career move type: ").strip()
    print("  Goal alignment: perfect_match | partial_match | indifferent | does_not_match | compromise")
    align   = input("  Goal alignment: ").strip()
    print("  Push factor options:")
    print("    toxic_environment | no_growth | company_instability | compensation_below_market")
    print("    role_changed_against_will | personal_relocation | no_push")
    push    = input("  Push factor: ").strip()
    print("  Pull factor options:")
    print("    dream_company | career_step_up | domain_passion | better_ctc")
    print("    better_wlb | referred_by_network | no_pull")
    pull    = input("  Pull factor: ").strip()
    p3_inputs = {
        "candidate_interview_rating": rating,
        "recruiter_observations"    : {
            "engagement"          : eng,
            "process_speed"       : spd,
            "responsiveness"      : resp,
            "interviewer_quality" : iq,
        },
        "offer_to_joining_days"     : gap,
        "engagement_during_gap"     : eng_gap,
        "career_move_type"          : move,
        "goal_alignment"            : align,
        "push_factor"               : push,
        "pull_factor"               : pull,
    }

    # --- P4
    print("\n--- P4: Counter-offer, Warmth & Stability ---")
    print("  Company type: top_brand | mid_size | early_startup | small_business")
    c_type  = input("  Current company type: ").strip()
    print("  Seniority level:")
    print("    csuite_vp_director | senior_manager_lead | manager_senior_ic | mid_level_ic | junior_entry")
    sen     = input("  Seniority level: ").strip()
    c_ten   = float(input("  Tenure at current company (years): "))
    w_rate  = int(input("  Recruiter warmth self-rating (1-5): "))
    print("  Warmth boosters (comma-separated, or leave blank):")
    print("    referred_someone | shared_personal_news | asked_joining_advice")
    print("    formalities_ahead_of_schedule | prior_placement")
    booster_raw = input("  Warmth boosters: ").strip()
    boosters = [b.strip() for b in booster_raw.split(",") if b.strip()] if booster_raw else []
    avg_ten = float(input("  Average tenure per company across career (years): "))
    print("  Stability modifiers (comma-separated, or leave blank):")
    print("    startups_shut_down | contract_roles | early_career_only | recent_trend_stable")
    print("    multiple_offer_drops | left_within_3_months | current_role_5_plus_yrs")
    stab_raw = input("  Stability modifiers: ").strip()
    stab_mods = [s.strip() for s in stab_raw.split(",") if s.strip()] if stab_raw else []
    p4_inputs = {
        "company_type"        : c_type,
        "seniority_level"     : sen,
        "current_tenure_years": c_ten,
        "warmth_rating"       : w_rate,
        "warmth_boosters"     : boosters,
        "avg_tenure_years"    : avg_ten,
        "stability_modifiers" : stab_mods,
    }

    return name, p0_inputs, p1_inputs, p2_inputs, p3_inputs, p4_inputs


# ---------------------------------------------------------------------------
# Demo Candidates
# ---------------------------------------------------------------------------

DEMO_CANDIDATES = [
    {
        "name": "Rahul Sharma",
        "note": "Strong candidate -- good hike, same city, no competition",
        "p0": {"current_ctc": 8,  "new_ctc": 14.4},
        "p1": {"relocation_type": "same_city",   "city_tier": 1,
               "family_profile": "married_no_children",
               "competing_offers": 0, "offer_strength": "best"},
        "p2": {"notice_period_days": 30, "buyout_situation": "not_available",
               "current_brand": "average", "new_brand": "top",
               "work_mode_preference": "prefers_hybrid", "work_mode_offered": "hybrid",
               "partner_profile": "not_applicable", "relocation_type": "same_city"},
        "p3": {"candidate_interview_rating": 5,
               "recruiter_observations": {"engagement": "high", "process_speed": "high",
                                          "responsiveness": "high", "interviewer_quality": "high"},
               "offer_to_joining_days": 30, "engagement_during_gap": "strong",
               "career_move_type": "clear_promotion", "goal_alignment": "perfect_match",
               "push_factor": "no_growth", "pull_factor": "dream_company"},
        "p4": {"company_type": "mid_size", "seniority_level": "mid_level_ic",
               "current_tenure_years": 2, "warmth_rating": 5,
               "warmth_boosters": ["referred_someone", "asked_joining_advice"],
               "avg_tenure_years": 2.5, "stability_modifiers": []},
    },
    {
        "name": "Priya Mehta",
        "note": "High risk -- relocation, school kids, 90d notice, 3 competing offers",
        "p0": {"current_ctc": 22, "new_ctc": 30.8},
        "p1": {"relocation_type": "diff_state",  "city_tier": 1,
               "family_profile": "married_school_children",
               "competing_offers": 3, "offer_strength": "equal"},
        "p2": {"notice_period_days": 90, "buyout_situation": "not_available",
               "current_brand": "top", "new_brand": "average",
               "work_mode_preference": "prefers_remote", "work_mode_offered": "full_office",
               "partner_profile": "employed_niche_role", "relocation_type": "diff_state"},
        "p3": {"candidate_interview_rating": 3,
               "recruiter_observations": {"engagement": "medium", "process_speed": "low",
                                          "responsiveness": "low", "interviewer_quality": "medium"},
               "offer_to_joining_days": 100, "engagement_during_gap": "minimal",
               "career_move_type": "lateral_move", "goal_alignment": "does_not_match",
               "push_factor": "compensation_below_market", "pull_factor": "better_ctc"},
        "p4": {"company_type": "top_brand", "seniority_level": "manager_senior_ic",
               "current_tenure_years": 6, "warmth_rating": 2,
               "warmth_boosters": [],
               "avg_tenure_years": 4.0, "stability_modifiers": []},
    },
    {
        "name": "Arjun Nair",
        "note": "Moderate -- decent hike, startup, single, neutral signals",
        "p0": {"current_ctc": 15, "new_ctc": 22.5},
        "p1": {"relocation_type": "diff_city_same_state", "city_tier": 2,
               "family_profile": "single_no_children",
               "competing_offers": 1, "offer_strength": "equal"},
        "p2": {"notice_period_days": 45, "buyout_situation": "available_unsure",
               "current_brand": "average", "new_brand": "average",
               "work_mode_preference": "no_preference", "work_mode_offered": "hybrid",
               "partner_profile": "not_applicable", "relocation_type": "diff_city_same_state"},
        "p3": {"candidate_interview_rating": 3,
               "recruiter_observations": {"engagement": "medium", "process_speed": "medium",
                                          "responsiveness": "medium", "interviewer_quality": "medium"},
               "offer_to_joining_days": 50, "engagement_during_gap": "moderate",
               "career_move_type": "stretch_role", "goal_alignment": "partial_match",
               "push_factor": "no_growth", "pull_factor": "better_ctc"},
        "p4": {"company_type": "early_startup", "seniority_level": "mid_level_ic",
               "current_tenure_years": 2, "warmth_rating": 3,
               "warmth_boosters": ["asked_joining_advice"],
               "avg_tenure_years": 2.0, "stability_modifiers": ["startups_shut_down"]},
    },
]


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def run_demo():
    """Run the model on all demo candidates."""
    print("\n" + "=" * 60)
    print("  RUNNING DEMO — 3 SAMPLE CANDIDATES")
    print("=" * 60)

    for candidate in DEMO_CANDIDATES:
        print("\n  >> {}  |  {}".format(candidate["name"], candidate["note"]))
        result = calculate_joining_probability(
            candidate_name = candidate["name"],
            p0_inputs      = candidate["p0"],
            p1_inputs      = candidate["p1"],
            p2_inputs      = candidate["p2"],
            p3_inputs      = candidate["p3"],
            p4_inputs      = candidate["p4"],
        )
        display_result(result)
        display_detailed(result)


def run_interactive():
    """Collect inputs from user and score a single candidate."""
    try:
        name, p0, p1, p2, p3, p4 = collect_candidate()
        result = calculate_joining_probability(
            candidate_name = name,
            p0_inputs      = p0,
            p1_inputs      = p1,
            p2_inputs      = p2,
            p3_inputs      = p3,
            p4_inputs      = p4,
        )
        display_result(result)
        show_detail = input("Show detailed breakdown? (y/n): ").strip().lower()
        if show_detail == "y":
            display_detailed(result)
    except KeyboardInterrupt:
        print("\n\nExited.")
    except Exception as e:
        print("\nError: {}".format(e))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  OFFER ACCEPTANCE PREDICTION MODEL")
    print("=" * 60)
    print("\n  1. Run demo (3 sample candidates)")
    print("  2. Enter a new candidate manually")


    
    run_demo()
    