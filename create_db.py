"""
Recruitment & Retention Prediction Database
============================================
Single SQLite database with two main tables:

1. candidates        -- master record for every candidate
2. interview_scores  -- interview evaluation (your existing chat data)
3. prediction_inputs -- P0-P4 model inputs
4. prediction_results-- final scores and outcomes

Run: python create_db.py
"""

import sqlite3
import json
import os

DB_PATH = "recruitment.db"


def create_database(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c    = conn.cursor()

    # -----------------------------------------------------------------------
    # Table 1: candidates
    # Master record — one row per candidate
    # -----------------------------------------------------------------------
    c.executescript("""
    CREATE TABLE IF NOT EXISTS candidates (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        name                TEXT    NOT NULL,
        email               TEXT,
        phone               TEXT,
        experience_years    REAL,
        current_company     TEXT,
        current_role        TEXT,
        technology_stack    TEXT,   -- comma-separated e.g. "LWC, Apex, Salesforce"
        source              TEXT,   -- how they came in: referral / portal / agency
        created_at          TEXT    DEFAULT (datetime('now')),
        updated_at          TEXT    DEFAULT (datetime('now')),
        notes               TEXT    -- free-text notes
    );

    -- -----------------------------------------------------------------------
    -- Table 2: interview_scores
    -- Stores your existing chat-style interview evaluation data
    -- -----------------------------------------------------------------------
    CREATE TABLE IF NOT EXISTS interview_scores (
        id                          INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id                INTEGER NOT NULL REFERENCES candidates(id),
        interview_date              TEXT,
        interviewer_name            TEXT,
        status                      TEXT,   -- Approved / Rejected / On Hold
        -- Scored dimensions (0.0 - 5.0)
        communication_confidence    REAL,
        apex_score                  REAL,
        scenario_problem_solving    REAL,
        lwc_score                   REAL,
        -- Add more skill dimensions as needed
        extra_skill_1_name          TEXT,
        extra_skill_1_score         REAL,
        extra_skill_2_name          TEXT,
        extra_skill_2_score         REAL,
        -- Overall
        overall_score               REAL,   -- auto-calculated average or manual
        rejection_reason            TEXT,   -- e.g. "Caught cheating", "Poor communication"
        interview_notes             TEXT,   -- free-text notes
        created_at                  TEXT    DEFAULT (datetime('now'))
    );

    -- -----------------------------------------------------------------------
    -- Table 3: prediction_inputs
    -- Stores all P0-P4 inputs for the offer acceptance model
    -- -----------------------------------------------------------------------
    CREATE TABLE IF NOT EXISTS prediction_inputs (
        id                          INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id                INTEGER NOT NULL REFERENCES candidates(id),
        input_date                  TEXT    DEFAULT (datetime('now')),

        -- P0: CTC
        current_ctc_lpa             REAL,
        new_ctc_lpa                 REAL,
        hike_pct                    REAL,   -- auto-calculated

        -- P1: Location, Family & Competing Offers
        relocation_type             TEXT,
        city_tier                   INTEGER,
        family_profile              TEXT,
        competing_offers            INTEGER,
        offer_strength              TEXT,

        -- P2: Notice, Brand, Work Mode & Partner
        notice_period_days          REAL,
        buyout_situation            TEXT,
        current_brand               TEXT,
        new_brand                   TEXT,
        work_mode_preference        TEXT,
        work_mode_offered           TEXT,
        partner_profile             TEXT,

        -- P3: Interview Experience & Motivation
        candidate_interview_rating  INTEGER,
        recruiter_obs_engagement    TEXT,
        recruiter_obs_process_speed TEXT,
        recruiter_obs_responsiveness TEXT,
        recruiter_obs_interviewer_quality TEXT,
        offer_to_joining_days       REAL,
        engagement_during_gap       TEXT,
        career_move_type            TEXT,
        goal_alignment              TEXT,
        push_factor                 TEXT,
        pull_factor                 TEXT,

        -- P4: Counter-offer, Warmth & Stability
        company_type                TEXT,
        seniority_level             TEXT,
        current_tenure_years        REAL,
        warmth_rating               INTEGER,
        warmth_boosters             TEXT,   -- stored as JSON array string
        avg_tenure_years            REAL,
        stability_modifiers         TEXT,   -- stored as JSON array string

        notes                       TEXT
    );

    -- -----------------------------------------------------------------------
    -- Table 4: prediction_results
    -- Stores computed scores and actual outcome
    -- -----------------------------------------------------------------------
    CREATE TABLE IF NOT EXISTS prediction_results (
        id                          INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id                INTEGER NOT NULL REFERENCES candidates(id),
        prediction_input_id         INTEGER REFERENCES prediction_inputs(id),
        scored_at                   TEXT    DEFAULT (datetime('now')),

        -- Individual parameter scores
        p0_score                    INTEGER,
        p1_score                    INTEGER,
        p2_score                    INTEGER,
        p3_score                    INTEGER,
        p4_score                    INTEGER,

        -- Weighted contributions
        p0_weighted                 REAL,
        p1_weighted                 REAL,
        p2_weighted                 REAL,
        p3_weighted                 REAL,
        p4_weighted                 REAL,

        -- Final output
        final_score                 INTEGER,
        joining_level               TEXT,   -- Very High / High / Moderate / Low / Very Low
        joining_probability         TEXT,   -- ">85%" etc
        recommended_action          TEXT,
        risk_flag                   TEXT,   -- NULL if no risk, else warning text

        -- Actual outcome (filled in later once known)
        actual_outcome              TEXT,   -- "joined" / "dropped" / "pending"
        actual_outcome_date         TEXT,
        outcome_notes               TEXT,

        -- Full breakdown stored as JSON for audit trail
        full_breakdown_json         TEXT
    );

    -- -----------------------------------------------------------------------
    -- Indexes for fast lookup
    -- -----------------------------------------------------------------------
    CREATE INDEX IF NOT EXISTS idx_candidates_name
        ON candidates(name);

    CREATE INDEX IF NOT EXISTS idx_interview_candidate
        ON interview_scores(candidate_id);

    CREATE INDEX IF NOT EXISTS idx_prediction_candidate
        ON prediction_inputs(candidate_id);

    CREATE INDEX IF NOT EXISTS idx_results_candidate
        ON prediction_results(candidate_id);

    CREATE INDEX IF NOT EXISTS idx_results_outcome
        ON prediction_results(actual_outcome);
    """)

    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Insert Helpers
# ---------------------------------------------------------------------------

def insert_candidate(conn, name, experience_years=None, email=None,
                     phone=None, current_company=None, current_role=None,
                     technology_stack=None, source=None, notes=None):
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidates
            (name, email, phone, experience_years, current_company,
             current_role, technology_stack, source, notes)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (name, email, phone, experience_years, current_company,
          current_role, technology_stack, source, notes))
    conn.commit()
    return c.lastrowid


