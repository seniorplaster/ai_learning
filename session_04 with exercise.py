import json
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ── SETUP ──────────────────────────────────────────────
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a senior Quality Management analyst at a contact center with "
    "20 years of experience. You will receive a call summary. "
    "Respond with a JSON object containing EXACTLY these three fields:\n"
    '{"strength": "one short bullet, under 15 words", '
    '"improvement": "one short bullet, under 15 words", '
    '"risk_flag": "Compliance Risk" or "Churn Risk" or "None"}\n'
    "risk_flag must be exactly one of those three strings — nothing else.\n"
    "Output ONLY the JSON object. No markdown, no code fences, no extra text."
)

# ── REUSABLE FUNCTION (from Exercise 3C) ──────────────
def ask_gemini(question):
    """Sends a question to Gemini and returns the text response."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    return response.text


# ── LOAD THE BATCH ─────────────────────────────────────
with open("calls_batch.json", "r") as file:
    calls = json.load(file)

print(f"Loaded {len(calls)} calls. Starting analysis...\n")

# ── PROCESS EACH CALL ──────────────────────────────────
results = []   # we will collect every result here

for call in calls:
    print(f"Processing {call['call_id']}...")

    try:
        raw_text = ask_gemini(call["transcript_summary"]).strip()

        # Defensive cleanup - strip markdown code fences if the model added them anyway
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`").replace("json", "", 1).strip()

        ai_data = json.loads(raw_text)   # parse the JSON STRING into a Python dict

        strength    = ai_data.get("strength", "N/A")
        improvement = ai_data.get("improvement", "N/A")
        risk_flag   = ai_data.get("risk_flag", "Unknown")
        status      = "SUCCESS"

    except Exception as e:
        strength    = "ERROR"
        improvement = f"ERROR: {e}"
        risk_flag   = "Unknown"
        status      = "FAILED"

    result_record = {
        "call_id":     call["call_id"],
        "agent_id":    call["agent_id"],
        "csat_score":  call["csat_score"],
        "resolved":    call["resolved"],
        "strength":    strength,
        "improvement": improvement,
        "risk_flag":   risk_flag,
        "status":      status
    }

    results.append(result_record)
    # Be polite to the free API tier - small pause between calls
    time.sleep(1)

# ── SAVE THE REPORT ────────────────────────────────────
with open(f"qm_report_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json", "w") as file:
    json.dump(results, file, indent=2)

print(f"\nDone. {len(results)} calls analyzed. Report saved to qm_report_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json")

# ── PRINT A QUICK SUMMARY ──────────────────────────────
low_csat_count = 0
for r in results:
    if r["csat_score"] <= 2:
        low_csat_count += 1

print(f"Calls with CSAT <= 2 requiring review: {low_csat_count} of {len(results)}")