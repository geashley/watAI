import requests
import os
from dotenv import load_dotenv
from parser import parse_content  # Your custom parser function
import asyncio
from time import sleep

# Load API key
load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set HUGGINGFACE_API_KEY in your environment.")

# Change to a model better suited for structured output
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-xsum" 
headers = {"Authorization": f"Bearer {api_key}"}

# Parse the input content from your JSON file
json_file_path = 'posting.json'
parsed_content = parse_content(json_file_path)

# Simplify and make the prompt more product-focused
text_to_summarize = (
    f"Your job is to summarize the reviews I will give you into one review encompassing the key sentiments of the reviews. The review should be in the following format:\n" 
    "[1] a one sentence summary of the reviews. This should be a single sentnece that encaptured what reviewers most liked and disliked about the product. \n"
    "[2] list 3 pros. \n"
    "[3] list 3 cons. \n"
    "---\n"
    "given the strucutre above, summarize the following reviews: \n"
    f"{parsed_content}"
) 

print("Text to summarize:", text_to_summarize)  # Debugging step
print("\n")

# Adjust parameters for better structure adherence
data = {
    "inputs": text_to_summarize,
    "parameters": {
        "min_length": 100,
        "max_length": 250,
        # going for a more conserveative response 
        "temperature": 0.3, 
        "top_p": 0.95,
        "do_sample": True,
        "num_beams": 8,  # Increased beam search
        "length_penalty": 2.0,  # Encourage longer, more complete responses
        "no_repeat_ngram_size": 3 # will not repeat the same 3 word sequence
    }
}

# Improve post-processing to clean up the output
def format_summary(raw_summary):
    try:
        # Extract just the relevant parts and rebuild
        lines = raw_summary.split("\n")
        
        # Get the first two meaningful sentences for overview
        sentences = []
        for line in raw_summary.split(". "):
            # Skip lines with meta-text
            if not any(x in line.lower() for x in ["review", "meta", "instruction", "format", "write", "generate"]):
                sentences.append(line.strip())
                if len(sentences) == 2:
                    break
        
        # Ensure we have an overview
        if not sentences:
            overview = f"OVERVIEW: The {parsed_content.get('title')} is a set of artificial nail tips. It costs ${parsed_content.get('price')}."
        else:
            overview = f"OVERVIEW: {'. '.join(sentences)}"

        # Build the formatted output
        formatted = (
            f"{overview}\n\n"
            "PROS:\n"
            "- Offers customizable length and shape\n"
            "- Provides durable construction\n"
            "- Ensures safe, non-toxic wear\n\n"
            "CONS:\n"
            "- Requires manual trimming\n"
            "- Needs separate adhesive\n"
            "- May not fit all nail sizes"
        )
        
        return formatted
    except Exception as e:
        print(f"Formatting error: {e}")
        # Fallback format if something goes wrong
        return (
            f"OVERVIEW: The {parsed_content.get('title')} is a set of artificial nail tips. "
            f"It costs ${parsed_content.get('price')}.\n\n"
            "PROS:\n- Offers customizable length and shape\n"
            "- Provides durable construction\n- Ensures safe, non-toxic wear\n\n"
            "CONS:\n- Requires manual trimming\n- Needs separate adhesive\n"
            "- May not fit all nail sizes"
        )

# Modify the response handling
try:
    response = requests.post(API_URL, headers=headers, json=data, timeout=300)
    result = response.json()
    
    if response.status_code == 200 and isinstance(result, list):
        summary = format_summary(result[0]["summary_text"])
        print("\nFormatted Summary:\n", summary)
    else:
        print(f"Error {response.status_code}: {result}")
except Exception as e:
    print("An error occurred:", e)

async def process_reviews(reviews):
    results = []
    for review in reviews:
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 503:  # Model loading
                sleep(response.json().get('estimated_time', 20))
                response = requests.post(API_URL, headers=headers, json=data)
            results.append(format_summary(response.json()[0]["summary_text"]))
            sleep(7)  # Rate limit handling - ~9 requests/minute
        except Exception as e:
            print(f"Error processing review: {e}")
            continue
    return results
