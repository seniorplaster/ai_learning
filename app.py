"""
ARIA — Agentic Review & Intelligence Analytics
CCaaS Contact Center AI Quality Management Platform
Version 2.4.1  |  Build 2026.06
"""

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ── PAGE CONFIG — must be first Streamlit command ────────────────────────
st.set_page_config(
    page_title="ARIA | AI Quality Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DESIGN SYSTEM & CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
header    {visibility: hidden;}
.block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── APP BACKGROUND ── */
.stApp {
    background: #070c18;
    background-image:
        radial-gradient(ellipse at 12% 40%, rgba(0,212,255,0.045) 0%, transparent 55%),
        radial-gradient(ellipse at 88% 12%, rgba(37,99,235,0.06)  0%, transparent 55%),
        radial-gradient(ellipse at 50% 95%, rgba(5,150,105,0.03)  0%, transparent 50%);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #030609 0%, #070c18 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.13) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* Sidebar buttons styled as nav items */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #475569 !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    text-align: left !important;
    padding: 9px 14px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.18s ease !important;
    margin-bottom: 2px !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    transform: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,212,255,0.06) !important;
    color: #94a3b8 !important;
    border-color: rgba(0,212,255,0.12) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── MAIN AREA BUTTONS ── */
.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    background: linear-gradient(135deg, #0f2a5e, #0a1a3d) !important;
    color: #00d4ff !important;
    border: 1px solid rgba(0,212,255,0.32) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: linear-gradient(135deg, #183880, #0f2060) !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 22px rgba(0,212,255,0.22), inset 0 0 12px rgba(0,212,255,0.03) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}
.main .stButton > button:active,
[data-testid="stMainBlockContainer"] .stButton > button:active {
    transform: translateY(0) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #054335, #065040) !important;
    color: #10b981 !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    width: 100% !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 22px rgba(16,185,129,0.2) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0b1322 !important;
    border-radius: 10px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border-radius: 7px !important;
    padding: 9px 24px !important;
    font-weight: 500 !important;
    font-size: 12px !important;
    letter-spacing: 0.07em !important;
    border: none !important;
    transition: color 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.13), rgba(37,99,235,0.13)) !important;
    color: #00d4ff !important;
    border: 1px solid rgba(0,212,255,0.28) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.8rem !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #090f1f, #0b1220) !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #00d4ff !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stDataFrameResizable"] {
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 12px !important;
}

/* ── ALERTS ── */
[data-baseweb="notification"] {
    background-color: rgba(0,212,255,0.07) !important;
    border: 1px solid rgba(0,212,255,0.18) !important;
    border-radius: 10px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,212,255,0.4); }

