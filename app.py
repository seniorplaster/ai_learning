"""
ARIA — Agentic Review & Intelligence Analytics
CCaaS Contact Center AI Quality Management Platform
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
    page_title="ARIA | AI Quality Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
header    {visibility: hidden;}
.block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── APP BACKGROUND ── */
.stApp { background: #f8fafc; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1220 0%, #111827 100%) !important;
    border-right: 1px solid #1e3a5f !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* Native sidebar collapse/expand button */
[data-testid="collapsedControl"] {
    background: #0c1220 !important;
    border-right: 2px solid rgba(0,212,255,0.25) !important;
    color: #00d4ff !important;
}
[data-testid="collapsedControl"] span { color: #00d4ff !important; }
[data-testid="collapsedControl"] svg  { fill: #00d4ff !important; }

/* ── SIDEBAR EXPANDERS ── */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"]:hover {
    border-color: rgba(0,212,255,0.25) !important;
}
[data-testid="stSidebar"] details summary {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stSidebar"] details[open] summary {
    color: #38bdf8 !important;
}

/* ── SIDEBAR INNER BUTTONS ── */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(56,189,248,0.08) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    padding: 5px 12px !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(56,189,248,0.15) !important;
    border-color: rgba(56,189,248,0.4) !important;
    box-shadow: none !important;
    transform: none !important;
    color: #ffffff !important;
}

/* ── MAIN BUTTONS ── */
.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: 1px solid #1d4ed8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.05em !important;
    padding: 0.55rem 1.4rem !important;
    width: 100% !important;
    box-shadow: 0 1px 3px rgba(29,78,216,0.2), 0 1px 2px rgba(0,0,0,0.06) !important;
    transition: all 0.2s ease !important;
}
.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: #1e40af !important;
    border-color: #1e40af !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.3) !important;
    transform: translateY(-1px) !important;
}
.main .stButton > button:active,
[data-testid="stMainBlockContainer"] .stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 3px rgba(29,78,216,0.2) !important;
}

/* ── RESET / SECONDARY BUTTON — white outline ── */
button[data-testid="stBaseButton-secondary"] {
    background: #ffffff !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
button[data-testid="stBaseButton-secondary"]:hover {
    background: #f9fafb !important;
    border-color: #9ca3af !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    transform: translateY(-1px) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #065f46 !important;
    color: #ffffff !important;
    border: 1px solid #065f46 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 1px 3px rgba(6,95,70,0.2) !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: #047857 !important;
    box-shadow: 0 4px 12px rgba(6,95,70,0.25) !important;
    transform: translateY(-1px) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9 !important;
    border-radius: 10px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid #e2e8f0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 7px !important;
    padding: 9px 22px !important;
    font-weight: 500 !important;
    font-size: 12px !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    transition: color 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1d4ed8 !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.6rem !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #1d4ed8 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
/* Metric delta — dark enough to read on white */
[data-testid="stMetricDelta"] svg  { display: none !important; }
[data-testid="stMetricDelta"] > div {
    color: #374151 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stDataFrameResizable"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

/* ── ALERTS ── */
[data-baseweb="notification"] {
    background-color: #eff6ff !important;
    border: 1px solid #93c5fd !important;
    border-radius: 10px !important;
    color: #1e3a8a !important;
}

/* ── EXPANDER (main area) ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary {
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── DIVIDER ── */
hr { border-color: #e2e8f0 !important; margin: 1.2rem 0 !important; }

/* ── COMPONENT CLASSES ── */
/* Cards */
.aria-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.aria-card-green {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-amber {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-red {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.aria-card-blue {
    background: #eff6ff;
    border: 1px solid #93c5fd;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}

/* WCAG AA compliant badges — min 4.5:1 contrast ratio */
.badge-green  { display:inline-block; background:#d1fae5; color:#065f46; border:1px solid #34d399; border-radius:99px; padding:3px 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; }
.badge-blue   { display:inline-block; background:#dbeafe; color:#1e3a8a; border:1px solid #93c5fd; border-radius:99px; padding:3px 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; }
.badge-amber  { display:inline-block; background:#fef3c7; color:#78350f; border:1px solid #fcd34d; border-radius:99px; padding:3px 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; }
.badge-red    { display:inline-block; background:#fee2e2; color:#991b1b; border:1px solid #fca5a5; border-radius:99px; padding:3px 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; }
.badge-gray   { display:inline-block; background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; border-radius:99px; padding:3px 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; }
.badge-lock   { display:inline-block; background:#f3f4f6; color:#4b5563; border:1px solid #d1d5db; border-radius:99px; padding:2px 8px;  font-size:9px;  font-weight:700; letter-spacing:0.08em; }

/* Status dots */
.dot-green { display:inline-block; width:7px; height:7px; background:#16a34a; border-radius:50%; box-shadow:0 0 6px rgba(22,163,74,0.5); animation:pulse-g 2.2s infinite; }
.dot-blue  { display:inline-block; width:7px; height:7px; background:#0284c7; border-radius:50%; box-shadow:0 0 6px rgba(2,132,199,0.5); animation:pulse-b 2.2s infinite; }
.dot-amber { display:inline-block; width:7px; height:7px; background:#d97706; border-radius:50%; }
@keyframes pulse-g { 0%,100%{opacity:1;} 55%{opacity:0.4;} }
@keyframes pulse-b { 0%,100%{opacity:1;} 55%{opacity:0.4;} }

/* Text helpers */
.gradient-text {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}
.mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #6b7280; }
.section-label {
    font-size: 10px; font-weight: 700; color: #6b7280;
    text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 6px;
}
/* Detail card labels and values — high contrast */
.detail-label { font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; margin-bottom: 3px; }
.detail-value { font-size: 14px; color: #0f172a; font-weight: 600; margin-bottom: 14px; }
.detail-mono  { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #374151; margin-bottom: 14px; font-weight: 500; }

/* Scan bar */
.scan-bar {
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #1d4ed8 40%, #0ea5e9 60%, transparent 100%);
    animation: scan 4s ease-in-out infinite;
    border-radius: 1px;
    margin: 6px 0 20px;
}
@keyframes scan { 0%{opacity:0.15;} 50%{opacity:0.6;} 100%{opacity:0.15;} }

/* Coaching terminal — dark, intentional contrast (code-editor style) */
.coaching-terminal {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px 28px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    color: #e2e8f0;
    min-height: 100px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.04);
}
.coaching-terminal::before {
    content: "ARIA COACHING ENGINE  •  OUTPUT";
    display: block;
    font-size: 9px;
    color: #475569;
    letter-spacing: 0.16em;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e293b;
}

/* Progress track — light */
.progress-track {
    background: #e2e8f0;
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
    border: none;
}
.progress-fill-blue  { height:100%; background:linear-gradient(90deg,#1d4ed8,#0ea5e9); border-radius:99px; }
.progress-fill-green { height:100%; background:linear-gradient(90deg,#059669,#10b981); border-radius:99px; }
.progress-fill-amber { height:100%; background:linear-gradient(90deg,#d97706,#f59e0b); border-radius:99px; }

/* Coming soon hero */
.coming-soon-hero {
    text-align: center;
    padding: 70px 40px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* Selection summary card */
.selection-bar {
    background: #eff6ff;
    border: 1px solid #93c5fd;
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ────────────────────────────────────────────────────────────────────
PLATFORM   = "ARIA"
TAGLINE    = "Agentic Review & Intelligence Analytics"
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


# ── SAMPLE DATA ──────────────────────────────────────────────────────────────────
SAMPLE_CALLS = [
    {
        "call_id": "AR-2026-0091", "agent_id": "AGT-101", "agent_name": "Sara Al Mansoori",
        "sector": "Banking", "queue": "Premier Banking — Disputes",
        "duration_seconds": 187, "csat_score": 5, "resolved": True,
        "sentiment": "Positive", "risk_flag": "None",
        "transcript_summary": (
            "Customer called about an unauthorized transaction on their premium Visa card. "
            "Agent Sara verified identity using multi-factor authentication within 60 seconds, "
            "immediately initiated a chargeback process, explained the 5-7 business-day timeline "
            "clearly, and proactively offered a temporary credit limit increase as goodwill. "
            "Customer expressed high satisfaction and thanked the agent by name."
        ),
    },
    {
        "call_id": "AR-2026-0092", "agent_id": "AGT-205", "agent_name": "Mohammed Al Rashidi",
        "sector": "Telecom", "queue": "Technical Support — Mobile",
        "duration_seconds": 643, "csat_score": 2, "resolved": False,
        "sentiment": "Negative", "risk_flag": "Churn Risk",
        "transcript_summary": (
            "Customer reported mobile data not working for 3 consecutive days. Agent took 8 minutes "
            "to locate the account despite the customer providing the account number upfront. Asked "
            "customer to repeat details twice. Did not check the network outage map before "
            "troubleshooting. Failed to offer escalation, compensation, or a callback. Customer "
            "stated they would switch to a competitor at the end of the call."
        ),
    },
    {
        "call_id": "AR-2026-0093", "agent_id": "AGT-310", "agent_name": "Fatima Al Zahra",
        "sector": "Government", "queue": "Licensing Services",
        "duration_seconds": 245, "csat_score": 4, "resolved": True,
        "sentiment": "Neutral", "risk_flag": "None",
        "transcript_summary": (
            "Citizen called to inquire about trade license renewal requirements and applicable fees. "
            "Agent Fatima provided clear step-by-step guidance, confirmed eligibility criteria, and "
            "sent a digital checklist via SMS during the call. A brief delay occurred when accessing "
            "the updated fee schedule, but the correct information was confirmed and the citizen "
            "confirmed readiness to proceed."
        ),
    },
    {
        "call_id": "AR-2026-0094", "agent_id": "AGT-101", "agent_name": "Sara Al Mansoori",
        "sector": "Healthcare", "queue": "Patient Services — Cardiology",
        "duration_seconds": 312, "csat_score": 5, "resolved": True,
        "sentiment": "Positive", "risk_flag": "None",
        "transcript_summary": (
            "Patient called to schedule a cardiology follow-up and inquire about insurance "
            "pre-authorization for an MRI scan. Sara efficiently coordinated between two departments, "
            "secured a same-week appointment slot, and initiated the pre-authorization form with the "
            "insurance team. Patient expressed strong gratitude for the seamless, end-to-end experience."
        ),
    },
    {
        "call_id": "AR-2026-0095", "agent_id": "AGT-422", "agent_name": "Khalid Al Nuaimi",
        "sector": "Insurance", "queue": "Claims Processing — Motor",
        "duration_seconds": 521, "csat_score": 1, "resolved": False,
        "sentiment": "Negative", "risk_flag": "Compliance Risk",
        "transcript_summary": (
            "Customer called about a denied motor insurance claim filed 3 weeks ago. Agent Khalid "
            "could not locate the claim in the CRM for 11 minutes. Transferred the customer twice "
            "without warning or context handover. When found, provided incorrect information about "
            "the appeals process and the regulatory timeline. Customer stated they would file a "
            "formal complaint with the UAE Insurance Authority (CBUAE)."
        ),
    },
    {
        "call_id": "AR-2026-0096", "agent_id": "AGT-205", "agent_name": "Mohammed Al Rashidi",
        "sector": "Banking", "queue": "Retail Banking — Loans",
        "duration_seconds": 198, "csat_score": 3, "resolved": True,
        "sentiment": "Neutral", "risk_flag": "None",
        "transcript_summary": (
            "Customer inquired about personal loan eligibility and current interest rates. Agent "
            "Mohammed provided the standard rate bands but could not run a live pre-qualification "
            "check because the credit-check tool was temporarily unavailable. Offered a callback "
            "from the loans team within 24 hours. Customer accepted but expressed mild frustration "
            "about not receiving an immediate eligibility answer."
        ),
    },
    {
        "call_id": "AR-2026-0097", "agent_id": "AGT-310", "agent_name": "Fatima Al Zahra",
        "sector": "Telecom", "queue": "Enterprise Sales — Upgrades",
        "duration_seconds": 289, "csat_score": 4, "resolved": True,
        "sentiment": "Positive", "risk_flag": "None",
        "transcript_summary": (
            "Enterprise customer called to upgrade their corporate data plan from 100 GB to 500 GB "
            "and add 3 SIM cards for new employees. Fatima processed the upgrade, applied the "
            "corporate bundle discount automatically, confirmed the activation timeline as next "
            "billing cycle, and emailed the updated contract. Customer appreciated the efficient handling."
        ),
    },
    {
        "call_id": "AR-2026-0098", "agent_id": "AGT-422", "agent_name": "Khalid Al Nuaimi",
        "sector": "Government", "queue": "Complaints & Escalation",
        "duration_seconds": 614, "csat_score": 2, "resolved": False,
        "sentiment": "Negative", "risk_flag": "Compliance Risk",
        "transcript_summary": (
            "Resident called to escalate a permit approval that was 18 days beyond the legally "
            "mandated 30-day processing window. Agent Khalid was unaware of the statutory SLA "
            "requirement. Did not log the complaint in the government CRM during the call. Provided "
            "vague reassurances with no escalation path, no reference number, and no supervisor "
            "involvement. Resident stated they would contact the relevant oversight body."
        ),
    },
    {
        "call_id": "AR-2026-0099", "agent_id": "AGT-101", "agent_name": "Sara Al Mansoori",
        "sector": "Healthcare", "queue": "Insurance & Billing — Disputes",
        "duration_seconds": 156, "csat_score": 5, "resolved": True,
        "sentiment": "Positive", "risk_flag": "None",
        "transcript_summary": (
            "Patient called to dispute an erroneous consultation fee on their last hospital invoice. "
            "Sara identified the billing discrepancy immediately by cross-referencing clinical notes "
            "and the billing system. Initiated a credit note on the spot, confirmed refund within "
            "3-5 working days, and apologised on behalf of the hospital. Patient was fully satisfied."
        ),
    },
]


# ── AI COACHING CONFIG ───────────────────────────────────────────────────────────
COACHING_SYSTEM_PROMPT = """You are ARIA's AI Coaching Engine — a senior contact center quality expert with 25 years of experience across banking, telecom, healthcare, government, and insurance in the GCC region.

