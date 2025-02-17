import mysql.connector  

# Replace these with your actual RDS credentials
host = 'my-db-instance.ctuqm8m24ut8.us-east-2.rds.amazonaws.com'
database = 'my_db_instance'
user = 'admin'
password = 'Elyssa1024768'

cursor = mysql.connector.cursor()

# Get the ASIN input from the user (or hardcode it in)
asin_input = 'B00BKSPPVA'  # Replace with the ASIN you're interested in

# Write the query to get the "text" for the reviews with the specified ASIN
query = """
    SELECT review_text 
    FROM reviews 
    WHERE parent_asin = %s;
"""

# Execute the query
cursor.execute(query, (asin_input,))

# Fetch all results
reviews = cursor.fetchall()

# Create a long string by concatenating all the review texts
long_review_text = ' '.join([review[0] for review in reviews])

# Close the cursor and connection
cursor.close()
conn.close()

# Define the output file path
output_file = 'reviews_for_asin.txt'

# Open the file in write mode to overwrite it
with open(output_file, 'w') as file:
    file.write(long_review_text)

print(f"Reviews for ASIN {asin_input} saved to {output_file}")