import mysql.connector
import os
from dotenv import load_dotenv
from reviewSummary import generate_summary  

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
            cursor = conn.cursor()

            # Query to fetch review text
            query = """
                SELECT text 
                FROM reviews3 
                WHERE asin = %s;
            """

            cursor.execute(query, (asin,))
            reviews = cursor.fetchall()
            
            # Format reviews for AI processing
            review_list = [{"text": review[0], "rating": 0} for review in reviews]
            
            # Generate AI summary from the reviews
            summary = generate_summary(review_list)
            
            return summary

    except mysql.connector.Error as e:
        raise Exception(f"Database error: {str(e)}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    # Test the function
    test_asin = 'B003JN5ZEG'
    summary = get_reviews(test_asin)
    print("AI-Generated Summary:")
    print("=" * 80)
    print(summary)
    print("=" * 80)
