import os
from dotenv import load_dotenv
from groq import Groq

def generate_summary(reviews):
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ API key not found")

    client = Groq(api_key=api_key)

    # Format reviews into text
    review_texts = [f"Review: {review['text']}" for review in reviews]
    all_reviews_text = "\n".join(review_texts)

    # Generate summary using AI
    prompt = (
        "Based on the following reviews, please provide a structured summary that includes:\n"
        "1. An overall summary of the product in your own words.\n"
        "2. The top 3 pros in bullet points.\n"
        "3. The top 3 cons in bullet points.\n\n"
        f"{all_reviews_text}\n\n"
    )
    
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Test the function
    test_reviews = [{"text": "Great product!", "rating": 5}]
    summary = generate_summary(test_reviews)
    print(summary)