def insert_interview(conn, candidate_id, status,
                     communication_confidence=None, apex_score=None,
                     scenario_problem_solving=None, lwc_score=None,
                     overall_score=None, rejection_reason=None,
                     interview_notes=None, interview_date=None,
                     interviewer_name=None,
                     extra_skill_1_name=None, extra_skill_1_score=None,
                     extra_skill_2_name=None, extra_skill_2_score=None):
    c = conn.cursor()

    # Auto-calculate overall if not provided and scores exist
    if overall_score is None:
        scores = [s for s in [communication_confidence, apex_score,
                               scenario_problem_solving, lwc_score] if s is not None]
        if scores:
            overall_score = round(sum(scores) / len(scores), 2)

    c.execute("""
        INSERT INTO interview_scores
            (candidate_id, interview_date, interviewer_name, status,
             communication_confidence, apex_score, scenario_problem_solving,
             lwc_score, extra_skill_1_name, extra_skill_1_score,
             extra_skill_2_name, extra_skill_2_score,
             overall_score, rejection_reason, interview_notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (candidate_id, interview_date, interviewer_name, status,
          communication_confidence, apex_score, scenario_problem_solving,
          lwc_score, extra_skill_1_name, extra_skill_1_score,
          extra_skill_2_name, extra_skill_2_score,
          overall_score, rejection_reason, interview_notes))
    conn.commit()
    return c.lastrowid


def insert_prediction(conn, candidate_id, p_inputs):
    """
    p_inputs: dict with keys matching the prediction_inputs columns.
    Accepts the same structure as main.py demo candidates.
    """
    c = conn.cursor()

    p0 = p_inputs.get("p0", {})
    p1 = p_inputs.get("p1", {})
    p2 = p_inputs.get("p2", {})
    p3 = p_inputs.get("p3", {})
    p4 = p_inputs.get("p4", {})
    ro = p3.get("recruiter_observations", {})

    current_ctc = p0.get("current_ctc", 0)
    new_ctc     = p0.get("new_ctc", 0)
    hike_pct    = round(((new_ctc - current_ctc) / current_ctc) * 100, 2) if current_ctc else None

    c.execute("""
        INSERT INTO prediction_inputs (
            candidate_id,
            current_ctc_lpa, new_ctc_lpa, hike_pct,
            relocation_type, city_tier, family_profile,
            competing_offers, offer_strength,
            notice_period_days, buyout_situation,
            current_brand, new_brand,
            work_mode_preference, work_mode_offered, partner_profile,
            candidate_interview_rating,
            recruiter_obs_engagement, recruiter_obs_process_speed,
            recruiter_obs_responsiveness, recruiter_obs_interviewer_quality,
            offer_to_joining_days, engagement_during_gap,
            career_move_type, goal_alignment,
            push_factor, pull_factor,
            company_type, seniority_level, current_tenure_years,
            warmth_rating, warmth_boosters,
            avg_tenure_years, stability_modifiers,
            notes
        ) VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
    """, (
        candidate_id,
        current_ctc, new_ctc, hike_pct,
        p1.get("relocation_type"), p1.get("city_tier"), p1.get("family_profile"),
        p1.get("competing_offers"), p1.get("offer_strength"),
        p2.get("notice_period_days"), p2.get("buyout_situation"),
        p2.get("current_brand"), p2.get("new_brand"),
        p2.get("work_mode_preference"), p2.get("work_mode_offered"),
        p2.get("partner_profile"),
        p3.get("candidate_interview_rating"),
        ro.get("engagement"), ro.get("process_speed"),
        ro.get("responsiveness"), ro.get("interviewer_quality"),
        p3.get("offer_to_joining_days"), p3.get("engagement_during_gap"),
        p3.get("career_move_type"), p3.get("goal_alignment"),
        p3.get("push_factor"), p3.get("pull_factor"),
        p4.get("company_type"), p4.get("seniority_level"),
        p4.get("current_tenure_years"), p4.get("warmth_rating"),
        json.dumps(p4.get("warmth_boosters", [])),
        p4.get("avg_tenure_years"),
        json.dumps(p4.get("stability_modifiers", [])),
        p_inputs.get("note")
    ))
    conn.commit()
    return c.lastrowid


def insert_result(conn, candidate_id, prediction_input_id, result_dict):
    """Save the output of calculate_joining_probability() to the DB."""
    c = conn.cursor()
    c.execute("""
        INSERT INTO prediction_results (
            candidate_id, prediction_input_id,
            p0_score, p1_score, p2_score, p3_score, p4_score,
            p0_weighted, p1_weighted, p2_weighted, p3_weighted, p4_weighted,
            final_score, joining_level, joining_probability,
            recommended_action, risk_flag,
            actual_outcome, full_breakdown_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        candidate_id, prediction_input_id,
        result_dict["p0_score"], result_dict["p1_score"],
        result_dict["p2_score"], result_dict["p3_score"], result_dict["p4_score"],
        result_dict["p0_weighted"], result_dict["p1_weighted"],
        result_dict["p2_weighted"], result_dict["p3_weighted"], result_dict["p4_weighted"],
        result_dict["final_score"], result_dict["joining_level"],
        result_dict["joining_probability"], result_dict["recommended_action"],
        result_dict.get("risk_flag"),
        "pending",
        json.dumps({
            "p0": result_dict["p0_breakdown"],
            "p1": result_dict["p1_breakdown"],
            "p2": result_dict["p2_breakdown"],
            "p3": result_dict["p3_breakdown"],
            "p4": result_dict["p4_breakdown"],
        }, default=str)
    ))
    conn.commit()
    return c.lastrowid


