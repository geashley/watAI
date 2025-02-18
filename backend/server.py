from flask import Flask, request, jsonify
from flask_cors import CORS 
from reviewSummary import get_reviews, generate_summary

app = Flask(__name__)

# Configure CORS properly
CORS(app) 

@app.route('/reviewpages', methods=['POST'])
def process_reviews():
    try:
        data = request.json
        asin_list = data.get('asinList', [])
        
        if not asin_list:
            return jsonify({
                'success': False,
                'error': "No Amazon IDs provided"
            }), 400
            
        summaries = {}
        for asin in asin_list:
            try:
                reviews = get_reviews(asin)
                if not reviews:
                    summaries[asin] = {"error": f"No reviews found for ASIN: {asin}"}
                    continue
                    
                summary = generate_summary(reviews)
                summaries[asin] = summary
            except Exception as e:
                summaries[asin] = {"error": f"Failed to process ASIN {asin}: {str(e)}"}

        return jsonify({
            'success': True,
            'reviews': summaries
        })
        
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# def extract_asin(url):
#     # Implement ASIN extraction from Amazon URL
#     # Example: https://www.amazon.com/dp/B003JN5ZEG -> B003JN5ZEG
#     pass

if __name__ == '__main__':
    app.run(debug=True, port=8000)