Your coaching reports are structured, specific, and actionable. Every recommendation must reference actual events in the call summary.

Format every coaching report with these exact sections:

**PERFORMANCE SUMMARY**
A 2-3 sentence overall assessment of this specific interaction.

**STRENGTHS IDENTIFIED**
2-3 bullet points of what the agent did well, referencing specific actions. If no genuine strengths, state that honestly.

**CRITICAL IMPROVEMENT AREAS**
3-4 numbered coaching points. Each must reference a specific moment in the call and explain the impact on the customer.

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
    m = call["duration_seconds"] // 60
    s = call["duration_seconds"] % 60
    outcome = "RESOLVED" if call["resolved"] else "UNRESOLVED"
    return f"""Generate a full coaching report for this contact center interaction.

CALL ID:  {call['call_id']}
AGENT:    {call['agent_name']} ({call['agent_id']})
SECTOR:   {call['sector']}
QUEUE:    {call['queue']}
DURATION: {m}m {s}s  |  CSAT: {call['csat_score']}/5  |  OUTCOME: {outcome}
SENTIMENT: {call['sentiment']}  |  RISK: {call['risk_flag']}

TRANSCRIPT SUMMARY:
{call['transcript_summary']}

Provide the full coaching report. Be specific to this exact call."""


# ── PDF GENERATOR ────────────────────────────────────────────────────────────────
def sanitize_for_pdf(text: str) -> str:
    """Strip emoji and non-latin-1 chars so FPDF core fonts can render them."""
    replacements = {
        "🟢": "[LOW PRIORITY]", "🟡": "[MEDIUM PRIORITY]",
        "🔴": "[HIGH PRIORITY]", "🚨": "[URGENT-COMPLIANCE]",
        "★": "*", "☆": "-", "◉": ">", "◈": ">", "⬡": "-",
        "→": "->", "←": "<-", "✓": "OK", "✗": "X",
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u00b7": "-",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)   # strip **bold**
    result = ""
    for ch in text:
        try:
            ch.encode("latin-1")
            result += ch
        except UnicodeEncodeError:
            result += "?"
    return result


def generate_pdf_report(calls_with_coaching: list) -> bytes:
    class ARIAReport(FPDF):
        def header(self):
            self.set_fill_color(29, 78, 216)
            self.rect(0, 0, 210, 11, "F")
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(255, 255, 255)
            self.set_xy(10, 2)
            self.cell(0, 7, "DEMO  |  AI Quality Coaching Report", ln=False)
            self.set_text_color(0, 0, 0)
            self.ln(13)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(107, 114, 128)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M") + " UTC+4"
            self.cell(0, 10, f"Generated: {timestamp}   |   DEMO — Confidential   |   Page {self.page_no()}", align="C")

    pdf = ARIAReport()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 18, 15)

    # ── Cover page ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(15, 23, 42)
    pdf.ln(12)
    pdf.cell(0, 12, "AI Quality Coaching Report", ln=True, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 8, datetime.now().strftime("%Y-%m-%d  %H:%M UTC+4"), ln=True, align="C")
    pdf.cell(0, 8, f"Total Interactions Analyzed: {len(calls_with_coaching)}", ln=True, align="C")

    if calls_with_coaching:
        pdf.ln(8)
        resolved = sum(1 for x in calls_with_coaching if x["call"]["resolved"])
        avg_csat = round(sum(x["call"]["csat_score"] for x in calls_with_coaching) / len(calls_with_coaching), 1)
        flagged  = sum(1 for x in calls_with_coaching if x["call"]["risk_flag"] != "None")

        pdf.set_fill_color(239, 246, 255)
        pdf.set_draw_color(147, 197, 253)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(30, 58, 138)
        pdf.set_x(30)
        pdf.cell(150, 9, f"Avg CSAT: {avg_csat}/5     Resolution Rate: {resolved}/{len(calls_with_coaching)}     Risk Flagged: {flagged}", border=1, fill=True, align="C", ln=True)

    pdf.ln(10)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 6, "This report was generated by the AI Coaching Engine. Content is based on the provided transcript summaries.", align="C", ln=True)
    pdf.cell(0, 6, "For questions contact your QM supervisor. Treat all agent performance data as confidential.", align="C", ln=True)

    # ── Individual call pages ────────────────────────────────────────────────
    for item in calls_with_coaching:
        call    = item["call"]
        coaching = sanitize_for_pdf(item["coaching"])
        pdf.add_page()

        # Call header box
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        y0 = pdf.get_y()
        pdf.rect(15, y0, 180, 38, "FD")

        pdf.set_xy(19, y0 + 4)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 7, sanitize_for_pdf(f"{call['call_id']}   |   {call['agent_name']} ({call['agent_id']})"), ln=True)

        pdf.set_x(19)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(55, 65, 81)
        dur = f"{call['duration_seconds']//60}m {call['duration_seconds']%60}s"
        pdf.cell(0, 6, sanitize_for_pdf(f"Sector: {call['sector']}    Queue: {call['queue']}    Duration: {dur}"), ln=True)

        pdf.set_x(19)
        outcome = "Resolved" if call["resolved"] else "Unresolved"
        pdf.cell(0, 6, sanitize_for_pdf(
            f"CSAT: {call['csat_score']}/5    Outcome: {outcome}    "
            f"Sentiment: {call['sentiment']}    Risk: {call['risk_flag']}"
        ), ln=True)

        pdf.set_xy(15, y0 + 40)
        pdf.ln(5)

        # Coaching content
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(29, 78, 216)
        pdf.cell(0, 7, "AI Coaching Analysis", ln=True)

        pdf.set_draw_color(29, 78, 216)
        pdf.set_line_width(0.5)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.ln(4)

        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(31, 41, 55)
        pdf.multi_cell(180, 5.5, coaching.strip())

    return bytes(pdf.output())