def update_outcome(conn, prediction_result_id, actual_outcome, outcome_notes=None):
    """Call this once you know if the candidate joined or dropped."""
    c = conn.cursor()
    c.execute("""
        UPDATE prediction_results
        SET actual_outcome      = ?,
            actual_outcome_date = datetime('now'),
            outcome_notes       = ?
        WHERE id = ?
    """, (actual_outcome, outcome_notes, prediction_result_id))
    conn.commit()


# ---------------------------------------------------------------------------
# Seed: Past Interview Data from Chat History
# ---------------------------------------------------------------------------

def seed_past_interviews(conn):
    """Load your existing candidate data from chat history."""

    past_candidates = [
        {
            "name": "Naman Puri",
            "experience_years": 4,
            "technology_stack": "LWC, Apex, Salesforce",
            "status": "Approved",
            "communication_confidence": 4.0,
            "apex_score": 3.5,
            "scenario_problem_solving": 3.5,
            "lwc_score": 4.0,
            "interview_notes": "Good understanding on LWC, Apex. Able to communicate well.",
        },
        {
            "name": "Abhinav Parate",
            "experience_years": 3,
            "technology_stack": "Salesforce",
            "status": "Rejected",
            "communication_confidence": None,
            "apex_score": None,
            "scenario_problem_solving": None,
            "lwc_score": None,
            "rejection_reason": "Caught Cheating",
            "interview_notes": "Was reading from the mobile/pc screen during interview.",
        },
    ]

    print("Seeding past interview data...")
    for cd in past_candidates:
        cid = insert_candidate(
            conn,
            name               = cd["name"],
            experience_years   = cd.get("experience_years"),
            technology_stack   = cd.get("technology_stack"),
        )
        insert_interview(
            conn,
            candidate_id             = cid,
            status                   = cd["status"],
            communication_confidence = cd.get("communication_confidence"),
            apex_score               = cd.get("apex_score"),
            scenario_problem_solving = cd.get("scenario_problem_solving"),
            lwc_score                = cd.get("lwc_score"),
            rejection_reason         = cd.get("rejection_reason"),
            interview_notes          = cd.get("interview_notes"),
        )
        print("  Inserted: {}  ({})".format(cd["name"], cd["status"]))


