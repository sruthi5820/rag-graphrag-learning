
import requests
import json

# Part 1: Make an API request
url = "http://localhost:8000/health"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    print("=== API Request ===")
    print("Status:", response.status_code)
    print("Response:", response.json())

except requests.RequestException as error:
    print("API request failed:", error)

# Part 2: JSON encoding and decoding
print("\n=== JSON Encoding and Decoding ===")

payload = {
    "question": "What is RAG?",
    "top_k": 5
}

# Convert Python dictionary to JSON string
encoded = json.dumps(payload, indent=2)
print("Encoded JSON:")
print(encoded)

# Convert JSON string back to Python dictionary
decoded = json.loads(encoded)
print("\nDecoded question:", decoded["question"])
print("Decoded top_k:", decoded["top_k"])
