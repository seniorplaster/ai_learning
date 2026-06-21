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
    "20 years of experience. You will receive a call summary. Respond with "
    "EXACTLY 3 short bullet points: (1) one strength, (2) one improvement "
    "area. Compile Each bullet under 15 words. No introduction, no extra text."
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
        ai_feedback = ask_gemini(call["transcript_summary"])
        status = "SUCCESS"
    except Exception as e:
        ai_feedback = f"ERROR: {e}"
        status = "FAILED"

    # Build a clean result record combining original data + AI output
    result_record = {
        "call_id":     call["call_id"],
        "agent_id":    call["agent_id"],
        "csat_score":  call["csat_score"],
        "resolved":    call["resolved"],
        "ai_feedback": ai_feedback,
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