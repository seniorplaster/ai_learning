import streamlit as st
import json
import time
from google import genai
from google.genai import types

# ── PAGE SETUP ──────────────────────────────────────────
st.title("📞 CCaaS Call Quality Analyzer")
st.write("Upload a batch of call records and get AI-powered QM analysis.")

# ── API CLIENT — uses Streamlit's secrets system ───────
# Same line of code works locally AND once deployed - explained below
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = (
    "You are a senior Quality Management analyst at a contact center with "
    "20 years of experience. You will receive a call summary. "
    "Respond with a JSON object containing EXACTLY these three fields:\n"
    '{"strength": "one short bullet, under 15 words", '
    '"improvement": "one short bullet, under 15 words", '
    '"risk_flag": "Compliance Risk" or "Churn Risk" or "None"}\n'
    "Output ONLY the JSON object. No markdown, no code fences, no extra text."
)

def ask_gemini(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    return response.text

# ── FILE UPLOAD — replaces the hardcoded calls_batch.json ──
uploaded_file = st.file_uploader("Upload your calls_batch.json file", type="json")

# ── PROCESS BUTTON — gates the AI calls behind a click ─────
if uploaded_file is not None:
    calls = json.load(uploaded_file)
    st.write(f"Loaded {len(calls)} calls.")

    if st.button("Run QM Analysis"):
        results = []
        progress_bar = st.progress(0)   # visual progress indicator

        for i, call in enumerate(calls):
            try:
                raw_text = ask_gemini(call["transcript_summary"]).strip()
                if raw_text.startswith("```"):
                    raw_text = raw_text.strip("`").replace("json", "", 1).strip()
                ai_data = json.loads(raw_text)

                strength    = ai_data.get("strength", "N/A")
                improvement = ai_data.get("improvement", "N/A")
                risk_flag   = ai_data.get("risk_flag", "Unknown")
                status      = "SUCCESS"
            except Exception as e:
                strength, improvement, risk_flag = "ERROR", str(e), "Unknown"
                status = "FAILED"

            results.append({
                "call_id":     call["call_id"],
                "agent_id":    call["agent_id"],
                "csat_score":  call["csat_score"],
                "strength":    strength,
                "improvement": improvement,
                "risk_flag":   risk_flag,
                "status":      status
            })

            progress_bar.progress((i + 1) / len(calls))
            time.sleep(1)

        st.success(f"Done. {len(results)} calls analyzed.")

        # ── RESULTS TABLE — replaces print() statements ────
        st.dataframe(results)

        # ── DOWNLOAD BUTTON — replaces json.dump() to disk ─
        st.download_button(
            label="Download Report (JSON)",
            data=json.dumps(results, indent=2),
            file_name="qm_report.json",
            mime="application/json"
        )