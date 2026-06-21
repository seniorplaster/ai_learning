import json

# If loading from a file:
with open("queues.json", "r") as f:
    data = json.load(f)

# If the JSON is already a Python dict, skip the above and assign directly:
# data = {...}  # your parsed dict

ids = [entity["id"] for entity in data["entities"]]

print(ids)


import json

# If loading from a file:
with open("wrapups.json", "r") as f:
    data = json.load(f)

# If the JSON is already a Python dict, skip the above and assign directly:
# data = {...}  # your parsed dict

ids = [entity["id"] for entity in data["entities"]]

print(ids)