import json

# Load your JSON file
with open("examples/json_schemas.json") as f:
    data = json.load(f)

# Print top-level keys
print("Keys:", list(data.keys()))

# Print the full transaction example
print("Full transaction preview:")
print(json.dumps(data["full_transaction_example"], indent=2))

