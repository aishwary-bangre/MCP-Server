import requests

url = "http://127.0.0.1:8000/append_to_doc"
payload = {
    "doc_id": "1yDummyDocID_PleaseIgnore-1234567890",
    "content": "## Automated Test Entry\n\nThis is a test of the HITL approval flow!"
}

print("Sending request to server for append_to_doc...")
response = requests.post(url, json=payload)
print(f"Response ({response.status_code}): {response.text}")
