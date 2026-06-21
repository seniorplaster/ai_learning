import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ── SETUP HAPPENS ONCE, AT THE TOP ─────────────────────
# Not inside the function — this is created a single time and reused
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ── EXERCISE 3C — Reusable AI function ─────────────────
def ask_gemini(question):
    """Sends a question to Gemini and returns the text response."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a senior Quality Analyst with 20 years of "
                "experience in contact center call quality management."
            )
        )
    )
    return response.text


# ── EXERCISE 3D — evaluate_call_quality, now AI-aware ──
def evaluate_call_quality(call_duration, csat_score, was_resolved,
                           agent_id, transcript_summary):
    """
    Evaluates a call. If CSAT is low, asks Gemini for coaching advice
    based on the ACTUAL transcript summary — not a generic prompt.
    """

    if csat_score >= 4 and was_resolved:
        verdict  = "PASS"
        priority = "Low"
        coaching = "None needed - great job!"

    elif csat_score <= 2 or not was_resolved:
        # Notice the space added at the end of the first line ↓
        prompt = (
            f"Here is a summary of a contact center call: "
            f"'{transcript_summary}'. "
            f"In exactly 3 bullet points, coach this agent on how to "
            f"improve. Be specific to what happened in THIS call."
        )

        coaching = ask_gemini(prompt)   # reusing the function from 3C
        verdict  = "FAIL"
        priority = "High - Immediate review required"

    else:
        verdict  = "REVIEW"
        priority = "Medium"
        coaching = "Review call recording and provide targeted feedback to agent."

    return {
        "agent":    agent_id,
        "verdict":  verdict,
        "priority": priority,
        "coaching": coaching,
        "duration": call_duration
    }


# ── Calling it with real transcript context ────────────
result_1 = evaluate_call_quality(
    call_duration       = 245,
    csat_score          = 5,
    was_resolved        = True,
    agent_id            = "AGT-101",
    transcript_summary  = "Quick balance inquiry, handled efficiently."
)

result_2 = evaluate_call_quality(
    call_duration       = 612,
    csat_score          = 1,
    was_resolved        = False,
    agent_id            = "AGT-205",
    transcript_summary  = ("Customer reported unauthorized transaction. "
                            "Agent took 8 minutes to locate it, asked "
                            "customer to repeat details twice, gave no "
                            "interim resolution timeline.")
)

print(f"Agent {result_1['agent']}: {result_1['verdict']} ({result_1['priority']})")
print(f"Agent {result_2['agent']}: {result_2['verdict']} ({result_2['priority']})")
print(f"\nCoaching for {result_2['agent']}:\n{result_2['coaching']}")