# ---------------------------------------------------------------------------
# Seed: Demo Prediction Candidates from main.py
# ---------------------------------------------------------------------------

def seed_prediction_candidates(conn):
    """Load the 3 demo candidates from main.py into the DB."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from main import DEMO_CANDIDATES, calculate_joining_probability

    print("\nSeeding prediction model candidates...")
    for cd in DEMO_CANDIDATES:
        cid = insert_candidate(
            conn,
            name  = cd["name"],
            notes = cd.get("note"),
        )
        pid = insert_prediction(conn, cid, cd)
        result = calculate_joining_probability(
            candidate_name = cd["name"],
            p0_inputs      = cd["p0"],
            p1_inputs      = cd["p1"],
            p2_inputs      = cd["p2"],
            p3_inputs      = cd["p3"],
            p4_inputs      = cd["p4"],
        )
        insert_result(conn, cid, pid, result)
        print("  Inserted: {}  (Final Score: {})".format(
            cd["name"], result["final_score"]))


# ---------------------------------------------------------------------------
# Quick Query: View All Candidates
# ---------------------------------------------------------------------------

def view_all(conn):
    c = conn.cursor()

    print("\n" + "=" * 70)
    print("  ALL CANDIDATES")
    print("=" * 70)

    # Interview candidates
    print("\n  INTERVIEW RECORDS")
    print("  {:<25} {:<6} {:<10} {:<8} {:<6}".format(
        "Name", "Exp", "Status", "Overall", "Tech"))
    print("  " + "-" * 60)
    rows = c.execute("""
        SELECT ca.name, ca.experience_years, i.status,
               i.overall_score, ca.technology_stack
        FROM candidates ca
        JOIN interview_scores i ON i.candidate_id = ca.id
        ORDER BY ca.created_at
    """).fetchall()
    for row in rows:
        print("  {:<25} {:<6} {:<10} {:<8} {:<6}".format(
            row[0],
            str(row[1]) + " yrs" if row[1] else "—",
            row[2] or "—",
            str(row[3]) + "/5" if row[3] else "—",
            row[4] or "—"
        ))

    # Prediction candidates
    print("\n  PREDICTION MODEL RECORDS")
    print("  {:<20} {:>6} {:>6} {:>6} {:>6} {:>6} {:>7} {:<10} {:<10}".format(
        "Name", "P0", "P1", "P2", "P3", "P4", "Final", "Level", "Outcome"))
    print("  " + "-" * 85)
    rows = c.execute("""
        SELECT ca.name,
               r.p0_score, r.p1_score, r.p2_score, r.p3_score, r.p4_score,
               r.final_score, r.joining_level, r.actual_outcome
        FROM candidates ca
        JOIN prediction_results r ON r.candidate_id = ca.id
        ORDER BY r.final_score DESC
    """).fetchall()
    for row in rows:
        print("  {:<20} {:>6} {:>6} {:>6} {:>6} {:>6} {:>7} {:<10} {:<10}".format(
            row[0], row[1], row[2], row[3], row[4], row[5],
            row[6], row[7] or "—", row[8] or "pending"))

    print("\n" + "=" * 70 + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Remove old DB if re-running
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing DB.")

    print("Creating database: {}".format(DB_PATH))
    conn = create_database(DB_PATH)
    print("Tables created.")

    seed_past_interviews(conn)
    seed_prediction_candidates(conn)
    view_all(conn)

    print("Database ready at: {}/{}".format(os.getcwd(), DB_PATH))
    conn.close()