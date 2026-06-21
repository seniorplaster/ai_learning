# -- STRING --- text, surrounded by quotes
client_name = "Emirates NBD"
agent_name = "Sara Al Mansoori"
call_status = "Resolved"

# -- INTEGER --- whole numbers, no quotes
call_duration = 347  # seconds
queue_position = 3
calls_in_queue = 25

# -- FLOAT -- decimal numbers
csat_score = 4.7
handle_time_avg = 3.25 # minutes
abandon_rate = 0.082 # 8.2%

# -- BOOLEANS -- True or False only, no quotes
is_vip_customer = True
call_recorded = True
escalated = False

# Print them all with f-strings
print(f"Clinet:{client_name}")
print(f"Agent: {agent_name}")
print(f"Call Status: {call_status}")
print(f"Call Duration: {call_duration} seconds")
print(f"Queue Position: {queue_position}")
print(f"Calls in Queue: {calls_in_queue}")
print(f"CSAT Score: {csat_score}")
print(f"Average Handle Time: {handle_time_avg} minutes")
print(f"Abandon Rate: {abandon_rate * 100}%")
print(f"Is VIP Customer: {is_vip_customer}")
print(f"Call Recorded: {call_recorded}")
print(f"Escalated: {escalated}")
