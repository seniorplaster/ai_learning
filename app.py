"""
DEMO — AI Contact Center Quality Management Platform
Version 2.4.1  |  Build 2026.06
"""

import streamlit as st
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DEMO | AI Quality Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE — init before anything renders ─────────────────────────────────
defaults = {
    "active_module":    "qm",
    "selected_indices": [],
    "coach_queue":      [],
    "coach_triggered":  False,
    "coaching_results": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── ALWAYS-VISIBLE MENU BUTTON (JS toggles native Streamlit sidebar) ─────────────
# Injected once, before everything else — persists across all reruns
st.markdown("""
<button id="menu-toggle-btn" onclick="(function(){
    var c = window.parent.document.querySelector('[data-testid=collapsedControl]');
    if (c) { c.click(); return; }
    var selectors = [
        'button[aria-label=\\"Close sidebar\\"]',
        'button[title=\\"Close sidebar\\"]',
        '[data-testid=stSidebarCollapseButton]',
        '[data-testid=stSidebarCloseButton]'
    ];
    for (var s of selectors) {
        var b = window.parent.document.querySelector(s);
        if (b) { b.click(); return; }
    }
    var all = window.parent.document.querySelectorAll(
        'section[data-testid=stSidebar] button, [data-testid=stSidebar] button'
    );
    if (all.length > 0) all[0].click();
})()"
style="
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 9999999;
    background: #1e40af;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 16px 8px 12px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 700;
    font-family: Inter, sans-serif;
    letter-spacing: 0.04em;
    box-shadow: 0 2px 8px rgba(30,64,175,0.35);
    display: flex;
    align-items: center;
    gap: 6px;
    line-height: 1;
    transition: background 0.15s;
" onmouseover="this.style.background='#1e3a8a'"
  onmouseout="this.style.background='#1e40af'">
    ☰ &nbsp;Menu
</button>
<style>
/* Push page content right so Menu button never overlaps the first word */
.block-container { padding-top: 1.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
header    {visibility: hidden;}
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── APP BACKGROUND ── */
.stApp { background: #f0f4f8; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 2px solid #21262d !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* Streamlit native sidebar collapse arrow — styled to be visible */
[data-testid="collapsedControl"] {
    background: #0d1117 !important;
    border-right: 2px solid #30363d !important;
}
[data-testid="collapsedControl"] svg { fill: #58a6ff !important; }

/* ── SIDEBAR EXPANDERS ── */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"]:hover {
    border-color: #58a6ff !important;
    background: rgba(88,166,255,0.06) !important;
}
[data-testid="stSidebar"] details summary {
    color: #8b949e !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
}
[data-testid="stSidebar"] details[open] summary {
    color: #58a6ff !important;
}
[data-testid="stSidebar"] details summary svg {
    fill: #8b949e !important;
}
[data-testid="stSidebar"] details[open] summary svg {
    fill: #58a6ff !important;
}

/* ── SIDEBAR BUTTONS ── */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(88,166,255,0.1) !important;
    color: #58a6ff !important;
    border: 1px solid rgba(88,166,255,0.3) !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    padding: 5px 10px !important;
    box-shadow: none !important;
    transform: none !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(88,166,255,0.18) !important;
    border-color: #58a6ff !important;
    color: #ffffff !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── MAIN BUTTONS ── */
.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    background: #1e40af !important;
    color: #ffffff !important;
    border: 1px solid #1e40af !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.4rem !important;
    width: 100% !important;
    box-shadow: 0 2px 4px rgba(30,64,175,0.25) !important;
    transition: all 0.18s ease !important;
}
.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: #1e3a8a !important;
    border-color: #1e3a8a !important;
    box-shadow: 0 4px 12px rgba(30,64,175,0.35) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}
.main .stButton > button:active,
[data-testid="stMainBlockContainer"] .stButton > button:active {
    transform: translateY(0) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #065f46 !important;
    color: #ffffff !important;
    border: 1px solid #065f46 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    width: 100% !important;
    box-shadow: 0 2px 4px rgba(6,95,70,0.25) !important;
    transition: all 0.18s ease !important;
}
.stDownloadButton > button:hover {
    background: #047857 !important;
    box-shadow: 0 4px 12px rgba(6,95,70,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 3px !important;
    border: 1px solid #cbd5e1 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border-radius: 7px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1e40af !important;
    border: 1px solid #bfdbfe !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-size: 11px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
}
[data-testid="stMetricValue"] {
    color: #1e40af !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricDelta"] > div {
    color: #374151 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 10px !important; overflow: hidden !important; }
[data-testid="stDataFrameResizable"] {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
}

/* ── EXPANDER (main area) ── */
[data-testid="stExpander"] {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    margin-bottom: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* ── ALERTS ── */
[data-baseweb="notification"] {
    background-color: #eff6ff !important;
    border: 1.5px solid #93c5fd !important;
    border-radius: 10px !important;
    color: #1e3a8a !important;
}
[data-baseweb="notification"] p { color: #1e3a8a !important; }

/* ── SUCCESS BOX ── */
div[data-testid="stSuccess"] {
    background: #f0fdf4 !important;
    border: 1.5px solid #4ade80 !important;
    border-radius: 10px !important;
}
div[data-testid="stSuccess"] p { color: #14532d !important; font-weight: 500 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0f4f8; }
::-webkit-scrollbar-thumb { background: #94a3b8; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #64748b; }

/* ── DIVIDER ── */
hr { border-color: #e2e8f0 !important; margin: 1rem 0 !important; }

/* ── COMPONENT CLASSES ── */
.qm-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.qm-card-green {
    background: #f0fdf4;
    border: 1.5px solid #4ade80;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.qm-card-amber {
    background: #fffbeb;
    border: 1.5px solid #fcd34d;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.qm-card-red {
    background: #fef2f2;
    border: 1.5px solid #f87171;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.qm-card-blue {
    background: #eff6ff;
    border: 1.5px solid #93c5fd;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* WCAG AA badges — all verified >= 4.5:1 */
.b-green { display:inline-block; background:#d1fae5; color:#065f46; border:1.5px solid #6ee7b7; border-radius:99px; padding:3px 12px; font-size:12px; font-weight:700; }
.b-blue  { display:inline-block; background:#dbeafe; color:#1e3a8a; border:1.5px solid #93c5fd; border-radius:99px; padding:3px 12px; font-size:12px; font-weight:700; }
.b-amber { display:inline-block; background:#fef3c7; color:#92400e; border:1.5px solid #fcd34d; border-radius:99px; padding:3px 12px; font-size:12px; font-weight:700; }
.b-red   { display:inline-block; background:#fee2e2; color:#991b1b; border:1.5px solid #f87171; border-radius:99px; padding:3px 12px; font-size:12px; font-weight:700; }
.b-gray  { display:inline-block; background:#f1f5f9; color:#1e293b; border:1.5px solid #94a3b8; border-radius:99px; padding:3px 12px; font-size:12px; font-weight:700; }
.b-lock  { display:inline-block; background:#f3f4f6; color:#374151; border:1.5px solid #9ca3af; border-radius:99px; padding:2px 9px; font-size:10px; font-weight:700; }

/* Status dots */
.dot-g { display:inline-block; width:8px; height:8px; background:#16a34a; border-radius:50%; box-shadow:0 0 6px rgba(22,163,74,0.6); animation:pg 2s infinite; }
.dot-b { display:inline-block; width:8px; height:8px; background:#2563eb; border-radius:50%; box-shadow:0 0 6px rgba(37,99,235,0.6); animation:pb 2s infinite; }
.dot-a { display:inline-block; width:8px; height:8px; background:#d97706; border-radius:50%; }
@keyframes pg { 0%,100%{opacity:1;} 50%{opacity:0.35;} }
@keyframes pb { 0%,100%{opacity:1;} 50%{opacity:0.35;} }

/* Text helpers */
.page-title {
    font-size: 24px; font-weight: 700;
    background: linear-gradient(135deg, #1e40af, #0284c7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.mono   { font-family:'JetBrains Mono',monospace; font-size:12px; color:#64748b; }
.slabel { font-size:10px; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:0.14em; margin-bottom:6px; }
.dlabel { font-size:11px; color:#6b7280; text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:3px; }
.dvalue { font-size:14px; color:#111827; font-weight:600; margin-bottom:12px; }
.dmono  { font-family:'JetBrains Mono',monospace; font-size:12px; color:#374151; margin-bottom:12px; font-weight:500; }

/* Scan bar */
.scanbar {
    height: 2px;
    background: linear-gradient(90deg, transparent, #2563eb 40%, #0ea5e9 60%, transparent);
    animation: sc 4s ease-in-out infinite;
    border-radius: 1px; margin: 6px 0 20px;
}
@keyframes sc { 0%{opacity:0.1;} 50%{opacity:0.5;} 100%{opacity:0.1;} }

/* Progress tracks */
.ptrack { background:#e2e8f0; border-radius:99px; height:5px; overflow:hidden; }
.pfill-blue  { height:100%; background:linear-gradient(90deg,#1e40af,#0ea5e9); border-radius:99px; }
.pfill-green { height:100%; background:linear-gradient(90deg,#059669,#10b981); border-radius:99px; }
.pfill-amber { height:100%; background:linear-gradient(90deg,#d97706,#f59e0b); border-radius:99px; }

/* Coming soon hero */
.cs-hero {
    text-align: center; padding: 70px 40px;
    background: #ffffff; border: 1.5px solid #e2e8f0;
    border-radius: 20px; margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)


# ── PLATFORM CONSTANTS ────────────────────────────────────────────────────────────
PLATFORM   = "DEMO"
TAGLINE    = "AI Contact Center Quality Platform"
VERSION    = "v2.4.1"
BUILD_DATE = "2026.06"

MODULES = [
    {"key": "qm",        "name": "QM Analyzer",           "icon": "◈", "available": True,  "progress": 100},
    {"key": "wfm",       "name": "WFM Scheduler",         "icon": "◉", "available": False, "progress": 78,
     "milestones": [("Demand Forecasting Engine", True), ("Schedule Optimiser", True), ("Shift Bidding Portal", False), ("Real-Time Adherence Feed", False)]},
    {"key": "ia",        "name": "Interaction Analytics", "icon": "◈", "available": False, "progress": 64,
     "milestones": [("Call Transcription Pipeline", True), ("Sentiment Trend Dashboard", True), ("Topic Clustering", False), ("Compliance Phrase Detection", False)]},
    {"key": "scoreboard","name": "Agent Scoreboard",      "icon": "◉", "available": False, "progress": 89,
     "milestones": [("KPI Calculation Engine", True), ("Team Leaderboard UI", True), ("Gamification Badges", True), ("Manager Approval Workflow", False)]},
    {"key": "hiring",    "name": "Agent Hiring Insights", "icon": "◈", "available": False, "progress": 41,
     "milestones": [("Candidate Scoring Model", True), ("Interview Question Generator", False), ("Predicted Attrition Index", False), ("Skills Gap Heatmap", False)]},
    {"key": "assist",    "name": "Agent Assist",          "icon": "◉", "available": False, "progress": 55,
     "milestones": [("Real-Time Transcription", True), ("Knowledge Base Search", True), ("Next-Best-Action Engine", False), ("Auto-Draft Response", False)]},
    {"key": "sentiment", "name": "Live Sentiment Assist", "icon": "◈", "available": False, "progress": 33,
     "milestones": [("Acoustic Model Training", True), ("Emotion Classification", False), ("Agent Alert System", False), ("Supervisor Escalation Feed", False)]},
]


# ── SAMPLE DATA ───────────────────────────────────────────────────────────────────
SAMPLE_CALLS = [
    {"call_id":"AR-2026-0091","agent_id":"AGT-101","agent_name":"Sara Al Mansoori",
     "sector":"Banking","queue":"Premier Banking — Disputes",
     "duration_seconds":187,"csat_score":5,"resolved":True,"sentiment":"Positive","risk_flag":"None",
     "transcript_summary":"Customer called about an unauthorized transaction on their premium Visa card. Agent Sara verified identity using multi-factor authentication within 60 seconds, immediately initiated a chargeback, explained the 5-7 business-day timeline clearly, and proactively offered a temporary credit limit increase as goodwill. Customer expressed high satisfaction and thanked the agent by name."},
    {"call_id":"AR-2026-0092","agent_id":"AGT-205","agent_name":"Mohammed Al Rashidi",
     "sector":"Telecom","queue":"Technical Support — Mobile",
     "duration_seconds":643,"csat_score":2,"resolved":False,"sentiment":"Negative","risk_flag":"Churn Risk",
     "transcript_summary":"Customer reported mobile data not working for 3 consecutive days. Agent took 8 minutes to locate the account despite the customer providing the account number upfront. Asked customer to repeat details twice. Did not check the network outage map before troubleshooting. Failed to offer escalation, compensation, or a callback. Customer stated they would switch to a competitor."},
    {"call_id":"AR-2026-0093","agent_id":"AGT-310","agent_name":"Fatima Al Zahra",
     "sector":"Government","queue":"Licensing Services",
     "duration_seconds":245,"csat_score":4,"resolved":True,"sentiment":"Neutral","risk_flag":"None",
     "transcript_summary":"Citizen called to inquire about trade license renewal requirements and applicable fees. Agent Fatima provided clear step-by-step guidance, confirmed eligibility criteria, and sent a digital checklist via SMS during the call. A brief delay occurred when accessing the updated fee schedule, but the correct information was confirmed and the citizen confirmed readiness to proceed."},
    {"call_id":"AR-2026-0094","agent_id":"AGT-101","agent_name":"Sara Al Mansoori",
     "sector":"Healthcare","queue":"Patient Services — Cardiology",
     "duration_seconds":312,"csat_score":5,"resolved":True,"sentiment":"Positive","risk_flag":"None",
     "transcript_summary":"Patient called to schedule a cardiology follow-up and inquire about insurance pre-authorization for an MRI scan. Sara efficiently coordinated between two departments, secured a same-week appointment slot, and initiated the pre-authorization form with the insurance team. Patient expressed strong gratitude for the seamless experience."},
    {"call_id":"AR-2026-0095","agent_id":"AGT-422","agent_name":"Khalid Al Nuaimi",
     "sector":"Insurance","queue":"Claims Processing — Motor",
     "duration_seconds":521,"csat_score":1,"resolved":False,"sentiment":"Negative","risk_flag":"Compliance Risk",
     "transcript_summary":"Customer called about a denied motor insurance claim filed 3 weeks ago. Agent Khalid could not locate the claim in the CRM for 11 minutes. Transferred the customer twice without warning or context handover. When found, provided incorrect information about the appeals process and the regulatory timeline. Customer stated they would file a formal complaint with the UAE Insurance Authority."},
    {"call_id":"AR-2026-0096","agent_id":"AGT-205","agent_name":"Mohammed Al Rashidi",
     "sector":"Banking","queue":"Retail Banking — Loans",
     "duration_seconds":198,"csat_score":3,"resolved":True,"sentiment":"Neutral","risk_flag":"None",
     "transcript_summary":"Customer inquired about personal loan eligibility and current interest rates. Agent Mohammed provided the standard rate bands but could not run a live pre-qualification check because the credit-check tool was temporarily unavailable. Offered a callback from the loans team within 24 hours. Customer accepted but expressed mild frustration about not receiving an immediate eligibility answer."},
    {"call_id":"AR-2026-0097","agent_id":"AGT-310","agent_name":"Fatima Al Zahra",
     "sector":"Telecom","queue":"Enterprise Sales — Upgrades",
     "duration_seconds":289,"csat_score":4,"resolved":True,"sentiment":"Positive","risk_flag":"None",
     "transcript_summary":"Enterprise customer called to upgrade their corporate data plan from 100 GB to 500 GB and add 3 SIM cards for new employees. Fatima processed the upgrade, applied the corporate bundle discount automatically, confirmed the activation timeline, and emailed the updated contract. Customer appreciated the professional and efficient handling."},
    {"call_id":"AR-2026-0098","agent_id":"AGT-422","agent_name":"Khalid Al Nuaimi",
     "sector":"Government","queue":"Complaints & Escalation",
     "duration_seconds":614,"csat_score":2,"resolved":False,"sentiment":"Negative","risk_flag":"Compliance Risk",
     "transcript_summary":"Resident called to escalate a permit approval that was 18 days beyond the legally mandated 30-day processing window. Agent Khalid was unaware of the statutory SLA requirement. Did not log the complaint in the government CRM during the call. Provided vague reassurances with no escalation path, no reference number, and no supervisor involvement."},
    {"call_id":"AR-2026-0099","agent_id":"AGT-101","agent_name":"Sara Al Mansoori",
     "sector":"Healthcare","queue":"Insurance & Billing — Disputes",
     "duration_seconds":156,"csat_score":5,"resolved":True,"sentiment":"Positive","risk_flag":"None",
     "transcript_summary":"Patient called to dispute an erroneous consultation fee on their last hospital invoice. Sara identified the billing discrepancy immediately by cross-referencing clinical notes and the billing system. Initiated a credit note on the spot, confirmed refund within 3-5 working days, and apologised on behalf of the hospital. Patient was fully satisfied."},
]


# ── COACHING CONFIG ───────────────────────────────────────────────────────────────
COACHING_SYSTEM_PROMPT = """You are a senior contact center quality expert with 25 years of experience across banking, telecom, healthcare, government, and insurance in the GCC region.

Your coaching reports are structured, specific, and actionable. Every recommendation must reference actual events in the call summary. Never give generic advice.

Format every coaching report with these exact sections:

**PERFORMANCE SUMMARY**
A 2-3 sentence overall assessment of this specific interaction.

**STRENGTHS IDENTIFIED**
2-3 bullet points of what the agent did well, referencing specific actions. If no genuine strengths exist, state that honestly.

**CRITICAL IMPROVEMENT AREAS**
3-4 numbered coaching points. Each must reference a specific moment in the call and explain the customer impact.

**RECOMMENDED ACTIONS**
Concrete next steps: specific training modules, role-play scenarios, or process reminders.

**COACHING PRIORITY**
End with exactly one of:
🟢 PRIORITY: LOW
🟡 PRIORITY: MEDIUM
🔴 PRIORITY: HIGH
🚨 PRIORITY: URGENT — Compliance Review Required

Be direct and honest. Do not soften critical feedback."""


def build_coaching_prompt(call: dict) -> str:
    m, s = call["duration_seconds"] // 60, call["duration_seconds"] % 60
    outcome = "RESOLVED" if call["resolved"] else "UNRESOLVED"
    return f"""Generate a full coaching report for this contact center interaction.

CALL ID:   {call['call_id']}
AGENT:     {call['agent_name']} ({call['agent_id']})
SECTOR:    {call['sector']}
QUEUE:     {call['queue']}
DURATION:  {m}m {s}s  |  CSAT: {call['csat_score']}/5  |  OUTCOME: {outcome}
SENTIMENT: {call['sentiment']}  |  RISK FLAG: {call['risk_flag']}

TRANSCRIPT SUMMARY:
{call['transcript_summary']}

Provide the full coaching report. Be specific to this exact call — do not give generic advice."""


# ── PDF GENERATOR ─────────────────────────────────────────────────────────────────
def sanitize_pdf(text: str) -> str:
    em = {"🟢":"[LOW]","🟡":"[MEDIUM]","🔴":"[HIGH]","🚨":"[URGENT]",
          "★":"*","☆":"-","◉":">","◈":">","⬡":"-","→":"->","←":"<-",
          "✓":"OK","✗":"X","\u2014":"-","\u2013":"-","\u2019":"'",
          "\u2018":"'","\u201c":'"',"\u201d":'"'}
    for a, b in em.items():
        text = text.replace(a, b)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return "".join(c if c.encode("latin-1", errors="ignore") else "?" for c in text)


def generate_pdf(items: list) -> bytes:
    class Report(FPDF):
        def header(self):
            self.set_fill_color(30, 64, 175)
            self.rect(0, 0, 210, 11, "F")
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(255, 255, 255)
            self.set_xy(10, 2)
            self.cell(0, 7, "DEMO  |  AI Quality Coaching Report  |  Confidential", ln=False)
            self.set_text_color(0, 0, 0)
            self.ln(13)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(107, 114, 128)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M UTC+4")
            self.cell(0, 10, f"{ts}   |   Page {self.page_no()}", align="C")

    pdf = Report()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 18, 15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 23, 42)
    pdf.ln(10)
    pdf.cell(0, 12, "AI Quality Coaching Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 8, datetime.now().strftime("%Y-%m-%d  %H:%M UTC+4"), ln=True, align="C")
    pdf.cell(0, 8, f"Total Interactions Analyzed: {len(items)}", ln=True, align="C")

    if items:
        avg = round(sum(x["call"]["csat_score"] for x in items) / len(items), 1)
        res = sum(1 for x in items if x["call"]["resolved"])
        pdf.ln(6)
        pdf.set_fill_color(239, 246, 255)
        pdf.set_draw_color(147, 197, 253)
        pdf.set_text_color(30, 58, 138)
        pdf.set_x(30)
        pdf.cell(150, 9, f"Avg CSAT: {avg}/5     Resolution Rate: {res}/{len(items)}", border=1, fill=True, align="C", ln=True)

    for item in items:
        call = item["call"]
        coaching = sanitize_pdf(item["coaching"])
        pdf.add_page()

        y0 = pdf.get_y()
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(15, y0, 180, 36, "FD")
        pdf.set_xy(19, y0 + 4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 7, sanitize_pdf(f"{call['call_id']}   |   {call['agent_name']} ({call['agent_id']})"), ln=True)
        pdf.set_x(19)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(55, 65, 81)
        dur = f"{call['duration_seconds']//60}m {call['duration_seconds']%60}s"
        pdf.cell(0, 6, sanitize_pdf(f"Sector: {call['sector']}    Queue: {call['queue']}    Duration: {dur}"), ln=True)
        pdf.set_x(19)
        outcome = "Resolved" if call["resolved"] else "Unresolved"
        pdf.cell(0, 6, sanitize_pdf(f"CSAT: {call['csat_score']}/5    Outcome: {outcome}    Sentiment: {call['sentiment']}    Risk: {call['risk_flag']}"), ln=True)
        pdf.set_xy(15, y0 + 38)
        pdf.ln(4)

        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 64, 175)
        pdf.cell(0, 7, "AI Coaching Analysis", ln=True)
        pdf.set_draw_color(30, 64, 175)
        pdf.set_line_width(0.5)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(31, 41, 55)
        pdf.multi_cell(180, 5.5, coaching.strip())

    return bytes(pdf.output())


# ── API SETUP ─────────────────────────────────────────────────────────────────────
load_dotenv()
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


# ── HELPERS ───────────────────────────────────────────────────────────────────────
def dur(sec): return f"{sec//60}m {sec%60}s"

def csat_b(n):
    if n >= 4: return f'<span class="b-green">★ {n} / 5</span>'
    if n == 3: return f'<span class="b-amber">★ {n} / 5</span>'
    return f'<span class="b-red">★ {n} / 5</span>'

def risk_b(f):
    if f == "None":         return '<span class="b-gray">✓ None</span>'
    if f == "Churn Risk":   return '<span class="b-amber">⚠ Churn Risk</span>'
    return '<span class="b-red">🚨 Compliance</span>'

def sent_b(s):
    if s == "Positive": return '<span class="b-green">↑ Positive</span>'
    if s == "Neutral":  return '<span class="b-gray">→ Neutral</span>'
    return '<span class="b-red">↓ Negative</span>'

def res_b(r):
    return '<span class="b-green">✓ Resolved</span>' if r else '<span class="b-red">✗ Open</span>'

def stream_coaching(call: dict):
    if not client:
        yield "⚠  No API key. Add GEMINI_API_KEY to .streamlit/secrets.toml"
        return
    try:
        stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=build_coaching_prompt(call),
            config=types.GenerateContentConfig(system_instruction=COACHING_SYSTEM_PROMPT)
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n⚠  Error: {e}"

def coaching_box(text: str):
    """Render coaching text in a dark high-contrast box."""
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f"""
    <div style="
        background: #1e293b;
        color: #f1f5f9;
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 24px 28px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13.5px;
        line-height: 1.85;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: 0 4px 20px rgba(0,0,0,0.18);
        margin-top: 8px;
    "><span style="display:block;font-size:9px;color:#64748b;letter-spacing:0.18em;
        margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #334155;">
    AI COACHING ENGINE  •  OUTPUT</span>{safe}</div>
    """, unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # ── Brand ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="padding:20px 4px 14px;">
            <div style="font-size:19px;font-weight:700;letter-spacing:0.1em;color:#58a6ff;">
                ⬡ {PLATFORM}
            </div>
            <div style="font-size:9.5px;color:#8b949e;letter-spacing:0.12em;
                        text-transform:uppercase;margin-top:4px;">{TAGLINE}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #21262d;margin-bottom:12px;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px;">Platform Modules</div>', unsafe_allow_html=True)

        # ── Expandable module tree ────────────────────────────────────────
        for mod in MODULES:
            is_active = st.session_state.active_module == mod["key"]
            if mod["available"]:
                with st.expander(f"{mod['icon']}  {mod['name']}", expanded=is_active):
                    for icon, name, desc in [("◈","Call Intelligence","Multi-select & profile"),
                                              ("⬡","AI Coaching Engine","Stream coaching reports"),
                                              ("⬇","Reports & Export","Download JSON / PDF")]:
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;padding:6px 8px;
                                    border-radius:6px;background:rgba(88,166,255,0.07);
                                    border:1px solid rgba(88,166,255,0.15);margin-bottom:4px;">
                            <span style="color:#58a6ff;font-size:12px;">{icon}</span>
                            <div>
                                <div style="font-size:11px;color:#c9d1d9;font-weight:500;">{name}</div>
                                <div style="font-size:9.5px;color:#6e7681;">{desc}</div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    if not is_active:
                        if st.button("Open Module", key=f"open_{mod['key']}"):
                            st.session_state.active_module = mod["key"]
                            st.rerun()
            else:
                progress   = mod.get("progress", 0)
                milestones = mod.get("milestones", [])
                done_n     = sum(1 for _, d in milestones if d)
                fc = "#16a34a" if progress >= 80 else "#d97706" if progress >= 50 else "#2563eb"
                with st.expander(f"{mod['icon']}  {mod['name']}", expanded=False):
                    st.markdown(f"""
                    <div style="padding:2px 0 10px;">
                        <div style="display:flex;justify-content:space-between;
                                    font-size:10px;color:#6b7280;font-weight:600;
                                    text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">
                            <span>Progress</span><span style="color:{fc};">{progress}%</span>
                        </div>
                        <div style="background:#21262d;border-radius:99px;height:4px;overflow:hidden;">
                            <div style="width:{progress}%;height:100%;background:{fc};border-radius:99px;"></div>
                        </div>
                        <div style="font-size:10px;color:#6e7681;margin-top:5px;">{done_n}/{len(milestones)} milestones done</div>
                    </div>""", unsafe_allow_html=True)
                    for ms, done in milestones:
                        c = "#3fb950" if done else "#6e7681"
                        i = "✓" if done else "○"
                        st.markdown(f'<div style="font-size:11px;color:{c};padding:2px 0;">{i}&nbsp;&nbsp;{ms}</div>', unsafe_allow_html=True)
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                    if st.button("View Preview", key=f"nav_{mod['key']}"):
                        st.session_state.active_module = mod["key"]
                        st.rerun()

        # ── System status ─────────────────────────────────────────────────
        st.markdown("""
        <div style="border-top:1px solid #21262d;padding:14px 0 8px;margin-top:12px;">
            <div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;">System Status</div>
            <div style="font-size:12px;color:#8b949e;line-height:2.4;">
                <span class="dot-g"></span>&nbsp;&nbsp;AI Engine&nbsp;
                <span style="float:right;color:#3fb950;font-weight:700;font-size:11px;">ONLINE</span><br>
                <span class="dot-g"></span>&nbsp;&nbsp;Data Pipeline&nbsp;
                <span style="float:right;color:#3fb950;font-weight:700;font-size:11px;">ONLINE</span><br>
                <span class="dot-b"></span>&nbsp;&nbsp;API Gateway&nbsp;
                <span style="float:right;color:#58a6ff;font-weight:700;font-size:11px;">ACTIVE</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Footer ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="border-top:1px solid #21262d;padding:10px 0 14px;margin-top:4px;">
            <div class="mono" style="font-size:10px;color:#6e7681;">{VERSION} &nbsp;|&nbsp; Build {BUILD_DATE}</div>
            <div style="font-size:9px;color:#30363d;margin-top:3px;">© 2026 DEMO</div>
        </div>""", unsafe_allow_html=True)


# ── QM ANALYZER ──────────────────────────────────────────────────────────────────
def render_qm():
    import pandas as pd

    # ── Page header ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:2px solid #e2e8f0;margin-bottom:8px;">
        <div style="font-size:10px;color:#9ca3af;letter-spacing:0.12em;text-transform:uppercase;font-weight:700;margin-bottom:6px;">
            {PLATFORM} &nbsp;›&nbsp; QM Analyzer
        </div>
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;">
            <div>
                <div class="page-title">Call Quality Intelligence Engine</div>
                <div style="font-size:13px;color:#6b7280;margin-top:4px;font-weight:500;">
                    AI-powered evaluation, coaching, and risk detection across all interactions
                </div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
                <span class="b-green">◉ LIVE SESSION</span>
                <div class="mono" style="margin-top:6px;font-size:10px;">
                    {datetime.now().strftime('%Y-%m-%d  %H:%M UTC+4')}
                </div>
            </div>
        </div>
    </div>
    <div class="scanbar"></div>
    """, unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["◈  CALL INTELLIGENCE", "⬡  COACHING RESULTS", "⬇  REPORTS & EXPORT"])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab1:
        # ── Build table ─────────────────────────────────────────────────
        rows = []
        for c in SAMPLE_CALLS:
            coached = "✓" if c["call_id"] in st.session_state.coaching_results else "—"
            rows.append({"Call ID":c["call_id"],"Agent":c["agent_name"],"Sector":c["sector"],
                          "Queue":c["queue"],"Duration":dur(c["duration_seconds"]),
                          "CSAT":c["csat_score"],"Resolved":"Yes" if c["resolved"] else "No",
                          "Sentiment":c["sentiment"],"Risk":c["risk_flag"],"Coached":coached})

        st.markdown('<div class="slabel" style="margin-bottom:8px;">Interaction Log — Click rows to select (Shift = range, Ctrl/Cmd = multi-pick)</div>', unsafe_allow_html=True)

        event = st.dataframe(
            pd.DataFrame(rows),
            on_select="rerun",
            selection_mode="multi-row",
            use_container_width=True,
            hide_index=True,
            key="calls_table",
            column_config={
                "CSAT":    st.column_config.NumberColumn("CSAT ★", format="%d / 5"),
                "Call ID": st.column_config.TextColumn("Call ID", width="small"),
                "Queue":   st.column_config.TextColumn("Queue", width="large"),
                "Coached": st.column_config.TextColumn("Coached", width="small"),
            },
        )

        # ── FIX: always sync selection from event (clears properly too) ─
        sel_rows = list(event.selection.rows) if (event.selection and event.selection.rows) else []
        st.session_state.selected_indices = sel_rows   # always update, even to []
        sel_calls    = [SAMPLE_CALLS[i] for i in sel_rows]
        display_calls = sel_calls if sel_calls else SAMPLE_CALLS
        n             = len(display_calls)

        # ── Dynamic metrics ──────────────────────────────────────────────
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        acsat = round(sum(c["csat_score"] for c in display_calls) / n, 1)
        res   = sum(1 for c in display_calls if c["resolved"])
        flag  = sum(1 for c in display_calls if c["risk_flag"] != "None")
        ags   = len(set(c["agent_id"] for c in display_calls))
        done  = sum(1 for c in display_calls if c["call_id"] in st.session_state.coaching_results)

        # Label changes based on selection — resets correctly when deselected
        m_label = f"Selected  ({n})" if sel_calls else "Total Interactions"

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: st.metric(m_label, n)
        with c2: st.metric("Avg CSAT", f"{acsat}/5")
        with c3: st.metric("Resolution Rate", f"{res/n*100:.0f}%", f"{res}/{n}")
        with c4: st.metric("Risk Flagged", flag, delta="Review needed" if flag else "None flagged", delta_color="inverse")
        with c5: st.metric("Agents", ags)
        with c6: st.metric("AI Coached", done, f"of {n}")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── Selection panel ──────────────────────────────────────────────
        if not sel_rows:
            st.info("💡 Click any row above to load an interaction profile. Hold **Shift** or **Ctrl** to select multiple calls for batch coaching.")

        elif len(sel_rows) == 1:
            call = sel_calls[0]
            cc = ("qm-card-green" if call["csat_score"] >= 4 else
                  "qm-card-amber" if call["csat_score"] == 3 else "qm-card-red")
            st.markdown(f"""
            <div class="{cc}">
                <div class="slabel" style="margin-bottom:14px;">Selected Interaction Profile</div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-bottom:16px;">
                    <div>
                        <div class="dlabel">Call ID</div><div class="dmono">{call['call_id']}</div>
                        <div class="dlabel">Agent</div><div class="dvalue">{call['agent_name']}</div>
                        <div class="dlabel">Agent ID</div><div class="dmono">{call['agent_id']}</div>
                    </div>
                    <div>
                        <div class="dlabel">Sector</div><div class="dvalue">{call['sector']}</div>
                        <div class="dlabel">Queue</div><div class="dvalue" style="font-size:12px;">{call['queue']}</div>
                    </div>
                    <div>
                        <div class="dlabel">Duration</div><div class="dvalue">{dur(call['duration_seconds'])}</div>
                        <div class="dlabel">CSAT Score</div><div style="margin-bottom:12px;">{csat_b(call['csat_score'])}</div>
                        <div class="dlabel">Outcome</div><div style="margin-bottom:12px;">{res_b(call['resolved'])}</div>
                    </div>
                    <div>
                        <div class="dlabel">Sentiment</div><div style="margin-bottom:12px;">{sent_b(call['sentiment'])}</div>
                        <div class="dlabel">Risk Flag</div><div style="margin-bottom:12px;">{risk_b(call['risk_flag'])}</div>
                        <div class="dlabel">AI Coached</div>
                        <div>{'<span class="b-green">✓ Done</span>' if call["call_id"] in st.session_state.coaching_results else '<span class="b-gray">Pending</span>'}</div>
                    </div>
                </div>
                <div class="dlabel">Transcript Summary</div>
                <div style="font-size:13px;color:#374151;line-height:1.7;
                            background:rgba(0,0,0,0.04);border-radius:8px;padding:12px 16px;
                            border:1px solid rgba(0,0,0,0.08);">{call['transcript_summary']}</div>
            </div>""", unsafe_allow_html=True)

            if not st.session_state.coach_triggered:
                if st.button(f"⬡  INITIATE AI COACHING  —  {call['call_id']}", key="btn_s"):
                    st.session_state.coach_queue    = sel_calls
                    st.session_state.coach_triggered = True

        else:
            # Multiple selected
            already = [c for c in sel_calls if c["call_id"] in st.session_state.coaching_results]
            pending = [c for c in sel_calls if c["call_id"] not in st.session_state.coaching_results]
            agents_s  = list(set(c["agent_name"] for c in sel_calls))
            sectors_s = list(set(c["sector"] for c in sel_calls))
            st.markdown(f"""
            <div class="qm-card-blue">
                <div class="slabel" style="margin-bottom:12px;">Batch Selection — {len(sel_rows)} Interactions</div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:12px;">
                    <div>
                        <div class="dlabel">Selected</div>
                        <div style="font-size:26px;font-weight:700;color:#1e40af;font-family:'JetBrains Mono',monospace;">{len(sel_rows)}</div>
                    </div>
                    <div>
                        <div class="dlabel">Avg CSAT</div>
                        <div style="font-size:26px;font-weight:700;color:#1e40af;font-family:'JetBrains Mono',monospace;">{round(sum(c['csat_score'] for c in sel_calls)/len(sel_calls),1)}</div>
                    </div>
                    <div>
                        <div class="dlabel">Already Coached</div>
                        <div style="font-size:26px;font-weight:700;color:#065f46;font-family:'JetBrains Mono',monospace;">{len(already)}</div>
                    </div>
                    <div>
                        <div class="dlabel">Pending</div>
                        <div style="font-size:26px;font-weight:700;color:#92400e;font-family:'JetBrains Mono',monospace;">{len(pending)}</div>
                    </div>
                </div>
                <div style="font-size:12px;color:#374151;font-weight:500;">
                    <b style="color:#1e40af;">Agents:</b> {', '.join(agents_s)} &nbsp;·&nbsp;
                    <b style="color:#1e40af;">Sectors:</b> {', '.join(sectors_s)}<br>
                    <b style="color:#1e40af;">Calls:</b> {', '.join(c['call_id'] for c in sel_calls)}
                </div>
            </div>""", unsafe_allow_html=True)

            if not st.session_state.coach_triggered:
                if st.button(f"⬡  START BATCH AI COACHING  —  {len(sel_rows)} INTERACTIONS", key="btn_b"):
                    st.session_state.coach_queue    = sel_calls
                    st.session_state.coach_triggered = True

        # ── Coaching output ──────────────────────────────────────────────
        if st.session_state.coach_triggered and st.session_state.coach_queue:
            st.divider()
            nq = len(st.session_state.coach_queue)
            st.markdown(f"""
            <div style="font-size:17px;font-weight:700;color:#111827;margin-bottom:6px;">
                ⬡ AI Coaching Analysis
                <span style="font-size:12px;font-weight:400;color:#6b7280;margin-left:10px;">
                    {nq} interaction{'s' if nq>1 else ''} queued
                </span>
            </div>
            <div style="font-size:13px;color:#4b5563;font-weight:500;margin-bottom:16px;">
                Generating coaching reports — results appear below and are saved automatically.
            </div>""", unsafe_allow_html=True)

            for call in st.session_state.coach_queue:
                call_id = call["call_id"]
                label   = f"◈  {call['agent_name']}  ·  {call_id}  ·  {call['sector']}  ·  CSAT {call['csat_score']}/5"
                with st.expander(label, expanded=True):
                    if call_id in st.session_state.coaching_results:
                        coaching_box(st.session_state.coaching_results[call_id])
                    else:
                        with st.spinner(f"Generating coaching for {call['agent_name']}..."):
                            full = st.write_stream(stream_coaching(call))
                        st.session_state.coaching_results[call_id] = full
                        st.rerun()

            all_done = all(c["call_id"] in st.session_state.coaching_results
                           for c in st.session_state.coach_queue)
            if all_done:
                st.success(f"✓  {nq} coaching report{'s' if nq>1 else ''} complete. View in COACHING RESULTS or download from REPORTS & EXPORT.")
                rc1, rc2 = st.columns(2)
                with rc1:
                    if st.button("↺  Clear & Select New Calls", key="reset_btn"):
                        st.session_state.coach_triggered  = False
                        st.session_state.coach_queue      = []
                        st.session_state.selected_indices = []
                        st.rerun()
                with rc2:
                    items = [{"call":c, "coaching":st.session_state.coaching_results[c["call_id"]]}
                             for c in st.session_state.coach_queue]
                    st.download_button(
                        label=f"⬇  Download Batch Report (JSON)",
                        data=json.dumps({"reports":[{"call":{k:v for k,v in i["call"].items()},
                                         "coaching":i["coaching"]} for i in items]}, indent=2),
                        file_name=f"coaching_batch_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json",
                        key="dl_batch"
                    )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — COACHING RESULTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab2:
        done_calls = [c for c in SAMPLE_CALLS if c["call_id"] in st.session_state.coaching_results]
        if not done_calls:
            st.markdown("""
            <div style="text-align:center;padding:60px 30px;color:#9ca3af;">
                <div style="font-size:42px;margin-bottom:14px;">⬡</div>
                <div style="font-size:18px;font-weight:600;color:#4b5563;margin-bottom:6px;">No Coaching Reports Yet</div>
                <div style="font-size:13px;">Go to <b style="color:#1e40af;">CALL INTELLIGENCE</b>, select interactions, and click the coaching button.</div>
            </div>""", unsafe_allow_html=True)
        else:
            t2c1, t2c2, t2c3 = st.columns(3)
            with t2c1: st.metric("Coaching Reports", len(done_calls))
            with t2c2:
                avg2 = round(sum(c["csat_score"] for c in done_calls)/len(done_calls), 1)
                st.metric("Avg CSAT (coached)", f"{avg2}/5")
            with t2c3:
                comp = sum(1 for c in done_calls if c["risk_flag"]=="Compliance Risk")
                st.metric("Compliance Flags", comp, delta_color="inverse")

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            for call in done_calls:
                cid = call["call_id"]
                coaching = st.session_state.coaching_results[cid]
                cc2 = ("qm-card-green" if call["csat_score"]>=4 else "qm-card-amber" if call["csat_score"]==3 else "qm-card-red")
                with st.expander(f"◈  {call['agent_name']}  ·  {cid}  ·  {call['sector']}  ·  CSAT {call['csat_score']}/5", expanded=False):
                    st.markdown(f"""
                    <div class="{cc2}" style="margin-bottom:14px;">
                        <div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center;">
                            <div><div class="dlabel">Agent</div><div class="dvalue" style="margin-bottom:0">{call['agent_name']}</div></div>
                            <div><div class="dlabel">Queue</div><div class="dvalue" style="margin-bottom:0;font-size:12px;">{call['queue']}</div></div>
                            <div><div class="dlabel">Duration</div><div class="dvalue" style="margin-bottom:0;">{dur(call['duration_seconds'])}</div></div>
                            <div><div class="dlabel">CSAT</div>{csat_b(call['csat_score'])}</div>
                            <div><div class="dlabel">Risk</div>{risk_b(call['risk_flag'])}</div>
                            <div><div class="dlabel">Outcome</div>{res_b(call['resolved'])}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    coaching_box(coaching)

                    dl2a, re2b = st.columns(2)
                    with dl2a:
                        st.download_button(
                            label="⬇  Download JSON",
                            data=json.dumps({"call":{k:v for k,v in call.items()},
                                             "coaching_report":coaching}, indent=2),
                            file_name=f"coaching_{cid}.json",
                            mime="application/json",
                            key=f"dl2_{cid}"
                        )
                    with re2b:
                        if st.button("↺  Re-generate", key=f"regen_{cid}"):
                            del st.session_state.coaching_results[cid]
                            st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — REPORTS & EXPORT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab3:
        analyzed = [c for c in SAMPLE_CALLS if c["call_id"] in st.session_state.coaching_results]
        pending  = [c for c in SAMPLE_CALLS if c["call_id"] not in st.session_state.coaching_results]

        r1, r2, r3 = st.columns(3)
        with r1: st.metric("AI Coached",    len(analyzed), f"of {len(SAMPLE_CALLS)}")
        with r2: st.metric("Pending",       len(pending))
        with r3:
            comp3 = sum(1 for c in analyzed if c["risk_flag"]=="Compliance Risk")
            st.metric("Compliance Flags", comp3, delta_color="inverse")

        if not analyzed:
            st.markdown("""
            <div style="text-align:center;padding:50px 30px;color:#9ca3af;">
                <div style="font-size:36px;margin-bottom:12px;">⬡</div>
                <div>No coaching reports yet. Return to <b style="color:#1e40af;">Call Intelligence</b> to analyze interactions.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-bottom:8px;">Completed Reports</div>', unsafe_allow_html=True)
            rep = [{"Call ID":c["call_id"],"Agent":c["agent_name"],"Sector":c["sector"],
                    "CSAT":f"{c['csat_score']}/5","Risk":c["risk_flag"],
                    "Outcome":"Resolved" if c["resolved"] else "Open","Status":"✓ Complete"}
                   for c in analyzed]
            st.dataframe(pd.DataFrame(rep), use_container_width=True, hide_index=True)
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-bottom:10px;">Bulk Download</div>', unsafe_allow_html=True)

            items3 = [{"call":c,"coaching":st.session_state.coaching_results[c["call_id"]]} for c in analyzed]
            json3  = json.dumps({"export_source":"DEMO QM Platform","platform_version":VERSION,
                                  "exported_at":datetime.now().isoformat(),
                                  "coached_count":len(analyzed),
                                  "reports":[{"call":{k:v for k,v in i["call"].items() if k!="transcript_summary"},
                                              "transcript_summary":i["call"]["transcript_summary"],
                                              "coaching_report":i["coaching"]} for i in items3]}, indent=2)
            d1, d2 = st.columns(2)
            with d1:
                st.download_button(f"⬇  Download All — JSON  ({len(analyzed)} reports)",
                                   data=json3,
                                   file_name=f"QM_Export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                                   mime="application/json", key="dl_all_json")
            with d2:
                if FPDF_AVAILABLE:
                    try:
                        pdf_b = generate_pdf(items3)
                        st.download_button(f"⬇  Download All — PDF  ({len(analyzed)} reports)",
                                           data=pdf_b,
                                           file_name=f"QM_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                           mime="application/pdf", key="dl_all_pdf")
                    except Exception as e:
                        st.error(f"PDF error: {e}")
                else:
                    st.info("Add `fpdf2` to requirements.txt for PDF export.")


# ── COMING SOON ───────────────────────────────────────────────────────────────────
def render_coming_soon(mod: dict):
    progress   = mod.get("progress", 50)
    milestones = mod.get("milestones", [])
    fc = "pfill-green" if progress>=80 else "pfill-amber" if progress>=50 else "pfill-blue"

    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:2px solid #e2e8f0;margin-bottom:24px;">
        <div style="font-size:10px;color:#9ca3af;letter-spacing:0.12em;text-transform:uppercase;font-weight:700;margin-bottom:6px;">
            {PLATFORM} &nbsp;›&nbsp; {mod['name']}
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="font-size:24px;font-weight:700;color:#374151;">{mod['name']}</div>
            <span class="b-lock">COMING SOON</span>
        </div>
    </div>
    <div class="scanbar"></div>
    <div class="cs-hero">
        <div style="font-size:52px;margin-bottom:16px;opacity:0.18;color:#374151;">{mod['icon']}</div>
        <div style="font-size:22px;font-weight:700;color:#1e293b;margin-bottom:8px;">{mod['name']}</div>
        <div style="font-size:13px;color:#6b7280;max-width:480px;margin:0 auto 28px;line-height:1.6;font-weight:500;">
            This module is in active development and will be released in an upcoming update.
        </div>
        <div style="max-width:340px;margin:0 auto;">
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        color:#4b5563;font-weight:700;text-transform:uppercase;margin-bottom:8px;">
                <span>Development Progress</span><span style="color:#1e40af;">{progress}%</span>
            </div>
            <div class="ptrack"><div class="{fc}" style="width:{progress}%;"></div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    if milestones:
        st.markdown('<div class="slabel" style="margin-bottom:12px;">Development Milestones</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (ms, done) in enumerate(milestones):
            with cols[i%2]:
                icon = "✓" if done else "○"
                c    = "#065f46" if done else "#6b7280"
                bg   = "#f0fdf4" if done else "#f9fafb"
                brd  = "#4ade80" if done else "#e5e7eb"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:11px 14px;
                            background:{bg};border:1.5px solid {brd};border-radius:10px;margin-bottom:8px;">
                    <span style="color:{c};font-size:14px;font-weight:700;">{icon}</span>
                    <span style="font-size:13px;color:{'#374151' if done else '#9ca3af'};font-weight:{'600' if done else '400'};">{ms}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button(f"🔔  Request Early Access — {mod['name']}", key=f"ea_{mod['key']}"):
        st.success(f"✓  Request submitted for **{mod['name']}**. You will be notified when this module becomes available.")


# ── MAIN ROUTING ──────────────────────────────────────────────────────────────────
render_sidebar()

active = st.session_state.active_module
if active == "qm":
    render_qm()
else:
    mod_data = next((m for m in MODULES if m["key"] == active), None)
    if mod_data:
        render_coming_soon(mod_data)