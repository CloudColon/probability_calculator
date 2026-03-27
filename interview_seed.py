"""
Seed batch 5 — Salesforce, React, React Native, Java, DevOps candidates.
Notes:
- First-name-only candidates stored as-is (Abhijit, Sohit, Dhananjay etc.)
- Multi-round: Prachi Bhumarkar, Rohit Yadav, Bhavesh Gujarkar, Chinmay,
               Rohit (multiple), Mudit, Avinash, Rajnandini, Sayali (first names)
- Second-round result notes added as interview_notes on existing records
- React/RN/Java/DevOps candidates get tech stored properly
"""
import sqlite3, sys, os
sys.path.insert(0, '/home/claude')
from create_db import insert_candidate, insert_interview

DB_PATH = './recruitment.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

candidates = [
    # ── Salesforce ────────────────────────────────────────────────────────────
    {
        "candidate": {"name": "Dilip Ahiwar", "experience_years": 2.5, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 2.5,
            "apex_score": 4.0, "scenario_problem_solving": 4.0,
            "interview_notes": "Accepted. Technically good — communication average (noted in second round result)."}]
    },
    {
        "candidate": {"name": "Dhananjay", "experience_years": 3.1, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 1.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Confidence", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Shubham Dharpure", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.25,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 3.5}]
    },
    {
        "candidate": {"name": "Mahesh Pawar", "experience_years": 2.0, "technology_stack": "Salesforce, Apex, LWC, Flow"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.75,
            "apex_score": 1.0, "lwc_score": 1.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Flow", "extra_skill_1_score": 1.0}]
    },
    {
        "candidate": {"name": "Abhijit", "experience_years": 3.5, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "apex_score": 3.5, "lwc_score": 3.5, "scenario_problem_solving": 3.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Sohit Mishra", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected"}]
    },
    {
        "candidate": {"name": "Sonali Surwase", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.75,
            "apex_score": 2.0, "scenario_problem_solving": 2.5}]
    },
    {
        "candidate": {"name": "Rahul Suryawanshi", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, Flow"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.25,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Flow", "extra_skill_1_score": 2.5}]
    },
    {
        "candidate": {"name": "Rohini", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Admin", "extra_skill_1_score": 2.5}]
    },
    {
        "candidate": {"name": "Krishna Sahu", "experience_years": 2.0, "technology_stack": "Salesforce, Apex, LWC, Flow"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.75,
            "apex_score": 3.5, "lwc_score": 3.5, "scenario_problem_solving": 3.5,
            "extra_skill_1_name": "Flow", "extra_skill_1_score": 3.0,
            "interview_notes": "Accepted. Technically good, communication good (second round result)."}]
    },
    {
        "candidate": {"name": "Pratik", "experience_years": 2.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "apex_score": 3.5, "scenario_problem_solving": 3.5,
            "interview_notes": "Accepted. Technically excellent, communication excellent (second round result)."}]
    },
    {
        "candidate": {"name": "Jyoti", "experience_years": 2.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 3.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Admin", "extra_skill_1_score": 2.5}]
    },
    {
        "candidate": {"name": "Sagar Dhawle", "experience_years": 2.6, "technology_stack": "Salesforce, Apex, LWC, Flow"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Flow", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Mehul Thavkar", "experience_years": 2.0, "technology_stack": "Salesforce, Apex, LWC, Flow"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Flow", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Rajshree Swarnkar", "experience_years": 2.5, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "apex_score": 3.5, "scenario_problem_solving": 3.5,
            "interview_notes": "Accepted. Technically good, communication very good. LWC not good (second round result)."}]
    },
    {
        "candidate": {"name": "Mukesh", "experience_years": 2.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Girish", "experience_years": 4.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "apex_score": 3.5, "lwc_score": 3.0,
            "extra_skill_1_name": "Admin", "extra_skill_1_score": 3.5,
            "interview_notes": "Accepted. Need to check more in second round on Apex. Technically good, communication good (second round result)."}]
    },
    {
        "candidate": {"name": "Mukesh Rawat", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 3.0, "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Admin", "extra_skill_1_score": 3.5}]
    },
    {
        "candidate": {"name": "Nikesh Balpande", "experience_years": 3.6, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 3.0}]
    },
    {
        "candidate": {"name": "Akshay Dongre", "experience_years": 2.5, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected"}]
    },
    {
        "candidate": {"name": "Sakshi Sai", "experience_years": 2.6, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 3.5}]
    },
    {
        "candidate": {"name": "Megha", "experience_years": 2.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Jitendra Singh", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "apex_score": 2.0, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Shubham Band", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "lwc_score": 0.5,
            "interview_notes": "LWC: No knowledge."}]
    },
    {
        "candidate": {"name": "Manisha Khorgade", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.5}]
    },
    {
        "candidate": {"name": "Rohit Pathak", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 4.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Saurabh Dixit", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected"}]
    },
    {
        "candidate": {"name": "Rajesh Raj", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected"}]
    },
    {
        "candidate": {"name": "Priya Singh", "experience_years": None, "technology_stack": "Salesforce, SOQL, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 4.0,
            "lwc_score": 2.5,
            "extra_skill_1_name": "Security Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 2.5}]
    },
    {
        "candidate": {"name": "Pravina Kshirsagar", "experience_years": 3.5, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected", "interview_notes": "Not good."}]
    },
    {
        "candidate": {"name": "Nehal Sehera", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.8,
            "apex_score": 2.5, "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0}]
    },
    {
        "candidate": {"name": "Arpit Sharma", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{"status": "Rejected", "communication_confidence": 2.5, "apex_score": 2.5}]
    },
    {
        "candidate": {"name": "Anushesh Nikhare", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.5,
            "apex_score": 2.5, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Rushikesh Deshmukh", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{"status": "Rejected", "communication_confidence": 3.0, "apex_score": 3.0}]
    },
    {
        "candidate": {"name": "Gopal", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "apex_score": 2.5, "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.5}]
    },
    {
        "candidate": {"name": "Neha Shahu", "experience_years": None, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Akshay Kumar", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Confidence", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Jayashri Patil", "experience_years": 2.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected",
            "apex_score": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 1.0}]
    },
    {
        "candidate": {"name": "Sakshi", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.5, "scenario_problem_solving": 3.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 4.0,
            "interview_notes": "Accepted for second round."}]
    },
    {
        "candidate": {"name": "Prasad", "experience_years": 3.6, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.5,
            "apex_score": 3.5, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    # Prachi Bhumarkar: two rounds, both approved
    {
        "candidate": {"name": "Prachi Bhumarkar", "experience_years": 5.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 4.0, "apex_score": 3.5, "scenario_problem_solving": 3.5,
             "extra_skill_1_name": "Basics", "extra_skill_1_score": 4.0,
             "interview_notes": "Accepted."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "communication_confidence": 4.5, "apex_score": 3.5,
             "scenario_problem_solving": 4.0, "lwc_score": 3.5,
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Sachin Pawar", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 3.0, "lwc_score": 1.0, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Deepak Kumar Sharma", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "apex_score": 4.0, "lwc_score": 4.0, "scenario_problem_solving": 4.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 4.0,
            "interview_notes": "Accepted for second round."}]
    },
    {
        "candidate": {"name": "Sudarshan", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 3.0, "lwc_score": 2.0, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Megha Chouhan", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 1.0}]
    },
    {
        "candidate": {"name": "Shubham Mishra", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 1.0}]
    },
    {
        "candidate": {"name": "Vipul Chaudhari", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 2.0}]
    },
    # Deepak: standalone approved (different from Deepak Kumar Sharma)
    {
        "candidate": {"name": "Deepak", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 4.0, "lwc_score": 3.0, "scenario_problem_solving": 3.0,
            "interview_notes": "Approved."}]
    },
    {
        "candidate": {"name": "Sakshi Gupta", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 4.0,
            "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0}]
    },
    {
        "candidate": {"name": "Simmi", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "scenario_problem_solving": 0.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 1.5}]
    },
    {
        "candidate": {"name": "Snehal", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Sanyam Jain", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Abhijeet", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 1.0, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Abhinay", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.5, "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Security", "extra_skill_1_score": 1.5}]
    },
    {
        "candidate": {"name": "Manisha Dautpure", "experience_years": 3.6, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 2.0}]
    },
    {
        "candidate": {"name": "Satyabrata", "experience_years": 3.9, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 4.0,
            "apex_score": 2.5, "scenario_problem_solving": 3.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0}]
    },
    {
        "candidate": {"name": "Vikram Dhongade", "experience_years": 2.6, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 3.0}]
    },
    # Rohit Yadav: on-hold R1, approved R2
    {
        "candidate": {"name": "Rohit Yadav", "experience_years": 0.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "On Hold",
             "communication_confidence": 3.5, "scenario_problem_solving": 2.0,
             "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
             "extra_skill_2_name": "SOQL Practical", "extra_skill_2_score": 3.0,
             "interview_notes": "Fresher. Accepted for next round (on hold)."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "communication_confidence": 3.5, "apex_score": 3.0,
             "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Ayush Shrivastava", "experience_years": 0.0, "technology_stack": "Salesforce, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 1.0,
            "interview_notes": "Fresher. Not able to write simple SOQL query."}]
    },
    {
        "candidate": {"name": "Anshuman Agarwal", "experience_years": 0.0, "technology_stack": "Salesforce, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.0,
            "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 1.0,
            "interview_notes": "Fresher."}]
    },
    {
        "candidate": {"name": "Ajinkya Shende", "experience_years": 0.0, "technology_stack": "Salesforce, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.5,
            "extra_skill_2_name": "SOQL", "extra_skill_2_score": 2.0,
            "interview_notes": "Fresher. Interview taken on Friday."}]
    },
    # Bhavesh Gujarkar: approved R1, rejected R2
    {
        "candidate": {"name": "Bhavesh Gujarkar", "experience_years": 0.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 3.0, "scenario_problem_solving": 3.0,
             "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
             "extra_skill_2_name": "SOQL & Apex", "extra_skill_2_score": 2.5,
             "interview_notes": "Fresher. Approved for second round."},
            {"interviewer_name": "Round 2", "status": "Rejected"}
        ]
    },
    {
        "candidate": {"name": "Omkar Shadangule", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Approved", "interview_notes": "Approved."}]
    },
    # Chinmay: approved-second R1, approved R2
    {
        "candidate": {"name": "Chinmay", "experience_years": 3.2, "technology_stack": "Salesforce, Apex, LWC"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 3.5, "apex_score": 4.0, "scenario_problem_solving": 3.5,
             "interview_notes": "Approved for second round."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "communication_confidence": 4.0, "apex_score": 3.5, "lwc_score": 3.5,
             "scenario_problem_solving": 4.0,
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Anup", "experience_years": 13.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.5,
            "apex_score": 2.0, "scenario_problem_solving": 3.5}]
    },
    {
        "candidate": {"name": "Sandesh", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Abhishek", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 1.0,
            "apex_score": 0.0, "scenario_problem_solving": 0.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 0.0}]
    },
    {
        "candidate": {"name": "Sahil Goyal", "experience_years": 3.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 1.0,
            "apex_score": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 1.0}]
    },
    {
        "candidate": {"name": "Akhil", "experience_years": 5.2, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "apex_score": 4.0, "scenario_problem_solving": 4.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Trupti Dahikar", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC, SOQL"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.0, "lwc_score": 2.5, "scenario_problem_solving": 3.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Rajnandini", "experience_years": 2.0, "technology_stack": "Salesforce, Apex, SOQL"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 4.5, "apex_score": 4.5, "scenario_problem_solving": 4.5,
             "interview_notes": "Approved for second round."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Avinash", "experience_years": 4.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 4.5, "apex_score": 4.5, "scenario_problem_solving": 4.5,
             "interview_notes": "Approved."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "communication_confidence": 4.0, "apex_score": 3.5, "scenario_problem_solving": 4.0,
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Rohit", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC, SOQL, Triggers"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 3.5, "apex_score": 3.0, "lwc_score": 3.0,
             "scenario_problem_solving": 3.0,
             "interview_notes": "Approved."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "communication_confidence": None, "apex_score": 3.5,
             "scenario_problem_solving": 4.0,
             "interview_notes": "Approved. LWD in 40 days."}
        ]
    },
    {
        "candidate": {"name": "Mudit", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC, Triggers"},
        "interviews": [
            {"interviewer_name": "Round 1", "status": "Approved",
             "communication_confidence": 2.0, "apex_score": 3.0, "lwc_score": 3.0,
             "scenario_problem_solving": 2.0,
             "interview_notes": "Approved."},
            {"interviewer_name": "Round 2", "status": "Approved",
             "apex_score": 3.5, "scenario_problem_solving": 3.5,
             "extra_skill_1_name": "Basics", "extra_skill_1_score": 4.0,
             "interview_notes": "Approved."}
        ]
    },
    {
        "candidate": {"name": "Sayali", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, LWC, Triggers"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 2.0,
            "apex_score": 2.0, "lwc_score": 1.0, "scenario_problem_solving": 2.0,
            "interview_notes": "Approved."}]
    },
    {
        "candidate": {"name": "Prachi", "experience_years": 2.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "apex_score": 2.0, "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Bhavesh Joshi", "experience_years": 3.0, "technology_stack": "Salesforce, Apex, SOQL, Triggers"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "scenario_problem_solving": 2.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Omeshwar", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "apex_score": 3.5, "scenario_problem_solving": 3.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Pravin", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.5, "scenario_problem_solving": 3.5,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Manoj", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "scenario_problem_solving": 2.0}]
    },
    {
        "candidate": {"name": "Pravin Bhadane", "experience_years": 2.5, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "apex_score": 2.0, "scenario_problem_solving": 1.0,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 2.0}]
    },
    {
        "candidate": {"name": "Payal", "experience_years": 0.0, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.0, "scenario_problem_solving": 2.5,
            "extra_skill_1_name": "Basics", "extra_skill_1_score": 3.0,
            "interview_notes": "Fresher. Approved for second round."}]
    },
    {
        "candidate": {"name": "Prince Saini", "experience_years": 0.0, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Approved", "interview_notes": "Fresher. Approved."}]
    },
    {
        "candidate": {"name": "Harsh", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.5, "scenario_problem_solving": 3.0,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Himanshu Jain", "experience_years": 0.0, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Approved", "interview_notes": "Fresher. Approved."}]
    },
    {
        "candidate": {"name": "Ashutosh Kalambe", "experience_years": None, "technology_stack": "Salesforce"},
        "interviews": [{"status": "Rejected"}]
    },
    {
        "candidate": {"name": "Rashid Khan", "experience_years": None, "technology_stack": "Salesforce, Apex"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "apex_score": 3.5, "scenario_problem_solving": 3.5,
            "interview_notes": "Approved for second round."}]
    },
    {
        "candidate": {"name": "Rohit Patel", "experience_years": None, "technology_stack": "Salesforce, Apex, LWC, SOQL"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 2.5,
            "apex_score": 2.0, "lwc_score": 2.0, "scenario_problem_solving": 2.0}]
    },

    # ── React Native ─────────────────────────────────────────────────────────
    {
        "candidate": {"name": "Rohit Arora", "experience_years": None, "technology_stack": "React Native"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 4.0,
            "interview_notes": "Technical good, communication average. Selected for next round."}]
    },
    {
        "candidate": {"name": "Ravi Shrivastava", "experience_years": None, "technology_stack": "React Native"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 3.0,
            "interview_notes": "Selected for next round."}]
    },
    {
        "candidate": {"name": "Yogendra Singh Girase", "experience_years": 10.0, "technology_stack": "React Native, React, JavaScript, TypeScript"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "extra_skill_1_name": "React Native & Project Exp", "extra_skill_1_score": 3.75,
            "extra_skill_2_name": "ReactJS & TypeScript", "extra_skill_2_score": 1.5,
            "interview_notes": "JS: 2, React Native: 3.5, ReactJS: 2, TypeScript: 1, Unit Testing: 3, Logical Thinking: 1, Previous Project Exp: 4."}]
    },
    {
        "candidate": {"name": "Vaishali Pal", "experience_years": None, "technology_stack": "React Native"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 3.5,
            "extra_skill_2_name": "Programming", "extra_skill_2_score": 3.0,
            "interview_notes": "Selected for next round."}]
    },

    # ── React ─────────────────────────────────────────────────────────────────
    {
        "candidate": {"name": "Palash Goyal", "experience_years": None, "technology_stack": "React, JavaScript"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 2.5,
            "extra_skill_2_name": "Programming & Unit Testing", "extra_skill_2_score": 1.5,
            "interview_notes": "JS: 2.5, Unit Testing: 1.5, Programming: 1.5."}]
    },
    {
        "candidate": {"name": "Himanshu Choudhary", "experience_years": None, "technology_stack": "React"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 4.0,
            "interview_notes": "Selected for next round."}]
    },
    {
        "candidate": {"name": "Nirmal Rathore", "experience_years": None, "technology_stack": "React"},
        "interviews": [{
            "status": "Rejected", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 3.0,
            "extra_skill_2_name": "Programming", "extra_skill_2_score": 1.5}]
    },
    {
        "candidate": {"name": "Anvita Dixit", "experience_years": None, "technology_stack": "React"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 3.5,
            "extra_skill_2_name": "Programming", "extra_skill_2_score": 3.0,
            "interview_notes": "Selected for next round."}]
    },
    {
        "candidate": {"name": "Namandeep Singh", "experience_years": None, "technology_stack": "React"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 2.5,
            "extra_skill_2_name": "Programming", "extra_skill_2_score": 3.0,
            "interview_notes": "Selected for next round."}]
    },

    # ── Java ─────────────────────────────────────────────────────────────────
    {
        "candidate": {"name": "Lokesh Roman", "experience_years": None, "technology_stack": "Java"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 3.0,
            "interview_notes": "Selected for next round (with me). Laptop not working — plan technical coding round. Candidate should be prepared with laptop. BOD as programming round not done."}]
    },
    {
        "candidate": {"name": "Sanjay Gupta", "experience_years": None, "technology_stack": "Java"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 3.5,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 4.0,
            "interview_notes": "Selected for next round."}]
    },

    # ── DevOps ────────────────────────────────────────────────────────────────
    {
        "candidate": {"name": "Samarth Kosal", "experience_years": None, "technology_stack": "DevOps"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 4.0,
            "interview_notes": "Technical good, communication good. Selected for next round."}]
    },
    {
        "candidate": {"name": "Ankit Singh Solanki", "experience_years": None, "technology_stack": "DevOps"},
        "interviews": [{
            "status": "Approved", "communication_confidence": 4.0,
            "extra_skill_1_name": "Technical", "extra_skill_1_score": 4.0,
            "interview_notes": "Selected for next round."}]
    },
]