/* ── COMPONENT CLASSES ── */
.aria-card {
    background: linear-gradient(135deg, #090f1f, #0b1525);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-green {
    background: linear-gradient(135deg, #03110a, #041510);
    border: 1px solid rgba(5,150,105,0.18);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-amber {
    background: linear-gradient(135deg, #140d03, #180f04);
    border: 1px solid rgba(245,158,11,0.18);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-red {
    background: linear-gradient(135deg, #130404, #170505);
    border: 1px solid rgba(239,68,68,0.22);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.gradient-text {
    background: linear-gradient(135deg, #00d4ff, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}
.gradient-text-green {
    background: linear-gradient(135deg, #10b981, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}
.mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #64748b; }
.section-label {
    font-size: 10px; font-weight: 600; color: #334155;
    text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 6px;
}
.badge-online  { display:inline-block; background:rgba(5,150,105,0.12);  color:#10b981; border:1px solid rgba(5,150,105,0.25);  border-radius:99px; padding:2px 10px; font-size:10px; font-weight:600; letter-spacing:0.08em; }
.badge-blue    { display:inline-block; background:rgba(0,212,255,0.1);   color:#00d4ff; border:1px solid rgba(0,212,255,0.25);  border-radius:99px; padding:2px 10px; font-size:10px; font-weight:600; letter-spacing:0.08em; }
.badge-amber   { display:inline-block; background:rgba(245,158,11,0.1);  color:#f59e0b; border:1px solid rgba(245,158,11,0.25); border-radius:99px; padding:2px 10px; font-size:10px; font-weight:600; letter-spacing:0.08em; }
.badge-red     { display:inline-block; background:rgba(239,68,68,0.1);   color:#ef4444; border:1px solid rgba(239,68,68,0.25);  border-radius:99px; padding:2px 10px; font-size:10px; font-weight:600; letter-spacing:0.08em; }
.badge-gray    { display:inline-block; background:rgba(100,116,139,0.1); color:#94a3b8; border:1px solid rgba(100,116,139,0.2); border-radius:99px; padding:2px 10px; font-size:10px; font-weight:600; letter-spacing:0.08em; }
.badge-lock    { display:inline-block; background:rgba(51,65,85,0.4);    color:#475569; border:1px solid rgba(51,65,85,0.5);    border-radius:99px; padding:2px 8px;  font-size:9px;  font-weight:600; letter-spacing:0.08em; }
.dot-green { display:inline-block; width:7px; height:7px; background:#10b981; border-radius:50%; box-shadow:0 0 7px #10b981; animation:pulse-g 2.2s infinite; }
.dot-blue  { display:inline-block; width:7px; height:7px; background:#00d4ff; border-radius:50%; box-shadow:0 0 7px #00d4ff; animation:pulse-b 2.2s infinite; }
.dot-amber { display:inline-block; width:7px; height:7px; background:#f59e0b; border-radius:50%; box-shadow:0 0 5px #f59e0b; }
@keyframes pulse-g { 0%,100%{opacity:1;} 55%{opacity:0.35;} }
@keyframes pulse-b { 0%,100%{opacity:1;} 55%{opacity:0.45;} }

.scan-bar {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #00d4ff 40%, #2563eb 60%, transparent 100%);
    animation: scan 4s ease-in-out infinite;
    opacity: 0.6;
    border-radius: 1px;
    margin: 6px 0 18px;
}
@keyframes scan { 0%{opacity:0.15;} 50%{opacity:0.7;} 100%{opacity:0.15;} }

.coaching-terminal {
    background: #04080f;
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 12px;
    padding: 24px 28px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.75;
    color: #cbd5e1;
    min-height: 120px;
    position: relative;
}
.coaching-terminal::before {
    content: "ARIA COACHING ENGINE  •  OUTPUT STREAM";
    display: block;
    font-size: 9px;
    color: #334155;
    letter-spacing: 0.14em;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0,212,255,0.07);
}
.detail-label { font-size: 10px; color: #334155; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; margin-bottom: 3px; }
.detail-value { font-size: 14px; color: #e2e8f0; font-weight: 500; margin-bottom: 14px; }
.detail-mono  { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #64748b; margin-bottom: 14px; }

.progress-track {
    background: #0d1526;
    border-radius: 99px;
    height: 4px;
    overflow: hidden;
    border: 1px solid rgba(0,212,255,0.07);
}
.progress-fill-blue  { height: 100%; background: linear-gradient(90deg, #2563eb, #00d4ff); border-radius: 99px; }
.progress-fill-green { height: 100%; background: linear-gradient(90deg, #059669, #10b981); border-radius: 99px; }
.progress-fill-amber { height: 100%; background: linear-gradient(90deg, #d97706, #f59e0b); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── PLATFORM CONSTANTS ───────────────────────────────────────────────────
PLATFORM   = "ARIA"
TAGLINE    = "Agentic Review & Intelligence Analytics"
VERSION    = "v2.4.1"
BUILD_DATE = "2026.06"

MODULES = [
    {"key": "qm",        "name": "QM Analyzer",            "icon": "◈", "available": True,  "progress": 100},
    {"key": "wfm",       "name": "WFM Scheduler",          "icon": "◉", "available": False, "progress": 78,
     "milestones": [("Demand Forecasting Engine", True), ("Schedule Optimiser", True), ("Shift Bidding Portal", False), ("Real-Time Adherence Feed", False)]},
    {"key": "ia",        "name": "Interaction Analytics",  "icon": "◈", "available": False, "progress": 64,
     "milestones": [("Call Transcription Pipeline", True), ("Sentiment Trend Dashboard", True), ("Topic Clustering", False), ("Compliance Phrase Detection", False)]},
    {"key": "scoreboard","name": "Agent Scoreboard",       "icon": "◉", "available": False, "progress": 89,
     "milestones": [("KPI Calculation Engine", True), ("Team Leaderboard UI", True), ("Gamification Badges", True), ("Manager Approval Workflow", False)]},
    {"key": "hiring",    "name": "Agent Hiring Insights",  "icon": "◈", "available": False, "progress": 41,
     "milestones": [("Candidate Scoring Model", True), ("Interview Question Generator", False), ("Predicted Attrition Index", False), ("Skills Gap Heatmap", False)]},
    {"key": "assist",    "name": "Agent Assist",           "icon": "◉", "available": False, "progress": 55,
     "milestones": [("Real-Time Transcription", True), ("Knowledge Base Search", True), ("Next-Best-Action Engine", False), ("Auto-Draft Response", False)]},
    {"key": "sentiment", "name": "Live Sentiment Assist",  "icon": "◈", "available": False, "progress": 33,
     "milestones": [("Acoustic Model Training", True), ("Emotion Classification", False), ("Agent Alert System", False), ("Supervisor Escalation Feed", False)]},
]


# ── SAMPLE CALL DATA ─────────────────────────────────────────────────────
SAMPLE_CALLS = [
    {
        "call_id": "AR-2026-0091",
        "agent_id": "AGT-101",
        "agent_name": "Sara Al Mansoori",
        "sector": "Banking",
        "queue": "Premier Banking — Disputes",
        "duration_seconds": 187,
        "csat_score": 5,
        "resolved": True,
        "sentiment": "Positive",
        "risk_flag": "None",
        "transcript_summary": (
            "Customer called about an unauthorized transaction on their premium Visa card. "
            "Agent Sara verified identity using multi-factor authentication within 60 seconds, "
            "immediately initiated a chargeback process, explained the 5–7 business-day timeline "
            "clearly, and proactively offered a temporary credit limit increase as a goodwill gesture. "
            "Customer expressed high satisfaction and thanked the agent by name."
        ),
    },
    {
        "call_id": "AR-2026-0092",
        "agent_id": "AGT-205",
        "agent_name": "Mohammed Al Rashidi",
        "sector": "Telecom",
        "queue": "Technical Support — Mobile",
        "duration_seconds": 643,
        "csat_score": 2,
        "resolved": False,
        "sentiment": "Negative",
        "risk_flag": "Churn Risk",
        "transcript_summary": (
            "Customer reported mobile data not working for 3 consecutive days. Agent took 8 minutes "
            "to locate the account despite the customer providing the account number upfront. Asked "
            "customer to repeat details twice. Did not check the network outage map before "
            "troubleshooting. Failed to offer escalation to the technical team, compensation, or a "
            "callback. Customer stated they would switch to a competitor at the end of the call."
        ),
    },
    {
        "call_id": "AR-2026-0093",
        "agent_id": "AGT-310",
        "agent_name": "Fatima Al Zahra",
        "sector": "Government",
        "queue": "Licensing Services",
        "duration_seconds": 245,
        "csat_score": 4,
        "resolved": True,
        "sentiment": "Neutral",
        "risk_flag": "None",
        "transcript_summary": (
            "Citizen called to inquire about trade license renewal requirements and applicable fees. "
            "Agent Fatima provided clear step-by-step guidance, confirmed eligibility criteria, and "
            "sent a digital checklist via SMS during the call. A brief delay occurred when accessing "
            "the updated fee schedule system, but the correct information was confirmed and the citizen "
            "confirmed readiness to proceed."
        ),
    },
    {
        "call_id": "AR-2026-0094",
        "agent_id": "AGT-101",
        "agent_name": "Sara Al Mansoori",
        "sector": "Healthcare",
        "queue": "Patient Services — Cardiology",
        "duration_seconds": 312,
        "csat_score": 5,
        "resolved": True,
        "sentiment": "Positive",
        "risk_flag": "None",
        "transcript_summary": (
            "Patient called to schedule a cardiology follow-up appointment and inquire about "
            "insurance pre-authorization for an MRI scan. Agent Sara efficiently coordinated between "
            "two departments, secured a same-week appointment slot, and initiated the pre-authorization "
            "form with the insurance team. Patient expressed strong gratitude for the seamless, "
            "end-to-end experience."
        ),
    },
    {
        "call_id": "AR-2026-0095",
        "agent_id": "AGT-422",
        "agent_name": "Khalid Al Nuaimi",
        "sector": "Insurance",
        "queue": "Claims Processing — Motor",
        "duration_seconds": 521,
        "csat_score": 1,
        "resolved": False,
        "sentiment": "Negative",
        "risk_flag": "Compliance Risk",
        "transcript_summary": (
            "Customer called about a denied motor insurance claim filed 3 weeks ago. Agent Khalid "
            "could not locate the claim in the CRM for 11 minutes. Transferred the customer twice "
            "without warning or context handover. When the claim was finally found, provided incorrect "
            "information about the appeals process and the regulatory timeline. Customer stated they "
            "would file a formal complaint with the UAE Insurance Authority (CBUAE)."
        ),
    },
    {
        "call_id": "AR-2026-0096",
        "agent_id": "AGT-205",
        "agent_name": "Mohammed Al Rashidi",
        "sector": "Banking",
        "queue": "Retail Banking — Loans",
        "duration_seconds": 198,
        "csat_score": 3,
        "resolved": True,
        "sentiment": "Neutral",
        "risk_flag": "None",
        "transcript_summary": (
            "Customer inquired about eligibility for a personal loan and current interest rates. "
            "Agent Mohammed provided the standard rate bands but could not run a live pre-qualification "
            "check because the credit-check tool was temporarily unavailable. Offered a callback from "
            "the loans specialist team within 24 hours. Customer accepted the callback but expressed "
            "mild frustration about not receiving an immediate eligibility answer."
        ),
    },
    {
        "call_id": "AR-2026-0097",
        "agent_id": "AGT-310",
        "agent_name": "Fatima Al Zahra",
        "sector": "Telecom",
        "queue": "Enterprise Sales — Upgrades",
        "duration_seconds": 289,
        "csat_score": 4,
        "resolved": True,
        "sentiment": "Positive",
        "risk_flag": "None",
        "transcript_summary": (
            "Enterprise customer called to upgrade their corporate data plan from 100 GB to 500 GB "
            "and add 3 additional SIM cards for new employees. Agent Fatima processed the upgrade "
            "request, applied the eligible corporate bundle discount automatically, confirmed the "
            "activation timeline as next billing cycle, and emailed the updated contract immediately. "
            "Customer appreciated the professional and efficient handling."
        ),
    },
    {
        "call_id": "AR-2026-0098",
        "agent_id": "AGT-422",
        "agent_name": "Khalid Al Nuaimi",
        "sector": "Government",
        "queue": "Complaints & Escalation",
        "duration_seconds": 614,
        "csat_score": 2,
        "resolved": False,
        "sentiment": "Negative",
        "risk_flag": "Compliance Risk",
        "transcript_summary": (
            "Resident called to formally escalate a permit approval that was 18 days beyond the "
            "legally mandated 30-day processing window. Agent Khalid was unaware of the statutory SLA "
            "requirement. Did not log the complaint in the government CRM during the call. Provided "
            "vague reassurances with no concrete escalation path, no reference number, and no "
            "supervisor involvement. Resident stated they would contact the relevant oversight body."
        ),
    },
    {
        "call_id": "AR-2026-0099",
        "agent_id": "AGT-101",
        "agent_name": "Sara Al Mansoori",
        "sector": "Healthcare",
        "queue": "Insurance & Billing — Disputes",
        "duration_seconds": 156,
        "csat_score": 5,
        "resolved": True,
        "sentiment": "Positive",
        "risk_flag": "None",
        "transcript_summary": (
            "Patient called to dispute an erroneous additional consultation fee on their last hospital "
            "invoice. Agent Sara identified the billing discrepancy immediately by cross-referencing "
            "clinical notes and the billing system. Initiated a credit note on the spot, confirmed the "
            "refund would appear within 3–5 working days, and apologised on behalf of the hospital. "
            "Patient was fully satisfied with the resolution speed."
        ),
    },
]


# ── AI COACHING CONFIG ───────────────────────────────────────────────────
COACHING_SYSTEM_PROMPT = """You are ARIA's AI Coaching Engine — a senior contact center quality expert with 25 years of experience across banking, telecom, healthcare, government, and insurance sectors in the GCC region.

Your coaching reports are structured, specific, and actionable. You do not give generic advice — every recommendation must reference the actual events described in the call summary.

Format every coaching report with these exact sections:

**PERFORMANCE SUMMARY**
A 2–3 sentence overall assessment of this specific interaction.

**STRENGTHS IDENTIFIED**
2–3 bullet points of what the agent did well, referencing specific actions in this call. If there are no genuine strengths, state that honestly.

**CRITICAL IMPROVEMENT AREAS**
3–4 numbered coaching points. Each must reference a specific moment in the call and explain the impact.

**RECOMMENDED ACTIONS**
Concrete next steps: specific training modules, role-play scenarios, process reminders, or escalation procedures the agent should review.

**COACHING PRIORITY**
End with exactly one of these ratings on its own line:
🟢 PRIORITY: LOW
🟡 PRIORITY: MEDIUM
🔴 PRIORITY: HIGH
🚨 PRIORITY: URGENT — Compliance Review Required

Write in a professional, direct tone. Do not soften critical feedback. Be honest."""


def build_coaching_prompt(call: dict) -> str:
    duration_m = call["duration_seconds"] // 60
    duration_s = call["duration_seconds"] % 60
    resolved_str = "RESOLVED ✓" if call["resolved"] else "UNRESOLVED ✗"
    return f"""Generate a full coaching report for the following contact center interaction.

═══════════════════════════════════════════════════════
CALL RECORD: {call['call_id']}
═══════════════════════════════════════════════════════
AGENT:     {call['agent_name']}  ({call['agent_id']})
SECTOR:    {call['sector']}
QUEUE:     {call['queue']}
DURATION:  {duration_m}m {duration_s}s
CSAT:      {call['csat_score']} / 5
OUTCOME:   {resolved_str}
SENTIMENT: {call['sentiment']}
RISK FLAG: {call['risk_flag']}

CALL TRANSCRIPT SUMMARY:
{call['transcript_summary']}
═══════════════════════════════════════════════════════

Provide a full coaching report following your structured format. Be specific to this exact call — do not give generic advice."""


# ── API SETUP ────────────────────────────────────────────────────────────
load_dotenv()
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key:
    client = genai.Client(api_key=api_key)


# ── SESSION STATE ────────────────────────────────────────────────────────
for k, v in {
    "active_module":   "qm",
    "selected_idx":    None,
    "coaching_results": {},      # {call_id: full_text}
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────
def csat_html(score: int) -> str:
    color = {5: "#10b981", 4: "#10b981", 3: "#f59e0b", 2: "#ef4444", 1: "#ef4444"}.get(score, "#94a3b8")
    return f'<span style="color:{color};font-weight:700;font-family:\'JetBrains Mono\',monospace;">{"★"*score}{"☆"*(5-score)} {score}/5</span>'

def risk_html(flag: str) -> str:
    if flag == "None":              return '<span class="badge-gray">✓ None</span>'
    elif flag == "Churn Risk":      return '<span class="badge-amber">⚠ Churn Risk</span>'
    else:                           return '<span class="badge-red">🚨 Compliance Risk</span>'

def sentiment_html(s: str) -> str:
    color = {"Positive": "#10b981", "Neutral": "#94a3b8", "Negative": "#ef4444"}.get(s, "#94a3b8")
    icon  = {"Positive": "↑", "Neutral": "→", "Negative": "↓"}.get(s, "")
    return f'<span style="color:{color};font-weight:600;">{icon} {s}</span>'

def resolved_html(r: bool) -> str:
    return '<span class="badge-online">✓ RESOLVED</span>' if r else '<span class="badge-red">✗ OPEN</span>'

def duration_fmt(sec: int) -> str:
    return f"{sec//60}m {sec%60}s"

def stream_coaching(call: dict):
    """Generator for word-by-word streaming from Gemini."""
    if not client:
        yield "\n⚠️  No API key configured — add GEMINI_API_KEY to your .streamlit/secrets.toml or .env file.\n"
        return
    try:
        prompt = build_coaching_prompt(call)
        stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=COACHING_SYSTEM_PROMPT)
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n⚠️  Streaming error: {e}\n"


# ── SIDEBAR ───────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo / brand
        st.markdown(f"""
        <div style="padding:22px 18px 18px;border-bottom:1px solid rgba(0,212,255,0.1);margin-bottom:8px;">
            <div style="font-size:21px;font-weight:700;letter-spacing:0.14em;
                        background:linear-gradient(135deg,#00d4ff,#2563eb);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">
                ⬡ {PLATFORM}
            </div>
            <div style="font-size:9.5px;color:#334155;letter-spacing:0.14em;
                        text-transform:uppercase;margin-top:5px;line-height:1.5;">
                {TAGLINE}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="padding:10px 18px 4px;">Platform Modules</div>',
                    unsafe_allow_html=True)

        for mod in MODULES:
            lock = "" if mod["available"] else "  ⋯"
            label = f"{mod['icon']}  {mod['name'].upper()}{lock}"
            is_active = st.session_state.active_module == mod["key"]

            # Highlight active module with a glow strip
            if is_active:
                st.markdown(
                    f'<div style="margin:1px 8px;padding:9px 10px;'
                    f'background:rgba(0,212,255,0.07);border:1px solid rgba(0,212,255,0.2);'
                    f'border-radius:8px;font-size:12px;font-weight:600;letter-spacing:0.05em;'
                    f'color:#00d4ff;cursor:default;">{label}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(label, key=f"nav_{mod['key']}", use_container_width=True):
                    st.session_state.active_module = mod["key"]
                    st.rerun()

        # System status
        st.markdown("""
        <div style="padding:18px 18px 10px;margin-top:16px;
                    border-top:1px solid rgba(0,212,255,0.07);">
            <div class="section-label">System Status</div>
            <div style="font-size:12px;color:#64748b;margin-top:10px;line-height:2.2;">
                <span class="dot-green"></span>&nbsp;&nbsp;AI Engine
                &nbsp;<span style="float:right;color:#10b981;font-weight:600;font-size:11px;">ONLINE</span><br>
                <span class="dot-green"></span>&nbsp;&nbsp;Data Pipeline
                &nbsp;<span style="float:right;color:#10b981;font-weight:600;font-size:11px;">ONLINE</span><br>
                <span class="dot-blue"></span>&nbsp;&nbsp;API Gateway
                &nbsp;<span style="float:right;color:#00d4ff;font-weight:600;font-size:11px;">ACTIVE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="padding:12px 18px 18px;border-top:1px solid rgba(0,212,255,0.05);">
            <div class="mono" style="font-size:10px;">
                {VERSION} &nbsp;|&nbsp; Build {BUILD_DATE}
            </div>
            <div style="font-size:9px;color:#1e293b;margin-top:4px;letter-spacing:0.05em;">
                © 2026 ARIA Intelligence Inc.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── QM ANALYZER MODULE ────────────────────────────────────────────────────
def render_qm_analyzer():
    # Header
    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:1px solid rgba(0,212,255,0.08);margin-bottom:6px;">
        <div style="font-size:10px;color:#334155;letter-spacing:0.12em;text-transform:uppercase;
                    font-weight:600;margin-bottom:6px;">
            ARIA Platform &nbsp;›&nbsp; QM Analyzer
        </div>
        <div style="display:flex;align-items:flex-start;justify-content:space-between;">
            <div>
                <h1 style="font-size:24px;font-weight:700;margin:0;line-height:1.2;
                            background:linear-gradient(135deg,#00d4ff,#2563eb);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                            background-clip:text;">
                    Call Quality Intelligence Engine
                </h1>
                <div style="font-size:13px;color:#475569;margin-top:4px;">
                    AI-powered evaluation, coaching, and risk detection across all interactions
                </div>
            </div>
            <div style="text-align:right;flex-shrink:0;margin-left:20px;">
                <span class="badge-online">◉ LIVE SESSION</span>
                <div class="mono" style="margin-top:6px;font-size:10px;">
                    {datetime.now().strftime('%Y-%m-%d  %H:%M UTC+4')}
                </div>
            </div>
        </div>
    </div>
    <div class="scan-bar"></div>
    """, unsafe_allow_html=True)

    # Metrics
    total    = len(SAMPLE_CALLS)
    resolved = sum(1 for c in SAMPLE_CALLS if c["resolved"])
    avg_csat = round(sum(c["csat_score"] for c in SAMPLE_CALLS) / total, 1)
    flagged  = sum(1 for c in SAMPLE_CALLS if c["risk_flag"] != "None")
    agents   = len(set(c["agent_id"] for c in SAMPLE_CALLS))
    analyzed = len(st.session_state.coaching_results)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("Total Interactions", total)
    with c2: st.metric("Avg CSAT", f"{avg_csat}/5", "+0.3 WoW")
    with c3: st.metric("Resolution Rate", f"{resolved/total*100:.0f}%", f"{resolved}/{total}")
    with c4: st.metric("Risk Flagged", flagged, "Needs review", delta_color="inverse")
    with c5: st.metric("Active Agents", agents)
    with c6: st.metric("AI Coached", analyzed, f"of {total} calls")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "◈  CALL INTELLIGENCE",
        "⬡  AI COACHING ENGINE",
        "⬇  REPORTS & EXPORT",
    ])

    # ────────────── TAB 1 — CALL INTELLIGENCE ──────────────────────────
    with tab1:
        st.markdown("""
        <div class="section-label" style="margin-bottom:10px;">
            Interaction Log — Select a call to load its full profile and proceed to coaching
        </div>
        """, unsafe_allow_html=True)

        import pandas as pd

        # Build display DataFrame
        rows = []
        for c in SAMPLE_CALLS:
            coached = "✓ Done" if c["call_id"] in st.session_state.coaching_results else "—"
            rows.append({
                "Call ID":    c["call_id"],
                "Agent":      c["agent_name"],
                "Sector":     c["sector"],
                "Queue":      c["queue"],
                "Duration":   duration_fmt(c["duration_seconds"]),
                "CSAT":       c["csat_score"],
                "Resolved":   "Yes" if c["resolved"] else "No",
                "Sentiment":  c["sentiment"],
                "Risk Flag":  c["risk_flag"],
                "AI Coached": coached,
            })
        df = pd.DataFrame(rows)

        event = st.dataframe(
            df,
            on_select="rerun",
            selection_mode="single-row",
            use_container_width=True,
            hide_index=True,
            key="calls_table",
            column_config={
                "CSAT": st.column_config.NumberColumn("CSAT ★", format="%d / 5"),
                "Call ID": st.column_config.TextColumn("Call ID", width="small"),
                "Queue": st.column_config.TextColumn("Queue", width="large"),
            },
        )

        # Handle row selection
        if event.selection and event.selection.rows:
            idx = event.selection.rows[0]
            st.session_state.selected_idx = idx
        
        if st.session_state.selected_idx is not None:
            call = SAMPLE_CALLS[st.session_state.selected_idx]
            
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            
            # Colour the card by CSAT
            card_class = "aria-card-green" if call["csat_score"] >= 4 else \
                         "aria-card-amber" if call["csat_score"] == 3 else "aria-card-red"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size:10px;color:#334155;letter-spacing:0.12em;
                            text-transform:uppercase;font-weight:600;margin-bottom:14px;">
                    Selected Interaction Profile
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:16px;">
                    <div>
                        <div class="detail-label">Call ID</div>
                        <div class="detail-mono">{call['call_id']}</div>
                        <div class="detail-label">Agent</div>
                        <div class="detail-value">{call['agent_name']}</div>
                        <div class="detail-label">Agent ID</div>
                        <div class="detail-mono">{call['agent_id']}</div>
                    </div>
                    <div>
                        <div class="detail-label">Sector</div>
                        <div class="detail-value">{call['sector']}</div>
                        <div class="detail-label">Queue</div>
                        <div class="detail-value" style="font-size:12px;">{call['queue']}</div>
                    </div>
                    <div>
                        <div class="detail-label">Duration</div>
                        <div class="detail-value">{duration_fmt(call['duration_seconds'])}</div>
                        <div class="detail-label">CSAT Score</div>
                        <div style="margin-bottom:14px;">{csat_html(call['csat_score'])}</div>
                        <div class="detail-label">Outcome</div>
                        <div style="margin-bottom:14px;">{resolved_html(call['resolved'])}</div>
                    </div>
                    <div>
                        <div class="detail-label">Customer Sentiment</div>
                        <div style="margin-bottom:14px;">{sentiment_html(call['sentiment'])}</div>
                        <div class="detail-label">Risk Flag</div>
                        <div style="margin-bottom:14px;">{risk_html(call['risk_flag'])}</div>
                        <div class="detail-label">AI Coached</div>
                        <div style="margin-bottom:14px;">
                            {'<span class="badge-online">✓ Complete</span>' if call['call_id'] in st.session_state.coaching_results else '<span class="badge-gray">Pending</span>'}
                        </div>
                    </div>
                </div>
                <div class="detail-label">Transcript Summary</div>
                <div style="font-size:13px;color:#94a3b8;line-height:1.7;
                            background:rgba(0,0,0,0.25);border-radius:8px;padding:12px 16px;
                            border:1px solid rgba(255,255,255,0.04);">
                    {call['transcript_summary']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.info(f"💡 Call **{call['call_id']}** loaded — switch to the **AI COACHING ENGINE** tab to generate the coaching report.")

    # ────────────── TAB 2 — AI COACHING ENGINE ─────────────────────────
    with tab2:
        if st.session_state.selected_idx is None:
            st.markdown("""
            <div style="text-align:center;padding:60px 40px;">
                <div style="font-size:40px;margin-bottom:16px;">⬡</div>
                <div style="font-size:18px;font-weight:600;color:#334155;margin-bottom:8px;">
                    No Interaction Selected
                </div>
                <div style="font-size:13px;color:#1e293b;">
                    Go to the <strong style="color:#00d4ff;">CALL INTELLIGENCE</strong> tab, 
                    click any row in the interaction log, then return here.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            call = SAMPLE_CALLS[st.session_state.selected_idx]
            call_id = call["call_id"]

            # Call summary strip
            st.markdown(f"""
            <div class="aria-card" style="margin-bottom:20px;">
                <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
                    <div>
                        <div class="section-label">Active Interaction</div>
                        <div style="font-size:16px;font-weight:700;color:#e2e8f0;margin-top:3px;">
                            {call['agent_name']}
                            <span class="mono" style="font-size:13px;margin-left:10px;">{call_id}</span>
                        </div>
                        <div style="font-size:12px;color:#475569;margin-top:4px;">
                            {call['sector']} &nbsp;·&nbsp; {call['queue']} &nbsp;·&nbsp; {duration_fmt(call['duration_seconds'])}
                        </div>
                    </div>
                    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
                        {csat_html(call['csat_score'])}
                        &nbsp;
                        {risk_html(call['risk_flag'])}
                        &nbsp;
                        {sentiment_html(call['sentiment'])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # AI config panel
            with st.expander("⚙️  AI Engine Configuration", expanded=False):
                st.markdown("""
                <div style="font-size:12px;color:#475569;font-family:'JetBrains Mono',monospace;line-height:1.8;">
                    <span style="color:#334155;">MODEL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                    <span style="color:#00d4ff;">gemini-2.5-flash</span><br>
                    <span style="color:#334155;">PROVIDER &nbsp;</span>
                    <span style="color:#94a3b8;">Google DeepMind — Gemini API</span><br>
                    <span style="color:#334155;">MODE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                    <span style="color:#94a3b8;">Streaming · Real-time token output</span><br>
                    <span style="color:#334155;">SCHEMA &nbsp;&nbsp;&nbsp;</span>
                    <span style="color:#94a3b8;">Structured QM Report (5-section)</span><br>
                    <span style="color:#334155;">PERSONA &nbsp;&nbsp;</span>
                    <span style="color:#94a3b8;">GCC Senior QM Analyst · 25yr experience</span><br>
                    <span style="color:#334155;">CONTEXT &nbsp;&nbsp;</span>
                    <span style="color:#94a3b8;">Call metadata + full transcript summary</span>
                </div>
                """, unsafe_allow_html=True)

            # Generate / display coaching
            already_done = call_id in st.session_state.coaching_results

            if not already_done:
                if st.button("⬡  INITIATE AI COACHING ANALYSIS", key="btn_coach"):
                    st.markdown('<div class="coaching-terminal">', unsafe_allow_html=True)
                    full_text = st.write_stream(stream_coaching(call))
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state.coaching_results[call_id] = full_text
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="coaching-terminal" style="display:flex;align-items:center;justify-content:center;color:#1e293b;">
                        Click the button above to generate the AI coaching report for this interaction.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Already streamed — display stored result
                st.markdown('<div class="coaching-terminal">', unsafe_allow_html=True)
                st.markdown(
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;'
                    f'line-height:1.75;color:#cbd5e1;white-space:pre-wrap;">'
                    f'{st.session_state.coaching_results[call_id]}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        label="⬇  DOWNLOAD COACHING REPORT",
                        data=json.dumps({
                            "generated_by": "ARIA AI Coaching Engine",
                            "generated_at": datetime.now().isoformat(),
                            "call": {k: v for k, v in call.items()},
                            "coaching_report": st.session_state.coaching_results[call_id],
                        }, indent=2),
                        file_name=f"coaching_{call_id}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        key="dl_single"
                    )
                with col_b:
                    if st.button("↺  RE-GENERATE COACHING", key="btn_regen"):
                        del st.session_state.coaching_results[call_id]
                        st.rerun()

    # ────────────── TAB 3 — REPORTS & EXPORT ───────────────────────────
    with tab3:
        analyzed_calls = [c for c in SAMPLE_CALLS if c["call_id"] in st.session_state.coaching_results]
        pending_calls  = [c for c in SAMPLE_CALLS if c["call_id"] not in st.session_state.coaching_results]

        r1, r2, r3 = st.columns(3)
        with r1: st.metric("AI Coached",  len(analyzed_calls), f"of {len(SAMPLE_CALLS)} total")
        with r2: st.metric("Pending",     len(pending_calls))
        with r3:
            comp_risk = sum(1 for c in analyzed_calls if c["risk_flag"] == "Compliance Risk")
            st.metric("Compliance Flags", comp_risk, "Reviewed" if comp_risk == 0 else "Action required", delta_color="inverse")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        if analyzed_calls:
            st.markdown('<div class="section-label" style="margin-bottom:10px;">Completed Coaching Reports</div>',
                        unsafe_allow_html=True)

            import pandas as pd
            rep_rows = []
            for c in analyzed_calls:
                rep_rows.append({
                    "Call ID":   c["call_id"],
                    "Agent":     c["agent_name"],
                    "Sector":    c["sector"],
                    "CSAT":      f"{c['csat_score']}/5",
                    "Risk":      c["risk_flag"],
                    "Outcome":   "Resolved" if c["resolved"] else "Open",
                    "Report Status": "✓ Complete",
                })
            st.dataframe(pd.DataFrame(rep_rows), use_container_width=True, hide_index=True)

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            # Build full export payload
            export_data = {
                "export_source":  "ARIA AI Quality Intelligence Platform",
                "platform_version": VERSION,
                "exported_at":    datetime.now().isoformat(),
                "total_interactions": len(SAMPLE_CALLS),
                "coached_interactions": len(analyzed_calls),
                "reports": [
                    {
                        "call_metadata": {k: v for k, v in c.items() if k != "transcript_summary"},
                        "transcript_summary": c["transcript_summary"],
                        "coaching_report": st.session_state.coaching_results[c["call_id"]],
                    }
                    for c in analyzed_calls
                ]
            }
            st.download_button(
                label=f"⬇  EXPORT ALL COACHING REPORTS  ({len(analyzed_calls)} interactions)",
                data=json.dumps(export_data, indent=2),
                file_name=f"ARIA_QM_Export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="dl_all"
            )
        else:
            st.markdown("""
            <div style="text-align:center;padding:50px 40px;color:#1e293b;">
                <div style="font-size:32px;margin-bottom:12px;">⬡</div>
                <div style="font-size:14px;">
                    No coaching reports generated yet.<br>
                    Select a call from <strong style="color:#00d4ff;">CALL INTELLIGENCE</strong>
                    and run the AI Coaching Engine.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── COMING SOON MODULE PAGE ───────────────────────────────────────────────
def render_coming_soon(mod: dict):
    progress = mod.get("progress", 50)
    milestones = mod.get("milestones", [])

    fill_color = "progress-fill-green" if progress >= 80 else \
                 "progress-fill-amber" if progress >= 50 else "progress-fill-blue"

    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:1px solid rgba(0,212,255,0.08);margin-bottom:24px;">
        <div style="font-size:10px;color:#334155;letter-spacing:0.12em;text-transform:uppercase;
                    font-weight:600;margin-bottom:6px;">
            ARIA Platform &nbsp;›&nbsp; {mod['name']}
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <h1 style="font-size:24px;font-weight:700;margin:0;color:#475569;">{mod['name']}</h1>
            <span class="badge-lock">COMING SOON</span>
        </div>
    </div>
    <div class="scan-bar"></div>
    """, unsafe_allow_html=True)

    # Hero card
    st.markdown(f"""
    <div style="text-align:center;padding:60px 40px 50px;
                background:linear-gradient(135deg,#070c18,#0a0f20);
                border:1px solid rgba(0,212,255,0.07);border-radius:20px;margin-bottom:24px;">
        <div style="font-size:52px;margin-bottom:16px;opacity:0.25;">{mod['icon']}</div>
        <div style="font-size:22px;font-weight:700;color:#334155;margin-bottom:8px;">
            {mod['name']}
        </div>
        <div style="font-size:13px;color:#1e293b;max-width:480px;margin:0 auto 28px;line-height:1.6;">
            This module is currently in active development and will be released in an upcoming
            ARIA platform update. Thank you for your patience.
        </div>
        <div style="max-width:360px;margin:0 auto;">
            <div style="display:flex;justify-content:space-between;
                        font-size:11px;color:#334155;font-weight:600;margin-bottom:8px;">
                <span>DEVELOPMENT PROGRESS</span>
                <span style="color:#00d4ff;">{progress}%</span>
            </div>
            <div class="progress-track">
                <div class="{fill_color}" style="width:{progress}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if milestones:
        st.markdown('<div class="section-label" style="margin-bottom:12px;">Development Milestones</div>',
                    unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (milestone, done) in enumerate(milestones):
            with cols[i % 2]:
                icon  = "✓" if done else "◌"
                color = "#10b981" if done else "#334155"
                bg    = "rgba(5,150,105,0.06)" if done else "rgba(51,65,85,0.08)"
                brd   = "rgba(5,150,105,0.15)" if done else "rgba(51,65,85,0.12)"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;
                            background:{bg};border:1px solid {brd};border-radius:10px;
                            margin-bottom:8px;">
                    <span style="color:{color};font-size:15px;font-weight:700;">{icon}</span>
                    <span style="font-size:13px;color:{'#94a3b8' if done else '#334155'};
                                 font-weight:{'500' if done else '400'};">{milestone}</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button(f"🔔  REQUEST EARLY ACCESS TO {mod['name'].upper()}", key=f"ea_{mod['key']}"):
        st.success(f"✓  Early access request submitted for **{mod['name']}**. We'll notify you at your registered email address when this module is available.")


# ── MAIN ROUTING ──────────────────────────────────────────────────────────
render_sidebar()

active = st.session_state.active_module
if active == "qm":
    render_qm_analyzer()
else:
    mod_data = next((m for m in MODULES if m["key"] == active), None)
    if mod_data:
        render_coming_soon(mod_data)