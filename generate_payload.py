import json

# Define the range of product IDs
start_id = 1300
end_id = 1600  # Adjust as needed

# Generate the payload
payload = [{"product_id": str(product_id)} for product_id in range(start_id, end_id)]

# Convert to JSON string
json_payload = json.dumps(payload, indent=4)

# Print or use the JSON payload
print(json_payload)
