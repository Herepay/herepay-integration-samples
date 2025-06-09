from flask import Flask, render_template, request
import requests
import hashlib
import hmac
import json
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY', 'your_api_key')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
PRIVATE_KEY = os.getenv('PRIVATE_KEY', 'your_private_key')

app = Flask(__name__)

def generate_checksum(data, private_key):
    """Generate checksum for payment data"""
    # Sort the data by keys
    sorted_data = dict(sorted(data.items()))
    
    # Extract values and handle arrays/objects
    values = []
    for key, value in sorted_data.items():
        if isinstance(value, (dict, list)):
            values.append(json.dumps(value))
        else:
            values.append(str(value))
    
    # Concatenate values with comma
    concatenated_data = ','.join(values)
    
    # Generate HMAC SHA256
    return hmac.new(
        private_key.encode('utf-8'),
        concatenated_data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

@app.route('/')
def index():
    """Render the payment form"""
    return render_template('index.html')

@app.route('/submit-payment', methods=['POST'])
def submit_payment():
    """Handle payment submission"""
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Configuration (replace with your actual credentials)
        private_key = PRIVATE_KEY 
        secret_key = SECRET_KEY
        api_key = API_KEY
        
        
        # Generate checksum
        checksum = generate_checksum(data, private_key)
        data['checksum'] = checksum

        print(f"Checksum: {checksum}")
        
        # Setup headers
        headers = {
            'SecretKey': secret_key,
            'XApiKey': api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Send request to Herepay
        response = requests.post(
            'https://uat.herepay.org/api/v1/herepay/initiate',
            data=urlencode(data),
            headers=headers
        )
        
        # Return the response
        return response.text, response.status_code
        
    except Exception as e:
        return f"Error initiating payment: {str(e)}", 500

@app.route('/redirect', methods=['POST'])
def redirect_handler():
    """Handle payment redirect/callback"""
    if request.method == 'POST':
        payload = request.form.to_dict()
        
        if payload.get('status_code') == '00':
            return 'Payment successful!'
        else:
            message = payload.get('message', 'Unknown error')
            return f'Payment failed: {message}'
    else:
        return 'Invalid access.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010) 