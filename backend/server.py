from flask import Flask, request, jsonify
from flask_cors import CORS  # Don't forget to install this: pip install flask-cors
from reviewSummary import get_reviews, generate_summary  # Import your review function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/reviewpages', methods=['POST'])
def process_reviews():
    try:
        data = request.json
        asin_list = data.get('asinList', [])
        
        if not asin_list:
            raise ValueError("No Amazon IDs provided")
            
        # Process each ASIN and get summaries
        summaries = {}
        for asin in asin_list:
            reviews = get_reviews(asin)
            summary = generate_summary(reviews)
            summaries[asin] = summary # dictionary of asins and summaries

        print(summaries) # should print the dictionary of asin and summaries out 

        return jsonify({
            'success': True,
            'reviews': summaries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# def extract_asin(url):
#     # Implement ASIN extraction from Amazon URL
#     # Example: https://www.amazon.com/dp/B003JN5ZEG -> B003JN5ZEG
#     pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