# ── API SETUP ────────────────────────────────────────────────────────────────────
load_dotenv()
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


# ── SESSION STATE ────────────────────────────────────────────────────────────────
defaults = {
    "active_module":    "qm",
    "selected_indices": [],          # list of row indices currently selected in the df
    "coach_queue":      [],          # list of call dicts queued for coaching
    "coach_triggered":  False,       # True → show coaching section in Tab 1
    "coaching_results": {},          # {call_id: coaching_text}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────────────
def csat_badge(score: int) -> str:
    if score >= 4:   return f'<span class="badge-green">★ {score} / 5</span>'
    elif score == 3: return f'<span class="badge-amber">★ {score} / 5</span>'
    else:            return f'<span class="badge-red">★ {score} / 5</span>'

def risk_badge(flag: str) -> str:
    if flag == "None":          return '<span class="badge-gray">✓ None</span>'
    elif flag == "Churn Risk":  return '<span class="badge-amber">⚠ Churn Risk</span>'
    else:                       return '<span class="badge-red">🚨 Compliance Risk</span>'

def sentiment_badge(s: str) -> str:
    if s == "Positive": return '<span class="badge-green">↑ Positive</span>'
    elif s == "Neutral":return '<span class="badge-gray">→ Neutral</span>'
    else:               return '<span class="badge-red">↓ Negative</span>'

def resolved_badge(r: bool) -> str:
    return '<span class="badge-green">✓ Resolved</span>' if r else '<span class="badge-red">✗ Open</span>'

def dur_fmt(sec: int) -> str:
    return f"{sec//60}m {sec%60}s"

def stream_coaching(call: dict):
    if not client:
        yield "⚠️  No API key configured. Add GEMINI_API_KEY to .streamlit/secrets.toml"
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
        yield f"\n\n⚠️  Error: {e}"


# ── SIDEBAR ──────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown(f"""
        <div style="padding:22px 16px 18px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:10px;">
            <div style="font-size:21px;font-weight:700;letter-spacing:0.14em;
                        background:linear-gradient(135deg,#38bdf8,#2563eb);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                ⬡ {PLATFORM}
            </div>
            <div style="font-size:9.5px;color:#475569;letter-spacing:0.14em;
                        text-transform:uppercase;margin-top:5px;line-height:1.5;">
                {TAGLINE}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.14em;padding:0 4px 8px;">Platform Modules</div>',
                    unsafe_allow_html=True)

        # Expandable module tree
        for mod in MODULES:
            is_active = st.session_state.active_module == mod["key"]

            if mod["available"]:
                with st.expander(f"{mod['icon']}  {mod['name']}", expanded=is_active):
                    sub = [("◈", "Call Intelligence", "Multi-select & analysis"),
                           ("⬡", "AI Coaching Engine", "Stream coaching reports"),
                           ("⬇", "Reports & Export",   "Download JSON / PDF")]
                    for icon, name, desc in sub:
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:9px;padding:6px 8px;
                                    border-radius:6px;background:rgba(56,189,248,0.06);
                                    border:1px solid rgba(56,189,248,0.12);margin-bottom:4px;">
                            <span style="color:#38bdf8;font-size:12px;">{icon}</span>
                            <div>
                                <div style="font-size:11px;color:#94a3b8;font-weight:500;">{name}</div>
                                <div style="font-size:9.5px;color:#334155;">{desc}</div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    if not is_active:
                        if st.button("Open Module", key=f"open_{mod['key']}"):
                            st.session_state.active_module = mod["key"]
                            st.rerun()

            else:
                progress   = mod.get("progress", 0)
                milestones = mod.get("milestones", [])
                done_count = sum(1 for _, d in milestones if d)
                fill_col   = "#16a34a" if progress >= 80 else "#d97706" if progress >= 50 else "#2563eb"

                with st.expander(f"{mod['icon']}  {mod['name']}", expanded=False):
                    st.markdown(f"""
                    <div style="padding:4px 0 10px;">
                        <div style="display:flex;justify-content:space-between;
                                    font-size:10px;color:#475569;font-weight:600;
                                    text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">
                            <span>Progress</span><span style="color:{fill_col};">{progress}%</span>
                        </div>
                        <div style="background:#1e293b;border-radius:99px;height:4px;overflow:hidden;">
                            <div style="width:{progress}%;height:100%;background:{fill_col};border-radius:99px;"></div>
                        </div>
                        <div style="font-size:10px;color:#334155;margin-top:6px;">
                            {done_count}/{len(milestones)} milestones complete
                        </div>
                    </div>""", unsafe_allow_html=True)
                    for ms_name, done in milestones:
                        c = "#10b981" if done else "#334155"
                        i = "✓" if done else "○"
                        st.markdown(f'<div style="font-size:11px;color:{c};padding:2px 0;">{i}&nbsp;&nbsp;{ms_name}</div>',
                                    unsafe_allow_html=True)
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                    if st.button("View Preview", key=f"nav_{mod['key']}"):
                        st.session_state.active_module = mod["key"]
                        st.rerun()

        # System status
        st.markdown("""
        <div style="padding:16px 4px 10px;margin-top:14px;border-top:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;">System Status</div>
            <div style="font-size:12px;color:#64748b;line-height:2.4;">
                <span class="dot-green"></span>&nbsp;&nbsp;AI Engine&nbsp;
                <span style="float:right;color:#16a34a;font-weight:700;font-size:11px;">ONLINE</span><br>
                <span class="dot-green"></span>&nbsp;&nbsp;Data Pipeline&nbsp;
                <span style="float:right;color:#16a34a;font-weight:700;font-size:11px;">ONLINE</span><br>
                <span class="dot-blue"></span>&nbsp;&nbsp;API Gateway&nbsp;
                <span style="float:right;color:#0284c7;font-weight:700;font-size:11px;">ACTIVE</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Collapse hint + footer
        st.markdown(f"""
        <div style="padding:12px 4px 18px;border-top:1px solid rgba(255,255,255,0.05);margin-top:6px;">
            <div style="font-size:10px;color:#334155;margin-bottom:6px;">
                ← Use the arrow button at the sidebar edge to collapse this panel.
            </div>
            <div class="mono" style="font-size:10px;">{VERSION} &nbsp;|&nbsp; Build {BUILD_DATE}</div>
            <div style="font-size:9px;color:#1e293b;margin-top:3px;">© 2026 DEMO</div>
        </div>""", unsafe_allow_html=True)


# ── QM ANALYZER ──────────────────────────────────────────────────────────────────
def render_qm_analyzer():
    import pandas as pd

    # ── Page header ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:1px solid #e2e8f0;margin-bottom:8px;">
        <div style="font-size:10px;color:#9ca3af;letter-spacing:0.12em;text-transform:uppercase;font-weight:600;margin-bottom:6px;">
            ARIA Platform &nbsp;›&nbsp; QM Analyzer
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <div>
                <h1 style="font-size:24px;font-weight:700;margin:0;
                            background:linear-gradient(135deg,#1d4ed8,#0ea5e9);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                    Call Quality Intelligence Engine
                </h1>
                <div style="font-size:13px;color:#6b7280;margin-top:4px;">
                    AI-powered evaluation, coaching, and risk detection across all interactions
                </div>
            </div>
            <div style="text-align:right;flex-shrink:0;margin-left:20px;">
                <span class="badge-green">◉ LIVE SESSION</span>
                <div class="mono" style="margin-top:6px;font-size:10px;color:#9ca3af;">
                    {datetime.now().strftime('%Y-%m-%d  %H:%M UTC+4')}
                </div>
            </div>
        </div>
    </div>
    <div class="scan-bar"></div>
    """, unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["◈  CALL INTELLIGENCE", "⬡  COACHING RESULTS", "⬇  REPORTS & EXPORT"])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — CALL INTELLIGENCE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab1:

        # ── 1a. Build dataframe ───────────────────────────────────────────
        rows = []
        for c in SAMPLE_CALLS:
            coached = "✓" if c["call_id"] in st.session_state.coaching_results else "—"
            rows.append({
                "Call ID":    c["call_id"],
                "Agent":      c["agent_name"],
                "Sector":     c["sector"],
                "Queue":      c["queue"],
                "Duration":   dur_fmt(c["duration_seconds"]),
                "CSAT":       c["csat_score"],
                "Resolved":   "Yes" if c["resolved"] else "No",
                "Sentiment":  c["sentiment"],
                "Risk Flag":  c["risk_flag"],
                "Coached":    coached,
            })
        df = pd.DataFrame(rows)

        st.markdown('<div class="section-label" style="margin-bottom:8px;">Interaction Log — Select one or more rows to begin analysis</div>', unsafe_allow_html=True)

        event = st.dataframe(
            df,
            on_select="rerun",
            selection_mode="multi-row",
            use_container_width=True,
            hide_index=True,
            key="calls_table",
            column_config={
                "CSAT":    st.column_config.NumberColumn("CSAT ★", format="%d / 5"),
                "Call ID": st.column_config.TextColumn("Call ID", width="small"),
                "Queue":   st.column_config.TextColumn("Queue", width="large"),
                "Coached": st.column_config.TextColumn("AI Coached", width="small"),
            },
        )

        # ── 1b. Read selection ────────────────────────────────────────────
        sel_rows = list(event.selection.rows) if event.selection and event.selection.rows else []
        # Persist last selection so it survives reruns triggered by coaching button
        if sel_rows:
            st.session_state.selected_indices = sel_rows
        current_sel = st.session_state.selected_indices
        sel_calls   = [SAMPLE_CALLS[i] for i in current_sel]

        # ── 1c. Dynamic metrics ───────────────────────────────────────────
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        display_calls = sel_calls if sel_calls else SAMPLE_CALLS
        n     = len(display_calls)
        res   = sum(1 for c in display_calls if c["resolved"])
        acsat = round(sum(c["csat_score"] for c in display_calls) / n, 1)
        flag  = sum(1 for c in display_calls if c["risk_flag"] != "None")
        ags   = len(set(c["agent_id"] for c in display_calls))
        done  = sum(1 for c in display_calls if c["call_id"] in st.session_state.coaching_results)
        m_label = f"Selected Calls  ({n})" if sel_calls else "Total Interactions"

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: st.metric(m_label, n)
        with c2: st.metric("Avg CSAT", f"{acsat}/5")
        with c3: st.metric("Resolution Rate", f"{res/n*100:.0f}%", f"{res}/{n}")
        with c4: st.metric("Risk Flagged", flag, delta="Needs review" if flag else "None", delta_color="inverse")
        with c5: st.metric("Agents", ags)
        with c6: st.metric("AI Coached", done, f"of {n} selected" if sel_calls else f"of {n} total")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── 1d. Selection panel ───────────────────────────────────────────
        if not current_sel:
            st.info("💡 Click any row (or hold **Shift/Ctrl** to select multiple) to load the interaction profile and generate AI coaching.")

        elif len(current_sel) == 1:
            # ── Single call selected ──────────────────────────────────────
            call = sel_calls[0]
            card_class = ("aria-card-green" if call["csat_score"] >= 4 else
                          "aria-card-amber" if call["csat_score"] == 3 else "aria-card-red")
            st.markdown(f"""
            <div class="{card_class}">
                <div class="section-label" style="margin-bottom:14px;">Selected Interaction Profile</div>
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
                        <div class="detail-value">{dur_fmt(call['duration_seconds'])}</div>
                        <div class="detail-label">CSAT Score</div>
                        <div style="margin-bottom:14px;">{csat_badge(call['csat_score'])}</div>
                        <div class="detail-label">Outcome</div>
                        <div style="margin-bottom:14px;">{resolved_badge(call['resolved'])}</div>
                    </div>
                    <div>
                        <div class="detail-label">Sentiment</div>
                        <div style="margin-bottom:14px;">{sentiment_badge(call['sentiment'])}</div>
                        <div class="detail-label">Risk Flag</div>
                        <div style="margin-bottom:14px;">{risk_badge(call['risk_flag'])}</div>
                        <div class="detail-label">AI Coached</div>
                        <div>{'<span class="badge-green">✓ Done</span>' if call["call_id"] in st.session_state.coaching_results else '<span class="badge-gray">Pending</span>'}</div>
                    </div>
                </div>
                <div class="detail-label">Transcript Summary</div>
                <div style="font-size:13px;color:#374151;line-height:1.7;
                            background:rgba(0,0,0,0.04);border-radius:8px;padding:12px 16px;
                            border:1px solid rgba(0,0,0,0.06);">
                    {call['transcript_summary']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Coaching trigger button
            if not st.session_state.coach_triggered:
                if st.button(f"⬡  INITIATE AI COACHING FOR  {call['call_id']}", key="btn_coach_single"):
                    st.session_state.coach_queue = sel_calls
                    st.session_state.coach_triggered = True

        else:
            # ── Multiple calls selected ───────────────────────────────────
            agents_sel  = list(set(c["agent_name"] for c in sel_calls))
            sectors_sel = list(set(c["sector"] for c in sel_calls))
            already_done = [c for c in sel_calls if c["call_id"] in st.session_state.coaching_results]
            needs_coaching = [c for c in sel_calls if c["call_id"] not in st.session_state.coaching_results]

            st.markdown(f"""
            <div class="aria-card-blue">
                <div class="section-label" style="margin-bottom:12px;">Batch Selection — {len(current_sel)} Interactions</div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:14px;">
                    <div>
                        <div class="detail-label">Selected Calls</div>
                        <div style="font-size:22px;font-weight:700;color:#1d4ed8;font-family:'JetBrains Mono',monospace;">{len(current_sel)}</div>
                    </div>
                    <div>
                        <div class="detail-label">Avg CSAT</div>
                        <div style="font-size:22px;font-weight:700;color:#1d4ed8;font-family:'JetBrains Mono',monospace;">{round(sum(c['csat_score'] for c in sel_calls)/len(sel_calls),1)}</div>
                    </div>
                    <div>
                        <div class="detail-label">Already Coached</div>
                        <div style="font-size:22px;font-weight:700;color:#065f46;font-family:'JetBrains Mono',monospace;">{len(already_done)}</div>
                    </div>
                    <div>
                        <div class="detail-label">Pending</div>
                        <div style="font-size:22px;font-weight:700;color:#78350f;font-family:'JetBrains Mono',monospace;">{len(needs_coaching)}</div>
                    </div>
                </div>
                <div style="font-size:12px;color:#374151;">
                    <b>Agents:</b> {', '.join(agents_sel)} &nbsp;·&nbsp;
                    <b>Sectors:</b> {', '.join(sectors_sel)} &nbsp;·&nbsp;
                    <b>Calls:</b> {', '.join(c['call_id'] for c in sel_calls)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.coach_triggered:
                if st.button(f"⬡  START BATCH AI COACHING — {len(current_sel)} INTERACTIONS", key="btn_coach_batch"):
                    st.session_state.coach_queue = sel_calls
                    st.session_state.coach_triggered = True

        # ── 1e. Coaching output section ───────────────────────────────────
        if st.session_state.coach_triggered and st.session_state.coach_queue:
            st.divider()
            n_q = len(st.session_state.coach_queue)
            st.markdown(f"""
            <div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:4px;">
                ⬡ AI Coaching Analysis
                <span style="font-size:12px;font-weight:400;color:#6b7280;margin-left:10px;">
                    {n_q} interaction{'s' if n_q > 1 else ''} queued
                </span>
            </div>
            <div style="font-size:13px;color:#6b7280;margin-bottom:18px;">
                Streaming coaching reports from Gemini — results are saved automatically.
            </div>
            """, unsafe_allow_html=True)

            for idx, call in enumerate(st.session_state.coach_queue):
                call_id = call["call_id"]
                label   = f"◈  {call['agent_name']}  ·  {call_id}  ·  {call['sector']}  ·  CSAT {call['csat_score']}/5"

                with st.expander(label, expanded=True):
                    if call_id in st.session_state.coaching_results:
                        st.markdown('<div class="coaching-terminal">', unsafe_allow_html=True)
                        st.markdown(
                            f'<div style="white-space:pre-wrap;font-family:\'JetBrains Mono\',monospace;'
                            f'font-size:13px;line-height:1.8;color:#e2e8f0;">'
                            f'{st.session_state.coaching_results[call_id]}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="coaching-terminal">', unsafe_allow_html=True)
                        full_text = st.write_stream(stream_coaching(call))
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.session_state.coaching_results[call_id] = full_text
                        st.rerun()

            # Reset + navigation prompt after all done
            all_done = all(c["call_id"] in st.session_state.coaching_results
                           for c in st.session_state.coach_queue)
            if all_done:
                st.success(f"✓  {n_q} coaching report{'s' if n_q > 1 else ''} complete. Switch to **COACHING RESULTS** or **REPORTS & EXPORT** to download.")
                if st.button("↺  Clear & Select New Calls", key="btn_reset"):
                    st.session_state.coach_triggered  = False
                    st.session_state.coach_queue      = []
                    st.session_state.selected_indices = []
                    st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — COACHING RESULTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab2:
        done_calls = [c for c in SAMPLE_CALLS if c["call_id"] in st.session_state.coaching_results]

        if not done_calls:
            st.markdown("""
            <div style="text-align:center;padding:60px 40px;">
                <div style="font-size:40px;margin-bottom:16px;color:#cbd5e1;">⬡</div>
                <div style="font-size:18px;font-weight:600;color:#374151;margin-bottom:8px;">No Coaching Reports Yet</div>
                <div style="font-size:13px;color:#9ca3af;">
                    Go to <strong style="color:#1d4ed8;">CALL INTELLIGENCE</strong>, select one or more interactions,
                    then click the coaching button to generate reports.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            t2c1, t2c2, t2c3 = st.columns(3)
            with t2c1: st.metric("Coaching Reports", len(done_calls))
            with t2c2:
                avg = round(sum(c["csat_score"] for c in done_calls) / len(done_calls), 1)
                st.metric("Avg CSAT (coached)", f"{avg}/5")
            with t2c3:
                comp = sum(1 for c in done_calls if c["risk_flag"] == "Compliance Risk")
                st.metric("Compliance Flags", comp, delta_color="inverse")

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            for call in done_calls:
                call_id  = call["call_id"]
                coaching = st.session_state.coaching_results[call_id]
                card = ("aria-card-green" if call["csat_score"] >= 4 else
                        "aria-card-amber" if call["csat_score"] == 3 else "aria-card-red")
                with st.expander(
                    f"◈  {call['agent_name']}  ·  {call_id}  ·  {call['sector']}  ·  CSAT {call['csat_score']}/5",
                    expanded=False
                ):
                    st.markdown(f"""
                    <div class="{card}" style="margin-bottom:14px;">
                        <div style="display:flex;gap:20px;flex-wrap:wrap;">
                            <div><div class="detail-label">Agent</div><div class="detail-value">{call['agent_name']}</div></div>
                            <div><div class="detail-label">Queue</div><div class="detail-value" style="font-size:12px;">{call['queue']}</div></div>
                            <div><div class="detail-label">Duration</div><div class="detail-value">{dur_fmt(call['duration_seconds'])}</div></div>
                            <div><div class="detail-label">CSAT</div><div style="padding-top:3px;">{csat_badge(call['csat_score'])}</div></div>
                            <div><div class="detail-label">Risk</div><div style="padding-top:3px;">{risk_badge(call['risk_flag'])}</div></div>
                            <div><div class="detail-label">Outcome</div><div style="padding-top:3px;">{resolved_badge(call['resolved'])}</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="coaching-terminal">', unsafe_allow_html=True)
                    st.markdown(
                        f'<div style="white-space:pre-wrap;font-size:13px;line-height:1.8;color:#e2e8f0;">'
                        f'{coaching}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                    dl_col, re_col = st.columns(2)
                    with dl_col:
                        payload = json.dumps({
                            "generated_by": "ARIA AI Coaching Engine",
                            "generated_at": datetime.now().isoformat(),
                            "call": {k: v for k, v in call.items()},
                            "coaching_report": coaching,
                        }, indent=2)
                        st.download_button(
                            label="⬇  Download JSON",
                            data=payload,
                            file_name=f"coaching_{call_id}.json",
                            mime="application/json",
                            key=f"dl_single_{call_id}"
                        )
                    with re_col:
                        if st.button("↺  Re-generate", key=f"regen_{call_id}"):
                            del st.session_state.coaching_results[call_id]
                            st.rerun()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — REPORTS & EXPORT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab3:
        analyzed = [c for c in SAMPLE_CALLS if c["call_id"] in st.session_state.coaching_results]
        pending  = [c for c in SAMPLE_CALLS if c["call_id"] not in st.session_state.coaching_results]

        t3c1, t3c2, t3c3 = st.columns(3)
        with t3c1: st.metric("AI Coached", len(analyzed), f"of {len(SAMPLE_CALLS)}")
        with t3c2: st.metric("Pending", len(pending))
        with t3c3:
            comp = sum(1 for c in analyzed if c["risk_flag"] == "Compliance Risk")
            st.metric("Compliance Flags", comp, delta_color="inverse")

        if not analyzed:
            st.markdown("""
            <div style="text-align:center;padding:50px 30px;color:#9ca3af;">
                <div style="font-size:32px;margin-bottom:12px;">⬡</div>
                <div>No coaching reports yet. Return to <strong style="color:#1d4ed8;">Call Intelligence</strong>
                to select and analyze interactions.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-bottom:8px;">Completed Reports</div>', unsafe_allow_html=True)

            rep_rows = [{"Call ID": c["call_id"], "Agent": c["agent_name"], "Sector": c["sector"],
                          "CSAT": f"{c['csat_score']}/5", "Risk": c["risk_flag"],
                          "Outcome": "Resolved" if c["resolved"] else "Open", "Status": "✓ Complete"}
                         for c in analyzed]
            st.dataframe(pd.DataFrame(rep_rows), use_container_width=True, hide_index=True)

            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-bottom:10px;">Bulk Download</div>', unsafe_allow_html=True)

            json_payload = json.dumps({
                "export_source": "ARIA AI Quality Intelligence Platform",
                "platform_version": VERSION,
                "exported_at": datetime.now().isoformat(),
                "total_interactions": len(SAMPLE_CALLS),
                "coached_interactions": len(analyzed),
                "reports": [{"call_metadata": {k: v for k, v in c.items() if k != "transcript_summary"},
                              "transcript_summary": c["transcript_summary"],
                              "coaching_report": st.session_state.coaching_results[c["call_id"]]}
                             for c in analyzed]
            }, indent=2)

            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(
                    label=f"⬇  Download All — JSON  ({len(analyzed)} reports)",
                    data=json_payload,
                    file_name=f"ARIA_QM_Export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    key="dl_all_json"
                )

            with dl2:
                if FPDF_AVAILABLE:
                    items = [{"call": c, "coaching": st.session_state.coaching_results[c["call_id"]]}
                             for c in analyzed]
                    try:
                        pdf_bytes = generate_pdf_report(items)
                        st.download_button(
                            label=f"⬇  Download All — PDF  ({len(analyzed)} reports)",
                            data=pdf_bytes,
                            file_name=f"ARIA_QM_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            key="dl_all_pdf"
                        )
                    except Exception as e:
                        st.error(f"PDF generation error: {e}")
                else:
                    st.info("Add `fpdf2` to requirements.txt to enable PDF export.")


# ── COMING SOON MODULE PAGE ───────────────────────────────────────────────────────
def render_coming_soon(mod: dict):
    progress   = mod.get("progress", 50)
    milestones = mod.get("milestones", [])

    fill_cls = ("progress-fill-green" if progress >= 80 else
                "progress-fill-amber" if progress >= 50 else "progress-fill-blue")

    st.markdown(f"""
    <div style="padding-bottom:14px;border-bottom:1px solid #e2e8f0;margin-bottom:24px;">
        <div style="font-size:10px;color:#9ca3af;letter-spacing:0.12em;text-transform:uppercase;font-weight:600;margin-bottom:6px;">
            ARIA Platform &nbsp;›&nbsp; {mod['name']}
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <h1 style="font-size:24px;font-weight:700;margin:0;color:#374151;">{mod['name']}</h1>
            <span class="badge-lock">COMING SOON</span>
        </div>
    </div>
    <div class="scan-bar"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="coming-soon-hero">
        <div style="font-size:52px;margin-bottom:16px;opacity:0.2;color:#374151;">{mod['icon']}</div>
        <div style="font-size:22px;font-weight:700;color:#374151;margin-bottom:8px;">{mod['name']}</div>
        <div style="font-size:13px;color:#9ca3af;max-width:480px;margin:0 auto 28px;line-height:1.6;">
            This module is currently in active development and will be released in an upcoming
            ARIA platform update. Thank you for your patience.
        </div>
        <div style="max-width:360px;margin:0 auto;">
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        color:#6b7280;font-weight:600;margin-bottom:8px;">
                <span>DEVELOPMENT PROGRESS</span>
                <span style="color:#1d4ed8;">{progress}%</span>
            </div>
            <div class="progress-track">
                <div class="{fill_cls}" style="width:{progress}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if milestones:
        st.markdown('<div class="section-label" style="margin-bottom:12px;">Development Milestones</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (ms, done) in enumerate(milestones):
            with cols[i % 2]:
                icon   = "✓" if done else "○"
                color  = "#065f46" if done else "#9ca3af"
                bg     = "#f0fdf4" if done else "#f9fafb"
                border = "#86efac" if done else "#e5e7eb"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:11px 14px;
                            background:{bg};border:1px solid {border};border-radius:10px;margin-bottom:8px;">
                    <span style="color:{color};font-size:14px;font-weight:700;">{icon}</span>
                    <span style="font-size:13px;color:{'#374151' if done else '#9ca3af'};
                                 font-weight:{'500' if done else '400'};">{ms}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button(f"🔔  Request Early Access to {mod['name']}", key=f"ea_{mod['key']}"):
        st.success(f"✓  Early access request submitted for **{mod['name']}**. You will be notified when this module is available.")


# ── MAIN ROUTING ──────────────────────────────────────────────────────────────────
render_sidebar()

active = st.session_state.active_module
if active == "qm":
    render_qm_analyzer()
else:
    mod_data = next((m for m in MODULES if m["key"] == active), None)
    if mod_data:
        render_coming_soon(mod_data)