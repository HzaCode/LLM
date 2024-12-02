import requests


HUGGINGFACE_API_KEY = ""

# API Endpoint
API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B-Preview"


user_input = "How many 'r' are there in the word 'strawberry'?"

# Build request payload
payload = {
    "inputs": f"You are a helpful assistant. User: {user_input}",
    "parameters": {
        "max_length": 100,  # Restrict output length
        "top_p": 0.9,       # Diversity control
        "temperature": 0.7  # Randomness control
    },
    "options": {"use_cache": True, "wait_for_model": True}  # Enable model caching
}

# Set authorization headers
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


response = requests.post(API_URL, headers=headers, json=payload)


if response.status_code == 200:
    print("Hugging Face Qwen QwQ-32B-Preview Reply:")
    print(response.json()[0]["generated_text"])  # Print generated response
else:
    print(f"Request failed, status code: {response.status_code}")
    print(response.json())