def seed():
    conn = get_conn()
    inserted = skipped = rounds_added = 0

    # Existing name-only candidates that might collide — check carefully
    # "Harsh" already exists as DevOps in batch3 — this is a different Harsh (Salesforce)
    # We'll suffix first-name-only conflicts with a note
    first_name_only_sf = {"Harsh", "Hrishikesh", "Abhishek"}

    for cd in candidates:
        name = cd["candidate"]["name"]
        tech = cd["candidate"].get("technology_stack", "")
        exists_rows = conn.execute("SELECT id, name FROM candidates WHERE name=?", (name,)).fetchall()

        # For first-name-only SF candidates that might conflict with existing DevOps entries
        if exists_rows and name in first_name_only_sf:
            existing_tech = conn.execute(
                "SELECT technology_stack FROM candidates WHERE id=?", (exists_rows[0]["id"],)
            ).fetchone()["technology_stack"] or ""
            # If existing is DevOps/AWS and new is Salesforce, they're different people — insert new
            if ("AWS" in existing_tech or "DevOps" in existing_tech) and "Salesforce" in tech:
                # Insert with a disambiguating note
                cd["candidate"]["name"] = name  # keep same name, different record
                exists_rows = []  # force insert

        if exists_rows:
            cid = exists_rows[0]["id"]
            existing_count = conn.execute(
                "SELECT COUNT(*) as c FROM interview_scores WHERE candidate_id=?", (cid,)
            ).fetchone()["c"]
            new_rounds = len(cd["interviews"])
            if existing_count < new_rounds:
                for iv in cd["interviews"][existing_count:]:
                    insert_interview(conn, cid, **iv)
                    rounds_added += 1
                print("Added round(s)  : {}".format(name))
            else:
                print("Skipped        : {}".format(name))
            skipped += 1
            continue

        cid = insert_candidate(conn,
            name             = name,
            experience_years = cd["candidate"].get("experience_years"),
            technology_stack = cd["candidate"].get("technology_stack"),
        )
        for iv in cd["interviews"]:
            insert_interview(conn, cid, **iv)

        r = len(cd["interviews"])
        print("Inserted       : {}  ({} record{})".format(name, r, "s" if r > 1 else ""))
        inserted += 1

    conn.close()
    print("\nDone — {} new, {} skipped, {} rounds added.".format(inserted, skipped, rounds_added))


