"""
Recruitment Dashboard — Flask Backend
=====================================
Run: pip install flask --break-system-packages && python app.py
Then open: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3, json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_db import (create_database, insert_candidate, insert_interview,
                       insert_prediction, insert_result, update_outcome)
from main import calculate_joining_probability

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recruitment.db")
app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── HTML ────────────────────────────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TalentOS — Recruitment Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg:       #0a0a0f;
  --surface:  #111118;
  --card:     #16161f;
  --border:   #23232f;
  --border2:  #2e2e3e;
  --accent:   #7c6cfc;
  --accent2:  #b06cfc;
  --green:    #3ecf8e;
  --red:      #fc6c6c;
  --amber:    #fcb96c;
  --text:     #e8e8f0;
  --muted:    #7070a0;
  --dim:      #3a3a5a;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif;
       font-size: 14px; line-height: 1.6; min-height: 100vh; }

/* ── LAYOUT ── */
.shell { display: flex; min-height: 100vh; }
.sidebar { width: 220px; background: var(--surface); border-right: 1px solid var(--border);
           display: flex; flex-direction: column; padding: 0; flex-shrink: 0; position: sticky;
           top: 0; height: 100vh; }
.logo { padding: 24px 20px 20px; border-bottom: 1px solid var(--border); }
.logo-mark { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 18px;
             background: linear-gradient(135deg, var(--accent), var(--accent2));
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.logo-sub { font-size: 10px; color: var(--muted); letter-spacing: 0.1em;
            text-transform: uppercase; margin-top: 2px; font-family: 'DM Mono', monospace; }
nav { flex: 1; padding: 12px 0; }
.nav-section { padding: 8px 20px 4px; font-size: 10px; font-family: 'DM Mono', monospace;
               letter-spacing: 0.12em; color: var(--dim); text-transform: uppercase; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 9px 20px;
            cursor: pointer; color: var(--muted); transition: all 0.15s; font-size: 13px;
            border-left: 2px solid transparent; }
.nav-item:hover { color: var(--text); background: rgba(124,108,252,0.06); }
.nav-item.active { color: var(--accent); border-left-color: var(--accent);
                   background: rgba(124,108,252,0.08); }
.nav-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; flex-shrink: 0; }
.main { flex: 1; overflow-y: auto; }
.page { display: none; padding: 32px 36px; }
.page.active { display: block; }

/* ── HEADER ── */
.page-header { margin-bottom: 28px; }
.page-title { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; }
.page-sub { color: var(--muted); font-size: 13px; margin-top: 4px; }

/* ── STATS ROW ── */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 28px; }
.stat-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
             padding: 18px 20px; }
.stat-label { font-size: 11px; font-family: 'DM Mono', monospace; color: var(--muted);
              text-transform: uppercase; letter-spacing: 0.08em; }
.stat-val { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 700; margin-top: 6px; }
.stat-val.green { color: var(--green); }
.stat-val.red   { color: var(--red); }
.stat-val.amber { color: var(--amber); }
.stat-val.purple{ color: var(--accent); }

/* ── TABLE ── */
.table-wrap { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
              overflow: hidden; }
.table-head { padding: 14px 20px; border-bottom: 1px solid var(--border);
              display: flex; align-items: center; justify-content: space-between; }
.table-title { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 14px; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 10px 16px; font-size: 10px; font-family: 'DM Mono', monospace;
     color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em;
     border-bottom: 1px solid var(--border); background: var(--surface); }
td { padding: 11px 16px; border-bottom: 1px solid var(--border); font-size: 13px; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

/* ── BADGES ── */
.badge { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 11px;
         font-family: 'DM Mono', monospace; font-weight: 500; }
.badge-green  { background: rgba(62,207,142,0.12); color: var(--green); }
.badge-red    { background: rgba(252,108,108,0.12); color: var(--red); }
.badge-amber  { background: rgba(252,185,108,0.12); color: var(--amber); }
.badge-purple { background: rgba(124,108,252,0.12); color: var(--accent); }
.badge-dim    { background: rgba(112,112,160,0.12); color: var(--muted); }

/* ── SCORE BAR ── */
.score-bar { display: flex; align-items: center; gap: 8px; }
.bar-track { flex: 1; height: 4px; background: var(--border2); border-radius: 2px; min-width: 60px; }
.bar-fill  { height: 100%; border-radius: 2px; transition: width 0.4s; }
.score-num { font-family: 'DM Mono', monospace; font-size: 12px; min-width: 28px; text-align: right; }

/* ── FORMS ── */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-grid.three { grid-template-columns: 1fr 1fr 1fr; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full { grid-column: 1 / -1; }
label { font-size: 11px; font-family: 'DM Mono', monospace; color: var(--muted);
        text-transform: uppercase; letter-spacing: 0.08em; }
input, select, textarea {
  background: var(--surface); border: 1px solid var(--border2); border-radius: 7px;
  color: var(--text); padding: 9px 12px; font-size: 13px; font-family: 'DM Sans', sans-serif;
  transition: border-color 0.15s; width: 100%; }
input:focus, select:focus, textarea:focus {
  outline: none; border-color: var(--accent); box-shadow: 0 0 0 2px rgba(124,108,252,0.15); }
select option { background: var(--card); }
textarea { resize: vertical; min-height: 72px; }
.form-section { margin-bottom: 24px; }
.form-section-title { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600;
                      color: var(--accent); margin-bottom: 14px; padding-bottom: 8px;
                      border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; }
.form-section-title::before { content: ''; display: block; width: 3px; height: 14px;
                               background: var(--accent); border-radius: 2px; }

/* ── BUTTONS ── */
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 18px;
       border-radius: 7px; font-size: 13px; font-weight: 500; cursor: pointer;
       border: none; transition: all 0.15s; font-family: 'DM Sans', sans-serif; }
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent2); transform: translateY(-1px); }
.btn-ghost { background: transparent; color: var(--muted); border: 1px solid var(--border2); }
.btn-ghost:hover { color: var(--text); border-color: var(--dim); }
.btn-sm { padding: 5px 12px; font-size: 12px; }
.btn-green { background: rgba(62,207,142,0.15); color: var(--green); border: 1px solid rgba(62,207,142,0.2); }
.btn-green:hover { background: rgba(62,207,142,0.25); }

/* ── CARD ── */
.card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 24px; }
.card + .card { margin-top: 16px; }

/* ── TABS ── */
.tabs { display: flex; gap: 2px; background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 3px; margin-bottom: 24px; width: fit-content; }
.tab { padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 13px;
       color: var(--muted); transition: all 0.15s; }
.tab.active { background: var(--card); color: var(--text); }

/* ── RESULT CARD ── */
.result-banner { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
                 padding: 24px; margin-bottom: 16px; display: none; }
.result-banner.show { display: block; }
.result-score { font-family: 'Syne', sans-serif; font-size: 48px; font-weight: 800; line-height: 1; }
.result-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 20px; }
.result-param { background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
                padding: 12px; text-align: center; }
.result-param-label { font-size: 10px; font-family: 'DM Mono', monospace; color: var(--muted);
                      text-transform: uppercase; margin-bottom: 6px; }
.result-param-score { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; }

/* ── ALERT ── */
.alert { padding: 12px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 16px;
         display: none; }
.alert.show { display: block; }
.alert-success { background: rgba(62,207,142,0.1); border: 1px solid rgba(62,207,142,0.2); color: var(--green); }
.alert-error   { background: rgba(252,108,108,0.1); border: 1px solid rgba(252,108,108,0.2); color: var(--red); }
.alert-warn    { background: rgba(252,185,108,0.1); border: 1px solid rgba(252,185,108,0.2); color: var(--amber); }

/* ── CHECKBOX GROUP ── */
.check-group { display: flex; flex-wrap: wrap; gap: 8px; }
.check-item { display: flex; align-items: center; gap: 6px; background: var(--surface);
              border: 1px solid var(--border2); border-radius: 6px; padding: 6px 10px;
              cursor: pointer; transition: all 0.15s; }
.check-item:hover { border-color: var(--accent); }
.check-item input { width: auto; accent-color: var(--accent); cursor: pointer; }
.check-item span { font-size: 12px; font-family: 'DM Mono', monospace; color: var(--muted); }
.check-item:has(input:checked) { border-color: var(--accent); background: rgba(124,108,252,0.08); }
.check-item:has(input:checked) span { color: var(--accent); }

.form-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 24px;
                padding-top: 20px; border-top: 1px solid var(--border); }
.spinner { display: none; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.2);
           border-top-color: #fff; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty { text-align: center; padding: 40px; color: var(--muted); font-size: 13px; }
</style>
</head>
<body>
<div class="shell">

<!-- SIDEBAR -->
<aside class="sidebar">
  <div class="logo">
    <div class="logo-mark">TalentOS</div>
    <div class="logo-sub">Recruitment Intelligence</div>
  </div>
  <nav>
    <div class="nav-section">Overview</div>
    <div class="nav-item active" onclick="showPage('dashboard')">
      <div class="nav-dot"></div> Dashboard
    </div>
    <div class="nav-section">Add Data</div>
    <div class="nav-item" onclick="showPage('add-interview')">
      <div class="nav-dot"></div> Interview Record
    </div>
    <div class="nav-item" onclick="showPage('add-prediction')">
      <div class="nav-dot"></div> Prediction Model
    </div>
    <div class="nav-section">Records</div>
    <div class="nav-item" onclick="showPage('interviews')">
      <div class="nav-dot"></div> All Interviews
    </div>
    <div class="nav-item" onclick="showPage('predictions')">
      <div class="nav-dot"></div> All Predictions
    </div>
  </nav>
</aside>

<!-- MAIN -->
<main class="main">

  <!-- DASHBOARD -->
  <div class="page active" id="page-dashboard">
    <div class="page-header">
      <div class="page-title">Dashboard</div>
      <div class="page-sub">Overview of all recruitment activity</div>
    </div>
    <div class="stats" id="stats-row">
      <div class="stat-card"><div class="stat-label">Total Candidates</div><div class="stat-val purple" id="stat-total">—</div></div>
      <div class="stat-card"><div class="stat-label">Approved</div><div class="stat-val green" id="stat-approved">—</div></div>
      <div class="stat-card"><div class="stat-label">Rejected</div><div class="stat-val red" id="stat-rejected">—</div></div>
      <div class="stat-card"><div class="stat-label">Predictions Run</div><div class="stat-val amber" id="stat-predictions">—</div></div>
    </div>
    <div class="table-wrap">
      <div class="table-head"><div class="table-title">Recent Candidates</div></div>
      <table><thead><tr>
        <th>Name</th><th>Experience</th><th>Status</th><th>Overall Score</th><th>Prediction</th><th>Joining Level</th>
      </tr></thead>
      <tbody id="dashboard-table"><tr><td colspan="6" class="empty">Loading...</td></tr></tbody></table>
    </div>
  </div>

  <!-- ADD INTERVIEW -->
  <div class="page" id="page-add-interview">
    <div class="page-header">
      <div class="page-title">Add Interview Record</div>
      <div class="page-sub">Record a new candidate's interview evaluation</div>
    </div>
    <div id="alert-interview" class="alert"></div>
    <form id="form-interview">
      <div class="card">
        <div class="form-section">
          <div class="form-section-title">Candidate Details</div>
          <div class="form-grid three">
            <div class="form-group"><label>Full Name *</label><input name="name" required placeholder="Naman Puri"></div>
            <div class="form-group"><label>Experience (Years)</label><input name="experience_years" type="number" step="0.5" placeholder="4"></div>
            <div class="form-group"><label>Email</label><input name="email" type="email" placeholder="naman@example.com"></div>
            <div class="form-group"><label>Phone</label><input name="phone" placeholder="+91 98765 43210"></div>
            <div class="form-group"><label>Current Company</label><input name="current_company" placeholder="Infosys"></div>
            <div class="form-group"><label>Current Role</label><input name="current_role" placeholder="Senior Developer"></div>
            <div class="form-group full"><label>Technology Stack (comma-separated)</label><input name="technology_stack" placeholder="LWC, Apex, Salesforce, JavaScript"></div>
            <div class="form-group"><label>Source</label>
              <select name="source">
                <option value="">— Select —</option>
                <option>Referral</option><option>Job Portal</option><option>Agency</option><option>LinkedIn</option><option>Direct Apply</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">Interview Evaluation</div>
          <div class="form-grid">
            <div class="form-group"><label>Interview Date</label><input name="interview_date" type="date"></div>
            <div class="form-group"><label>Interviewer Name</label><input name="interviewer_name" placeholder="Your name"></div>
            <div class="form-group"><label>Status *</label>
              <select name="status" required>
                <option value="">— Select —</option>
                <option>Approved</option><option>Rejected</option><option>On Hold</option>
              </select>
            </div>
            <div class="form-group"><label>Rejection Reason (if rejected)</label><input name="rejection_reason" placeholder="e.g. Caught cheating, Poor communication"></div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">Scores (out of 5)</div>
          <div class="form-grid">
            <div class="form-group"><label>Communication & Confidence</label><input name="communication_confidence" type="number" min="0" max="5" step="0.5" placeholder="4.0"></div>
            <div class="form-group"><label>Apex</label><input name="apex_score" type="number" min="0" max="5" step="0.5" placeholder="3.5"></div>
            <div class="form-group"><label>Scenarios & Problem Solving</label><input name="scenario_problem_solving" type="number" min="0" max="5" step="0.5" placeholder="3.5"></div>
            <div class="form-group"><label>LWC</label><input name="lwc_score" type="number" min="0" max="5" step="0.5" placeholder="4.0"></div>
            <div class="form-group"><label>Extra Skill 1 — Name</label><input name="extra_skill_1_name" placeholder="e.g. REST APIs"></div>
            <div class="form-group"><label>Extra Skill 1 — Score</label><input name="extra_skill_1_score" type="number" min="0" max="5" step="0.5" placeholder="3.5"></div>
            <div class="form-group"><label>Extra Skill 2 — Name</label><input name="extra_skill_2_name" placeholder="e.g. SQL"></div>
            <div class="form-group"><label>Extra Skill 2 — Score</label><input name="extra_skill_2_score" type="number" min="0" max="5" step="0.5" placeholder="3.5"></div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">Notes</div>
          <div class="form-group full"><textarea name="interview_notes" placeholder="Good understanding on LWC, Apex. Able to communicate well."></textarea></div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="resetForm('form-interview')">Clear</button>
          <button type="submit" class="btn btn-primary">
            <span class="spinner" id="spin-interview"></span> Save Interview Record
          </button>
        </div>
      </div>
    </form>
  </div>

  <!-- ADD PREDICTION -->
  <div class="page" id="page-add-prediction">
    <div class="page-header">
      <div class="page-title">Run Prediction Model</div>
      <div class="page-sub">Enter P0–P4 inputs and get the joining probability score</div>
    </div>
    <div id="alert-prediction" class="alert"></div>

    <!-- Result banner -->
    <div class="result-banner" id="result-banner">
      <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:20px;">
        <div>
          <div style="font-size:11px;font-family:'DM Mono',monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;">Final Score</div>
          <div class="result-score" id="res-score">—</div>
          <div style="margin-top:8px;display:flex;gap:8px;align-items:center;">
            <span class="badge badge-purple" id="res-level">—</span>
            <span style="color:var(--muted);font-size:12px;" id="res-prob">—</span>
          </div>
        </div>
        <div style="flex:1; padding-left:24px; border-left:1px solid var(--border);">
          <div style="font-size:11px;font-family:'DM Mono',monospace;color:var(--muted);text-transform:uppercase;margin-bottom:8px;">Recommended Action</div>
          <div style="font-size:13px;" id="res-action">—</div>
          <div id="res-risk" style="margin-top:8px;padding:8px 12px;background:rgba(252,108,108,0.1);border:1px solid rgba(252,108,108,0.2);border-radius:6px;color:var(--red);font-size:12px;display:none;"></div>
        </div>
      </div>
      <div class="result-grid" id="result-grid"></div>
    </div>

    <form id="form-prediction">
      <div class="card">
        <div class="form-section">
          <div class="form-section-title">Candidate</div>
          <div class="form-grid three">
            <div class="form-group"><label>Full Name *</label><input name="name" required placeholder="Arjun Nair"></div>
            <div class="form-group"><label>Note / Summary</label><input name="note" placeholder="Strong candidate, 4yr exp, Bangalore"></div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">P0 — CTC</div>
          <div class="form-grid">
            <div class="form-group"><label>Current CTC (LPA) *</label><input name="p0_current_ctc" type="number" step="0.1" required placeholder="15"></div>
            <div class="form-group"><label>New CTC Offered (LPA) *</label><input name="p0_new_ctc" type="number" step="0.1" required placeholder="22.5"></div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">P1 — Location, Family & Competing Offers</div>
          <div class="form-grid three">
            <div class="form-group"><label>Relocation Type *</label>
              <select name="p1_relocation_type" required>
                <option value="">— Select —</option>
                <option value="same_city">Same City</option>
                <option value="diff_city_same_state">Diff City, Same State</option>
                <option value="diff_state">Different State</option>
                <option value="abroad_with_family">Abroad with Family</option>
                <option value="abroad_without_family">Abroad without Family</option>
              </select>
            </div>
            <div class="form-group"><label>City Tier *</label>
              <select name="p1_city_tier" required>
                <option value="">— Select —</option>
                <option value="1">Tier 1 — High Expense (Mumbai, Bengaluru, Delhi)</option>
                <option value="2">Tier 2 — Mid Expense (Kolkata, Jaipur, Kochi)</option>
                <option value="3">Tier 3 — Low Expense (Other cities)</option>
              </select>
            </div>
            <div class="form-group"><label>Family Profile *</label>
              <select name="p1_family_profile" required>
                <option value="">— Select —</option>
                <option value="single_no_children">Single, No Children</option>
                <option value="single_with_children">Single, With Children</option>
                <option value="married_no_children">Married, No Children</option>
                <option value="married_school_children">Married, School-age Children</option>
                <option value="married_preschool_children">Married, Pre-school Children</option>
                <option value="married_adult_children">Married, Adult Children</option>
              </select>
            </div>
            <div class="form-group"><label>Competing Offers in Hand *</label>
              <select name="p1_competing_offers" required>
                <option value="">— Select —</option>
                <option value="0">0 — Only this offer</option>
                <option value="1">1 — One other offer</option>
                <option value="2">2 — Two other offers</option>
                <option value="3">3 — Three other offers</option>
                <option value="4">4+ — Four or more</option>
              </select>
            </div>
            <div class="form-group"><label>Offer Strength vs Others *</label>
              <select name="p1_offer_strength" required>
                <option value="">— Select —</option>
                <option value="best">Best — Clearly the best offer</option>
                <option value="equal">Equal — Roughly equal to others</option>
                <option value="weaker">Weaker — Weaker than at least one</option>
                <option value="weakest">Weakest — Weakest among all offers</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">P2 — Notice, Brand, Work Mode & Partner</div>
          <div class="form-grid three">
            <div class="form-group"><label>Notice Period (Days) *</label><input name="p2_notice_period_days" type="number" required placeholder="45"></div>
            <div class="form-group"><label>Buyout Situation *</label>
              <select name="p2_buyout_situation" required>
                <option value="">— Select —</option>
                <option value="available_willing">Available & Candidate Willing</option>
                <option value="available_unsure">Available but Unsure</option>
                <option value="not_available">Not Available</option>
                <option value="unwilling">Candidate Unwilling</option>
              </select>
            </div>
            <div class="form-group"><label>Current Company Brand *</label>
              <select name="p2_current_brand" required>
                <option value="">— Select —</option>
                <option value="top">Top Brand (FAANG / Large MNC)</option>
                <option value="average">Average Brand (Mid-size known)</option>
                <option value="unknown">Unknown Brand (Startup / SME)</option>
              </select>
            </div>
            <div class="form-group"><label>New Company Brand *</label>
              <select name="p2_new_brand" required>
                <option value="">— Select —</option>
                <option value="top">Top Brand</option>
                <option value="average">Average Brand</option>
                <option value="unknown">Unknown Brand</option>
              </select>
            </div>
            <div class="form-group"><label>Work Mode Preference *</label>
              <select name="p2_work_mode_preference" required>
                <option value="">— Select —</option>
                <option value="prefers_remote">Prefers Full Remote</option>
                <option value="prefers_hybrid">Prefers Hybrid</option>
                <option value="prefers_office">Prefers Full Office</option>
                <option value="no_preference">No Strong Preference</option>
              </select>
            </div>
            <div class="form-group"><label>Work Mode Offered *</label>
              <select name="p2_work_mode_offered" required>
                <option value="">— Select —</option>
                <option value="full_remote">Full Remote</option>
                <option value="hybrid">Hybrid (2–3 days)</option>
                <option value="full_office">Full Office / On-site</option>
                <option value="flexible">Flexible</option>
              </select>
            </div>
            <div class="form-group"><label>Partner Employment Profile *</label>
              <select name="p2_partner_profile" required>
                <option value="">— Select —</option>
                <option value="not_applicable">Not Applicable (Single)</option>
                <option value="not_employed">Partner Not Employed</option>
                <option value="employed_jobs_available">Partner Employed — Jobs Available</option>
                <option value="employed_niche_role">Partner Employed — Niche Role</option>
                <option value="employed_no_jobs">Partner Employed — No Jobs in New City</option>
                <option value="self_employed">Partner Self-employed / Freelancer</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">P3 — Interview Experience, Gap & Motivation</div>
          <div class="form-grid three">
            <div class="form-group"><label>Candidate Interview Rating (1–5) *</label>
              <select name="p3_candidate_interview_rating" required>
                <option value="">— Select —</option>
                <option value="5">5 — Excellent</option>
                <option value="4">4 — Good</option>
                <option value="3">3 — Neutral</option>
                <option value="2">2 — Poor</option>
                <option value="1">1 — Very Poor</option>
              </select>
            </div>
            <div class="form-group"><label>Engagement During Interviews *</label>
              <select name="p3_obs_engagement" required>
                <option value="">— Select —</option>
                <option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option>
              </select>
            </div>
            <div class="form-group"><label>Process Speed & Organisation *</label>
              <select name="p3_obs_process_speed" required>
                <option value="">— Select —</option>
                <option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option>
              </select>
            </div>
            <div class="form-group"><label>Post-interview Responsiveness *</label>
              <select name="p3_obs_responsiveness" required>
                <option value="">— Select —</option>
                <option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option>
              </select>
            </div>
            <div class="form-group"><label>Interviewer Quality Perceived *</label>
              <select name="p3_obs_interviewer_quality" required>
                <option value="">— Select —</option>
                <option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option>
              </select>
            </div>
            <div class="form-group"><label>Offer to Joining Gap (Days) *</label><input name="p3_offer_to_joining_days" type="number" required placeholder="45"></div>
            <div class="form-group"><label>Engagement During Gap *</label>
              <select name="p3_engagement_during_gap" required>
                <option value="">— Select —</option>
                <option value="strong">Strong</option><option value="moderate">Moderate</option>
                <option value="minimal">Minimal</option><option value="none">None</option>
              </select>
            </div>
            <div class="form-group"><label>Career Move Type *</label>
              <select name="p3_career_move_type" required>
                <option value="">— Select —</option>
                <option value="clear_promotion">Clear Promotion</option>
                <option value="stretch_role">Stretch Role</option>
                <option value="lateral_move">Lateral Move</option>
              </select>
            </div>
            <div class="form-group"><label>Goal Alignment *</label>
              <select name="p3_goal_alignment" required>
                <option value="">— Select —</option>
                <option value="perfect_match">Perfect Match</option>
                <option value="partial_match">Partial Match</option>
                <option value="indifferent">Indifferent</option>
                <option value="does_not_match">Does Not Match</option>
                <option value="compromise">Compromise</option>
              </select>
            </div>
            <div class="form-group"><label>Push Factor (Reason to Leave) *</label>
              <select name="p3_push_factor" required>
                <option value="">— Select —</option>
                <option value="toxic_environment">Toxic Environment / Bad Manager</option>
                <option value="no_growth">No Growth / Stagnation</option>
                <option value="company_instability">Company Instability / Layoffs</option>
                <option value="compensation_below_market">Compensation Below Market</option>
                <option value="role_changed_against_will">Role Changed Against Will</option>
                <option value="personal_relocation">Personal Relocation</option>
                <option value="no_push">No Push / Just Exploring</option>
              </select>
            </div>
            <div class="form-group"><label>Pull Factor (Reason to Join) *</label>
              <select name="p3_pull_factor" required>
                <option value="">— Select —</option>
                <option value="dream_company">Dream Company / Brand</option>
                <option value="career_step_up">Career Step Up</option>
                <option value="domain_passion">Domain / Tech Passion</option>
                <option value="better_ctc">Better CTC</option>
                <option value="better_wlb">Better Work-Life Balance</option>
                <option value="referred_by_network">Referred by Network</option>
                <option value="no_pull">No Strong Pull</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <div class="form-section-title">P4 — Counter-offer, Warmth & Stability</div>
          <div class="form-grid three">
            <div class="form-group"><label>Current Company Type *</label>
              <select name="p4_company_type" required>
                <option value="">— Select —</option>
                <option value="top_brand">Top Brand / FAANG / Large MNC</option>
                <option value="mid_size">Mid-size Known Company (Series B–D+)</option>
                <option value="early_startup">Early-stage Startup (Seed–Series A)</option>
                <option value="small_business">Small Business / Bootstrapped</option>
              </select>
            </div>
            <div class="form-group"><label>Seniority Level *</label>
              <select name="p4_seniority_level" required>
                <option value="">— Select —</option>
                <option value="csuite_vp_director">C-Suite / VP / Director</option>
                <option value="senior_manager_lead">Senior Manager / Lead (8–15 yrs)</option>
                <option value="manager_senior_ic">Manager / Senior IC (5–8 yrs)</option>
                <option value="mid_level_ic">Mid-level IC (3–5 yrs)</option>
                <option value="junior_entry">Junior / Entry Level (0–3 yrs)</option>
              </select>
            </div>
            <div class="form-group"><label>Tenure at Current Company (Years) *</label><input name="p4_current_tenure_years" type="number" step="0.5" required placeholder="2"></div>
            <div class="form-group"><label>Recruiter Warmth Rating (1–5) *</label>
              <select name="p4_warmth_rating" required>
                <option value="">— Select —</option>
                <option value="5">5 — Very Strong Bond</option>
                <option value="4">4 — Good Rapport</option>
                <option value="3">3 — Professional but Neutral</option>
                <option value="2">2 — Distant / Formal</option>
                <option value="1">1 — Cold / Disengaged</option>
              </select>
            </div>
            <div class="form-group"><label>Average Tenure Per Company (Years) *</label><input name="p4_avg_tenure_years" type="number" step="0.5" required placeholder="2.5"></div>
          </div>
          <div style="margin-top:14px;">
            <label style="display:block;margin-bottom:8px;font-size:11px;font-family:'DM Mono',monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;">Warmth Boosters (select all that apply)</label>
            <div class="check-group">
              <label class="check-item"><input type="checkbox" name="warmth_boosters" value="referred_someone"><span>Referred someone</span></label>
              <label class="check-item"><input type="checkbox" name="warmth_boosters" value="shared_personal_news"><span>Shared personal news</span></label>
              <label class="check-item"><input type="checkbox" name="warmth_boosters" value="asked_joining_advice"><span>Asked for advice</span></label>
              <label class="check-item"><input type="checkbox" name="warmth_boosters" value="formalities_ahead_of_schedule"><span>Formalities early</span></label>
              <label class="check-item"><input type="checkbox" name="warmth_boosters" value="prior_placement"><span>Prior placement</span></label>
            </div>
          </div>
          <div style="margin-top:14px;">
            <label style="display:block;margin-bottom:8px;font-size:11px;font-family:'DM Mono',monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;">Stability Modifiers (select all that apply)</label>
            <div class="check-group">
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="startups_shut_down"><span>Startups shut down</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="contract_roles"><span>Contract roles</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="early_career_only"><span>Early career only</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="recent_trend_stable"><span>Recent trend stable</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="multiple_offer_drops"><span>Multiple offer drops</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="left_within_3_months"><span>Left within 3 months</span></label>
              <label class="check-item"><input type="checkbox" name="stability_modifiers" value="current_role_5_plus_yrs"><span>Current role 5+ yrs</span></label>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="resetForm('form-prediction')">Clear</button>
          <button type="submit" class="btn btn-primary">
            <span class="spinner" id="spin-prediction"></span> Run Prediction & Save
          </button>
        </div>
      </div>
    </form>
  </div>

  <!-- ALL INTERVIEWS -->
  <div class="page" id="page-interviews">
    <div class="page-header">
      <div class="page-title">Interview Records</div>
      <div class="page-sub">All candidate interview evaluations</div>
    </div>
    <div class="table-wrap">
      <table><thead><tr>
        <th>Name</th><th>Exp</th><th>Tech Stack</th><th>Status</th>
        <th>Comm</th><th>Apex</th><th>Scenarios</th><th>LWC</th><th>Overall</th><th>Notes</th>
      </tr></thead>
      <tbody id="interviews-table"><tr><td colspan="10" class="empty">Loading...</td></tr></tbody></table>
    </div>
  </div>

  <!-- ALL PREDICTIONS -->
  <div class="page" id="page-predictions">
    <div class="page-header">
      <div class="page-title">Prediction Records</div>
      <div class="page-sub">All offer acceptance model scores</div>
    </div>
    <div class="table-wrap">
      <table><thead><tr>
        <th>Name</th><th>Hike %</th>
        <th>P0</th><th>P1</th><th>P2</th><th>P3</th><th>P4</th>
        <th>Final</th><th>Level</th><th>Outcome</th><th>Action</th>
      </tr></thead>
      <tbody id="predictions-table"><tr><td colspan="11" class="empty">Loading...</td></tr></tbody></table>
    </div>
  </div>

</main>
</div>

<script>
// ── Navigation ───────────────────────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  event.currentTarget.classList.add('active');
  if (id === 'dashboard')   loadDashboard();
  if (id === 'interviews')  loadInterviews();
  if (id === 'predictions') loadPredictions();
}

// ── Score bar ────────────────────────────────────────────────────────────────
function scoreBar(score) {
  const color = score >= 85 ? '#3ecf8e' : score >= 70 ? '#7c6cfc' : score >= 55 ? '#fcb96c' : '#fc6c6c';
  return `<div class="score-bar">
    <div class="bar-track"><div class="bar-fill" style="width:${score}%;background:${color}"></div></div>
    <div class="score-num" style="color:${color}">${score}</div>
  </div>`;
}

function levelBadge(level) {
  const map = { 'Very High': 'green', 'High': 'purple', 'Moderate': 'amber',
                'Low': 'red', 'Very Low': 'red' };
  return `<span class="badge badge-${map[level] || 'dim'}">${level || '—'}</span>`;
}

function statusBadge(s) {
  const map = { Approved: 'green', Rejected: 'red', 'On Hold': 'amber', pending: 'dim', joined: 'green', dropped: 'red' };
  return `<span class="badge badge-${map[s] || 'dim'}">${s || 'pending'}</span>`;
}

// ── Dashboard ────────────────────────────────────────────────────────────────
async function loadDashboard() {
  const r = await fetch('/api/dashboard');
  const d = await r.json();
  document.getElementById('stat-total').textContent = d.total_candidates;
  document.getElementById('stat-approved').textContent = d.approved;
  document.getElementById('stat-rejected').textContent = d.rejected;
  document.getElementById('stat-predictions').textContent = d.predictions;
  const tb = document.getElementById('dashboard-table');
  if (!d.recent.length) { tb.innerHTML = '<tr><td colspan="6" class="empty">No candidates yet.</td></tr>'; return; }
  tb.innerHTML = d.recent.map(r => `<tr>
    <td><strong>${r.name}</strong></td>
    <td>${r.experience_years ? r.experience_years + ' yrs' : '—'}</td>
    <td>${statusBadge(r.status)}</td>
    <td>${r.overall_score ? r.overall_score + ' / 5' : '—'}</td>
    <td>${r.final_score ? scoreBar(r.final_score) : '—'}</td>
    <td>${r.joining_level ? levelBadge(r.joining_level) : '—'}</td>
  </tr>`).join('');
}

// ── Interviews ───────────────────────────────────────────────────────────────
async function loadInterviews() {
  const r = await fetch('/api/interviews');
  const d = await r.json();
  const tb = document.getElementById('interviews-table');
  if (!d.length) { tb.innerHTML = '<tr><td colspan="10" class="empty">No interview records yet.</td></tr>'; return; }
  tb.innerHTML = d.map(r => `<tr>
    <td><strong>${r.name}</strong></td>
    <td>${r.experience_years ? r.experience_years + ' yrs' : '—'}</td>
    <td><span style="color:var(--muted);font-size:12px">${r.technology_stack || '—'}</span></td>
    <td>${statusBadge(r.status)}</td>
    <td>${r.communication_confidence || '—'}</td>
    <td>${r.apex_score || '—'}</td>
    <td>${r.scenario_problem_solving || '—'}</td>
    <td>${r.lwc_score || '—'}</td>
    <td>${r.overall_score ? '<strong>' + r.overall_score + '</strong> / 5' : '—'}</td>
    <td style="max-width:200px;color:var(--muted);font-size:12px">${r.interview_notes || r.rejection_reason || '—'}</td>
  </tr>`).join('');
}

// ── Predictions ──────────────────────────────────────────────────────────────
async function loadPredictions() {
  const r = await fetch('/api/predictions');
  const d = await r.json();
  const tb = document.getElementById('predictions-table');
  if (!d.length) { tb.innerHTML = '<tr><td colspan="11" class="empty">No predictions yet.</td></tr>'; return; }
  tb.innerHTML = d.map(r => `<tr>
    <td><strong>${r.name}</strong></td>
    <td>${r.hike_pct ? r.hike_pct + '%' : '—'}</td>
    <td>${r.p0_score || '—'}</td><td>${r.p1_score || '—'}</td>
    <td>${r.p2_score || '—'}</td><td>${r.p3_score || '—'}</td><td>${r.p4_score || '—'}</td>
    <td>${r.final_score ? scoreBar(r.final_score) : '—'}</td>
    <td>${levelBadge(r.joining_level)}</td>
    <td>${statusBadge(r.actual_outcome)}</td>
    <td>
      <select onchange="updateOutcome(${r.result_id}, this.value)"
              style="padding:4px 8px;font-size:11px;background:var(--surface);border:1px solid var(--border2);border-radius:5px;color:var(--text)">
        <option value="pending" ${r.actual_outcome==='pending'?'selected':''}>Pending</option>
        <option value="joined"  ${r.actual_outcome==='joined'?'selected':''}>Joined</option>
        <option value="dropped" ${r.actual_outcome==='dropped'?'selected':''}>Dropped</option>
      </select>
    </td>
  </tr>`).join('');
}

async function updateOutcome(id, outcome) {
  await fetch('/api/update-outcome', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({id, outcome})
  });
}

// ── Form: Interview ───────────────────────────────────────────────────────────
document.getElementById('form-interview').addEventListener('submit', async function(e) {
  e.preventDefault();
  const spin = document.getElementById('spin-interview');
  spin.style.display = 'inline-block';
  const fd = new FormData(this);
  const data = Object.fromEntries(fd.entries());
  try {
    const r = await fetch('/api/add-interview', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    const res = await r.json();
    showAlert('alert-interview', res.ok ? 'success' : 'error',
              res.ok ? 'Interview record saved successfully.' : res.error);
    if (res.ok) this.reset();
  } catch(err) {
    showAlert('alert-interview', 'error', 'Failed to save: ' + err.message);
  }
  spin.style.display = 'none';
});

// ── Form: Prediction ──────────────────────────────────────────────────────────
document.getElementById('form-prediction').addEventListener('submit', async function(e) {
  e.preventDefault();
  const spin = document.getElementById('spin-prediction');
  spin.style.display = 'inline-block';
  const fd = new FormData(this);
  const warmth_boosters    = fd.getAll('warmth_boosters');
  const stability_modifiers = fd.getAll('stability_modifiers');
  const data = Object.fromEntries(fd.entries());
  data.warmth_boosters     = warmth_boosters;
  data.stability_modifiers = stability_modifiers;
  try {
    const r = await fetch('/api/add-prediction', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    const res = await r.json();
    if (res.ok) {
      showAlert('alert-prediction', 'success', 'Prediction saved successfully.');
      showResult(res.result);
    } else {
      showAlert('alert-prediction', 'error', res.error);
    }
  } catch(err) {
    showAlert('alert-prediction', 'error', 'Failed: ' + err.message);
  }
  spin.style.display = 'none';
});

function showResult(r) {
  const color = r.final_score >= 85 ? '#3ecf8e' : r.final_score >= 70 ? '#7c6cfc' : r.final_score >= 55 ? '#fcb96c' : '#fc6c6c';
  document.getElementById('res-score').textContent = r.final_score;
  document.getElementById('res-score').style.color = color;
  document.getElementById('res-level').textContent = r.joining_level;
  document.getElementById('res-prob').textContent = 'Probability: ' + r.joining_probability;
  document.getElementById('res-action').textContent = r.recommended_action;
  const riskEl = document.getElementById('res-risk');
  if (r.risk_flag) { riskEl.textContent = r.risk_flag; riskEl.style.display = 'block'; }
  else { riskEl.style.display = 'none'; }
  const params = [
    {label:'P0 CTC',         score:r.p0_score, weight:'45%'},
    {label:'P1 Location',    score:r.p1_score, weight:'22%'},
    {label:'P2 Friction',    score:r.p2_score, weight:'17%'},
    {label:'P3 Motivation',  score:r.p3_score, weight:'10%'},
    {label:'P4 Risk',        score:r.p4_score, weight:'6%'},
  ];
  const c = s => s >= 85 ? '#3ecf8e' : s >= 70 ? '#7c6cfc' : s >= 55 ? '#fcb96c' : '#fc6c6c';
  document.getElementById('result-grid').innerHTML = params.map(p => `
    <div class="result-param">
      <div class="result-param-label">${p.label} (${p.weight})</div>
      <div class="result-param-score" style="color:${c(p.score)}">${p.score}</div>
    </div>`).join('');
  document.getElementById('result-banner').classList.add('show');
  document.getElementById('result-banner').scrollIntoView({behavior:'smooth', block:'nearest'});
}

function showAlert(id, type, msg) {
  const el = document.getElementById(id);
  el.className = 'alert show alert-' + type;
  el.textContent = msg;
  setTimeout(() => el.classList.remove('show'), 5000);
}

function resetForm(id) {
  document.getElementById(id).reset();
  document.getElementById('result-banner').classList.remove('show');
}

// Initial load
loadDashboard();
</script>
</body>
</html>"""

