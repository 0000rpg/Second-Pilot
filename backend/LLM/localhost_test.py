import requests
import json

# API endpoint
url = "http://localhost:1234/v1/chat/completions"

# Headers
headers = {
    "Content-Type": "application/json"
}

# Payload (matches the curl -d data)
payload = {
    "model": "gemma-3-1b-it-qat",
    "messages": [
        {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
        {"role": "user", "content": "What day is it today?"}
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": False
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)

# Check response
if response.status_code == 200:
    # Print the JSON response (formatted for readability)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print(f"Request failed with status {response.status_code}")
    print(response.text)