def summary():
    conn = get_conn()
    total_cands = conn.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    total_iv    = conn.execute("SELECT COUNT(*) FROM interview_scores").fetchone()[0]
    rows = conn.execute(
        "SELECT status, COUNT(*) as c FROM interview_scores GROUP BY status ORDER BY c DESC"
    ).fetchall()
    cheating = conn.execute(
        "SELECT COUNT(*) as c FROM interview_scores WHERE rejection_reason LIKE '%Cheat%' OR rejection_reason LIKE '%cheat%' OR rejection_reason LIKE '%AI%'"
    ).fetchone()["c"]

    sf   = conn.execute("SELECT COUNT(DISTINCT ca.id) FROM candidates ca WHERE ca.technology_stack LIKE '%Salesforce%'").fetchone()[0]
    java = conn.execute("SELECT COUNT(DISTINCT ca.id) FROM candidates ca WHERE (ca.technology_stack LIKE '%Java%' OR ca.technology_stack = 'Java') AND ca.technology_stack NOT LIKE '%Salesforce%'").fetchone()[0]
    dev  = conn.execute("SELECT COUNT(DISTINCT ca.id) FROM candidates ca WHERE (ca.technology_stack LIKE '%AWS%' OR ca.technology_stack LIKE '%DevOps%' OR ca.technology_stack LIKE '%Terraform%') AND ca.technology_stack NOT LIKE '%Salesforce%'").fetchone()[0]
    react= conn.execute("SELECT COUNT(DISTINCT ca.id) FROM candidates ca WHERE (ca.technology_stack LIKE '%React%') AND ca.technology_stack NOT LIKE '%Salesforce%'").fetchone()[0]

    print("\n" + "=" * 52)
    print("  FULL DB SUMMARY")
    print("=" * 52)
    print("  Total candidates       : {}".format(total_cands))
    print("  Total interview records: {}".format(total_iv))
    print("  ── by status ──")
    for r in rows:
        print("    {:<24}: {}".format(r["status"], r["c"]))
    print("  Caught Cheating / AI   : {}".format(cheating))
    print("  ── by tech domain ──")
    print("    Salesforce             : {}".format(sf))
    print("    Java / Spring Boot     : {}".format(java))
    print("    DevOps / Cloud         : {}".format(dev))
    print("    React / React Native   : {}".format(react))
    print("=" * 52)
    conn.close()


if __name__ == "__main__":
    seed()
    summary()