import os
from dotenv import load_dotenv
from groq import Groq

import mysql.connector

def get_reviews(asin):
    load_dotenv()
    
    # Load environment variables securely
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    # Ensure credentials are set
    if not all([host, database, user, password]):
        raise ValueError("Database credentials are missing!")

    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            # Query to fetch review text and rating
            query = """
                SELECT text, rating 
                FROM reviews3 
                WHERE asin = %s;
            """

            cursor.execute(query, (asin,))
            reviews = cursor.fetchall()
            
            # Format reviews for AI processing
            review_list = [{"text": review["text"], "rating": review["rating"]} for review in reviews]
            
            return review_list

    except mysql.connector.Error as e:
        raise Exception(f"Database error: {str(e)}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def generate_summary(reviews):
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ API key not found")

    client = Groq(api_key=api_key)

    review_texts = [f"Review: {review['text']}" for review in reviews]
    all_reviews_text = "\n".join(review_texts)

    # Modified prompt to request JSON-like structure
    prompt = (
        "Based on the following reviews, please provide a summary in this exact format:\n"
        "SUMMARY: [overall product summary]\n"
        "PRO1: [first major pro]\n"
        "PRO2: [second major pro]\n"
        "PRO3: [third major pro]\n"
        "CON1: [first major con]\n"
        "CON2: [second major con]\n"
        "CON3: [third major con]\n\n"
        f"{all_reviews_text}\n\n"
        "Please maintain the exact format with SUMMARY:, PRO1:, etc. at the start of each line."
    )
    
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )

    # Parse the response into a dictionary
    content = response.choices[0].message.content
    summary_dict = {}
    
    for line in content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            summary_dict[key.strip()] = value.strip()

    return summary_dict

if __name__ == "__main__":
    # Test the function
    test_reviews = [{"text": "Great product!", "rating": 5}]
    summary = generate_summary(test_reviews)
    print(summary)