# ── API Routes ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/dashboard')
def api_dashboard():
    conn = get_conn()
    c    = conn.cursor()
    total      = c.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    approved   = c.execute("SELECT COUNT(*) FROM interview_scores WHERE status='Approved'").fetchone()[0]
    rejected   = c.execute("SELECT COUNT(*) FROM interview_scores WHERE status='Rejected'").fetchone()[0]
    predictions= c.execute("SELECT COUNT(*) FROM prediction_results").fetchone()[0]
    recent     = c.execute("""
        SELECT ca.name, ca.experience_years,
               i.status, i.overall_score,
               r.final_score, r.joining_level
        FROM candidates ca
        LEFT JOIN interview_scores i  ON i.candidate_id  = ca.id
        LEFT JOIN prediction_results r ON r.candidate_id = ca.id
        ORDER BY ca.created_at DESC LIMIT 20
    """).fetchall()
    conn.close()
    return jsonify({
        "total_candidates": total,
        "approved": approved,
        "rejected": rejected,
        "predictions": predictions,
        "recent": [dict(r) for r in recent],
    })

@app.route('/api/interviews')
def api_interviews():
    conn = get_conn()
    rows = conn.execute("""
        SELECT ca.name, ca.experience_years, ca.technology_stack,
               i.status, i.communication_confidence, i.apex_score,
               i.scenario_problem_solving, i.lwc_score,
               i.overall_score, i.interview_notes, i.rejection_reason
        FROM interview_scores i
        JOIN candidates ca ON ca.id = i.candidate_id
        ORDER BY i.created_at DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/predictions')
def api_predictions():
    conn = get_conn()
    rows = conn.execute("""
        SELECT ca.name, pi.hike_pct,
               r.id as result_id,
               r.p0_score, r.p1_score, r.p2_score, r.p3_score, r.p4_score,
               r.final_score, r.joining_level, r.joining_probability,
               r.recommended_action, r.actual_outcome
        FROM prediction_results r
        JOIN candidates ca        ON ca.id = r.candidate_id
        LEFT JOIN prediction_inputs pi ON pi.id = r.prediction_input_id
        ORDER BY r.final_score DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/add-interview', methods=['POST'])
def api_add_interview():
    d = request.json
    try:
        conn = get_conn()
        cid  = insert_candidate(
            conn,
            name               = d.get('name','').strip(),
            email              = d.get('email') or None,
            phone              = d.get('phone') or None,
            experience_years   = float(d['experience_years']) if d.get('experience_years') else None,
            current_company    = d.get('current_company') or None,
            current_role       = d.get('current_role') or None,
            technology_stack   = d.get('technology_stack') or None,
            source             = d.get('source') or None,
            notes              = d.get('notes') or None,
        )
        def flt(k): return float(d[k]) if d.get(k) else None
        insert_interview(
            conn,
            candidate_id             = cid,
            interview_date           = d.get('interview_date') or None,
            interviewer_name         = d.get('interviewer_name') or None,
            status                   = d.get('status'),
            communication_confidence = flt('communication_confidence'),
            apex_score               = flt('apex_score'),
            scenario_problem_solving = flt('scenario_problem_solving'),
            lwc_score                = flt('lwc_score'),
            extra_skill_1_name       = d.get('extra_skill_1_name') or None,
            extra_skill_1_score      = flt('extra_skill_1_score'),
            extra_skill_2_name       = d.get('extra_skill_2_name') or None,
            extra_skill_2_score      = flt('extra_skill_2_score'),
            rejection_reason         = d.get('rejection_reason') or None,
            interview_notes          = d.get('interview_notes') or None,
        )
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/add-prediction', methods=['POST'])
def api_add_prediction():
    d = request.json
    try:
        p_inputs = {
            "note": d.get('note'),
            "p0": {
                "current_ctc": float(d['p0_current_ctc']),
                "new_ctc":     float(d['p0_new_ctc']),
            },
            "p1": {
                "relocation_type" : d['p1_relocation_type'],
                "city_tier"       : int(d['p1_city_tier']),
                "family_profile"  : d['p1_family_profile'],
                "competing_offers": int(d['p1_competing_offers']),
                "offer_strength"  : d['p1_offer_strength'],
            },
            "p2": {
                "notice_period_days"  : float(d['p2_notice_period_days']),
                "buyout_situation"    : d['p2_buyout_situation'],
                "current_brand"       : d['p2_current_brand'],
                "new_brand"           : d['p2_new_brand'],
                "work_mode_preference": d['p2_work_mode_preference'],
                "work_mode_offered"   : d['p2_work_mode_offered'],
                "partner_profile"     : d['p2_partner_profile'],
                "relocation_type"     : d['p1_relocation_type'],
            },
            "p3": {
                "candidate_interview_rating": int(d['p3_candidate_interview_rating']),
                "recruiter_observations": {
                    "engagement"          : d['p3_obs_engagement'],
                    "process_speed"       : d['p3_obs_process_speed'],
                    "responsiveness"      : d['p3_obs_responsiveness'],
                    "interviewer_quality" : d['p3_obs_interviewer_quality'],
                },
                "offer_to_joining_days": float(d['p3_offer_to_joining_days']),
                "engagement_during_gap": d['p3_engagement_during_gap'],
                "career_move_type"     : d['p3_career_move_type'],
                "goal_alignment"       : d['p3_goal_alignment'],
                "push_factor"          : d['p3_push_factor'],
                "pull_factor"          : d['p3_pull_factor'],
            },
            "p4": {
                "company_type"        : d['p4_company_type'],
                "seniority_level"     : d['p4_seniority_level'],
                "current_tenure_years": float(d['p4_current_tenure_years']),
                "warmth_rating"       : int(d['p4_warmth_rating']),
                "warmth_boosters"     : d.get('warmth_boosters', []),
                "avg_tenure_years"    : float(d['p4_avg_tenure_years']),
                "stability_modifiers" : d.get('stability_modifiers', []),
            },
        }
        result = calculate_joining_probability(
            candidate_name = d.get('name', 'Unknown'),
            p0_inputs = p_inputs['p0'],
            p1_inputs = p_inputs['p1'],
            p2_inputs = p_inputs['p2'],
            p3_inputs = p_inputs['p3'],
            p4_inputs = p_inputs['p4'],
        )
        conn = get_conn()
        cid  = insert_candidate(conn, name=d.get('name','').strip(), notes=d.get('note'))
        pid  = insert_prediction(conn, cid, p_inputs)
        insert_result(conn, cid, pid, result)
        conn.close()
        return jsonify({"ok": True, "result": {
            "final_score"       : result['final_score'],
            "joining_level"     : result['joining_level'],
            "joining_probability": result['joining_probability'],
            "recommended_action": result['recommended_action'],
            "risk_flag"         : result.get('risk_flag'),
            "p0_score": result['p0_score'], "p1_score": result['p1_score'],
            "p2_score": result['p2_score'], "p3_score": result['p3_score'],
            "p4_score": result['p4_score'],
        }})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/update-outcome', methods=['POST'])
def api_update_outcome():
    d = request.json
    conn = get_conn()
    update_outcome(conn, d['id'], d['outcome'])
    conn.close()
    return jsonify({"ok": True})

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("DB not found, creating...")
        conn = create_database(DB_PATH)
        conn.close()
    print("\nTalentOS running at http://localhost:5000\n")
    app.run(debug=True, port=5000)