import mysql.connector  
import os 
from dotenv import load_dotenv

load_dotenv()
# Load environment variables securely
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Ensure credentials are set
if not all([host, database, user, password]):
    raise ValueError("Database credentials are missing! Set them as environment variables.")

try:
    # Establish a secure database connection
    conn = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    if conn.is_connected():
        print("Connected to MySQL database.")

        # Create a cursor
        cursor = conn.cursor()

        # ASIN input
        asin_input = 'B003JN5ZEG'  # Replace with actual ASIN if needed

        # Query to fetch review text for the given ASIN
        query = """
            SELECT text 
            FROM reviews3 
            WHERE asin = %s;
        """

        cursor.execute(query, (asin_input,))
        
        # Add debugging information
        print(f"Query executed: {cursor._check_executed()}")
        reviews = cursor.fetchall()
        print(reviews)
        print(f"Number of reviews found: {len(reviews)}")

        # Concatenate all review texts into a single string
        long_review_text = ' '.join([review[0] for review in reviews])
        
        # Print first few reviews to verify
        for i, review in enumerate(reviews[:5]):
            print(f"Review {i+1}: {review[0][:100]}...")  # Print first 100 chars of each review

        # Define output file path
        output_file = 'reviews_for_asin.txt'

        # Write reviews to file securely
        with open(output_file, 'w') as file:
            file.write(long_review_text)

        print(f"Reviews for ASIN {asin_input} saved to {output_file}")

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    # Ensure cursor and connection are closed
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
