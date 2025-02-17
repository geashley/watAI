from flask import Flask, request, jsonify
from flask_cors import CORS  # Don't forget to install this: pip install flask-cors
from pullSummary import get_reviews  # Import your review function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/reviewpages', methods=['POST'])
def process_reviews():
    try:
        data = request.json
        product_link = data.get('productLink')
        
        # Extract ASIN from the Amazon link (you'll need to implement this)
        asin = extract_asin(product_link)
        
        # Call your existing review function
        reviews = get_reviews(asin)
        
        return jsonify({
            'success': True,
            'reviews': reviews
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def extract_asin(url):
    # Implement ASIN extraction from Amazon URL
    # Example: https://www.amazon.com/dp/B003JN5ZEG -> B003JN5ZEG
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
