import requests
import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, whoami
from parser import parse_content  # Your custom parser function

# Load API key
load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set HUGGINGFACE_API_KEY in your environment.")

# Optional: Print account info to verify connection
api = HfApi()
print(whoami())

# Use the BART-based summarization model
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {api_key}"}

# Parse the input content from your JSON file
json_file_path = 'data.json'
parsed_content = parse_content(json_file_path)

# Convert parsed content into a formatted string
text_to_summarize = f"will this product help me silence my dog?: {parsed_content.get('title', 'No title')}. " \
                    f"Features: {' '.join(parsed_content.get('features', []))}. " \
                    f"Description: {' '.join(parsed_content.get('description', [])).strip()}."

print("Text to summarize:", text_to_summarize)  # Debugging step
print("\n")

# Prepare the correct input format for the BART model
data = {
    "inputs": text_to_summarize,  # BART requires a simple text string, not chat-style messages
    "parameters": {
        "max_length": 200,  # Adjust length as needed
        "temperature": 0.7
    }
}

# Send request to Hugging Face API
try:
    response = requests.post(API_URL, headers=headers, json=data, timeout=300)
    
    if response.status_code == 200:
        result = response.json()
        print("Summary:", result[0]["summary_text"])  # Correct key for BART models
    else:
        print(f"Error {response.status_code}: {response.json()}")
except Exception as e:
    print("An error occurred:", e)
