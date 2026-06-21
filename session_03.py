# ── STRINGS ── text, surrounded by quotes
client_name = "Emirates NBD"
agent_name  = "Sara Al Mansoori"
call_status = "Resolved"

# ── INTEGERS ── whole numbers, no quotes
call_duration   = 347        # seconds
queue_position  = 3
calls_in_queue  = 28

# ── FLOATS ── decimal numbers
csat_score      = 4.7
handle_time_avg = 3.25       # minutes
abandon_rate    = 0.082      # 8.2%

# ── BOOLEANS ── True or False only, no quotes
is_vip_customer  = True
call_recorded    = True
escalated        = False

# Print them all with f-strings
print(f"Client: {client_name}")
print(f"Agent: {agent_name}")
print(f"CSAT: {csat_score}")
print(f"VIP: {is_vip_customer}")
print(f"Duration: {call_duration} seconds")
print(f"Queue Position: {queue_position}")
print(f"Calls in Queue: {calls_in_queue}")

# A list of queued calls - square brackets, items separated by commas
call_queue = ["Call_001", "Call_002", "Call_003", "Call_004", "Call_005"]

# Access by position - Python counts from ZERO, not one
print(call_queue[0])    # Call_001  ← first item is [0]
print(call_queue[1])    # Call_002  ← second item is [1]
print(call_queue[-1])   # Call_005  ← last item, always [-1]

# How many items?
print(len(call_queue))  # 5

# Add a new call to the end of the queue
call_queue.append("Call_006")
print(len(call_queue))  # 6

# Remove the first call (it was answered)
call_queue.pop(0)
print(call_queue)       # ['Call_002', 'Call_003', 'Call_004', 'Call_005', 'Call_006']

# A list of AI chat messages - this is the EXACT structure the APIs use
conversation_history = [
    "User: What is my account balance?",
    "Assistant: Your current balance is AED 12,450.",
    "User: Can I increase my credit limit?"
]

print(f"Conversation has {len(conversation_history)} turns so far")


# A caller's CRM screen-pop as a Python dictionary
# Curly braces {}, key: value pairs, separated by commas
caller_record = {
    "account_id":     "ACC-88421",
    "full_name":      "Mohammed Al Rashidi",
    "segment":        "Premier Banking",
    "is_vip":         True,
    "open_tickets":   2,
    "csat_last_call": 3.2,
    "preferred_lang": "Arabic"
}

# Access values by key name - use square brackets with the key
print(caller_record["full_name"])       # Mohammed Al Rashidi
print(caller_record["segment"])         # Premier Banking
print(caller_record["is_vip"])          # True
print(caller_record["csat_last_call"])  # 3.2

# Add a new field
caller_record["call_reason"] = "Credit limit inquiry"

# Update an existing field
caller_record["open_tickets"] = 3

# Check if a key exists before accessing it (safe practice)
if "preferred_lang" in caller_record:
    print(f"Serve in: {caller_record['preferred_lang']}")

# A dictionary inside a list - this is the messages format the APIs use
messages = [
    {"role": "system",    "content": "You are a helpful banking assistant."},
    {"role": "user",      "content": "What is my balance?"},
    {"role": "assistant", "content": "Your balance is AED 12,450."},
    {"role": "user",      "content": "Can I increase my limit?"}
]

# Access the last user message
print(messages[-1]["content"])    # Can I increase my limit?
print(messages[-1]["role"])       # user

# IVR-style call routing in Python
call_data = {
    "ani":           "+971501234567",
    "queue":         "Technical Support",
    "wait_seconds":  245,
    "vip_tier":      "Gold",
    "language":      "English",
    "csat_avg":      2.8
}

# Routing decision logic - maps directly to IVR condition blocks
if call_data["vip_tier"] == "Platinum":
    print("Route: Dedicated Platinum desk — immediate answer")

elif call_data["vip_tier"] == "Gold" and call_data["wait_seconds"] > 120:
    print("Route: Gold priority queue — manager callback offered")

elif call_data["csat_avg"] < 3.0:
    print("Route: Retention team — at-risk customer flag applied")

elif call_data["wait_seconds"] > 300:
    print("Route: Overflow team — SLA breach imminent")

else:
    print("Route: Standard queue — normal handling")

# Python comparison operators - identical to what you use in IVR logic
# ==   equals
# !=   not equals
# >    greater than
# <    less than
# >=   greater than or equal
# <=   less than or equal
# and  both conditions must be true
# or   either condition must be true
# not  reverse a condition


# Batch of calls to process
call_batch = [
    {"id": "C001", "duration": 187, "resolved": True,  "csat": 5},
    {"id": "C002", "duration": 643, "resolved": False, "csat": 2},
    {"id": "C003", "duration": 312, "resolved": True,  "csat": 4},
    {"id": "C004", "duration": 89,  "resolved": True,  "csat": 5},
    {"id": "C005", "duration": 521, "resolved": False, "csat": 1},
]

# Process every call in the batch
print("=== Daily Call QM Report ===")

for call in call_batch:
    # 'call' is a temporary variable - takes each dictionary one at a time
    status = "✓ Resolved" if call["resolved"] else "✗ Escalation needed"
    flag   = " ⚠ LOW CSAT" if call["csat"] <= 2 else ""

    print(f"Call {call['id']} | {call['duration']}s | CSAT: {call['csat']} | {status}{flag}")

# Calculate the average CSAT across all calls
total_csat = 0
for call in call_batch:
    total_csat = total_csat + call["csat"]

average_csat = total_csat / len(call_batch)
print(f"\nBatch average CSAT: {average_csat:.1f}")   # :.1f = 1 decimal place


# Define a function with 'def', give it a name, list its inputs in ()
def evaluate_call_quality(call_duration, csat_score, was_resolved, agent_id):
    """
    Evaluates a single call and returns a QM verdict.
    This is a docstring - explains what the function does.
    """

    # Build the verdict based on conditions
    if csat_score >= 4 and was_resolved:
        verdict  = "PASS"
        priority = "Low"
        coaching = "None needed - great job!"
    elif csat_score <= 2 or not was_resolved:
        import os
        import os

        from google import genai
        from google.genai import types
        from dotenv import load_dotenv
        load_dotenv()


        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "In exactly 3 bullet points, list the 3 most important things"
                "to coach agent on how to improve the quality of their calls"
                ),
            config=types.GenerateContentConfig(
                system_instruction=(
                    "you are a senior Quality Analyst with 20 years of experience in contact center call quality management."
                )
            )
        )
        verdict  = "FAIL"
        priority = "High - Immediate review required"
        coaching = response.text

    else:
        verdict  = "REVIEW"
        priority = "Medium"
        coaching = "Review call recording and provide targeted feedback to agent."

    # Return a dictionary with all results
    return {
        "agent":    agent_id,
        "verdict":  verdict,
        "priority": priority,
        "coaching": coaching,
        "duration": call_duration
    }


# Call the function - pass in the values it needs
result_1 = evaluate_call_quality(
    call_duration = 245,
    csat_score    = 5,
    was_resolved  = True,
    agent_id      = "AGT-101"
)

result_2 = evaluate_call_quality(
    call_duration = 612,
    csat_score    = 1,
    was_resolved  = False,
    agent_id      = "AGT-205"
)



# Use the returned dictionaries
print(f"Agent {result_1['agent']}: {result_1['verdict']} ({result_1['priority']}) coaching: ({result_1['coaching']})")
print(f"Agent {result_2['agent']}: {result_2['verdict']} ({result_2['priority']}) coaching: ({result_2['coaching']})")


