import requests
from parser import parse_content  # Import your custom parser function
import os
from dotenv import load_dotenv


# API URL and Authorization Header
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"


# Load environment variables from .env file (if it exists)
load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")

# Parse the content using your custom function
parsed_content = parse_content()

if not api_key:
    raise ValueError("API key not found. Please set HUGGINGFACE_API_KEY in your environment or .env file.")

headers = {"Authorization": f"Bearer {api_key}"}


# Prepare the input data for summarization
data = {
    "inputs": f"Summarize the following content: {parsed_content}",
    "parameters": {
        "max_length": 200,  # Limit the output length of the summary
        "temperature": 0.7  # Optional: Control creativity (lower = less creative)
    }
}

# Send a POST request to Hugging Face's API
response = requests.post(API_URL, headers=headers, json=data)

# Handle and display the response
if response.status_code == 200:
    result = response.json()
    print("Summary:", result[0]["generated_text"])  # Print the summarized text
else:
    print(f"Error {response.status_code}: {response.json()}")
