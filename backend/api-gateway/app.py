from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Service URLs
ML_PREDICTION_SERVICE = os.getenv('ML_PREDICTION_SERVICE_URL', 'http://localhost:5001')
MODEL_TRAINING_SERVICE = os.getenv('MODEL_TRAINING_SERVICE_URL', 'http://localhost:5002')
DATA_SERVICE = os.getenv('DATA_SERVICE_URL', 'http://localhost:5003')

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'ML Microservices API Gateway',
        'endpoints': {
            'health': '/health',
            'predict': '/api/predict (POST)',
            'train': '/api/train (POST)',
            'data': '/api/data (GET/POST)'
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'api-gateway'}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        response = requests.post(f'{ML_PREDICTION_SERVICE}/predict', json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 503

@app.route('/api/train', methods=['POST'])
def train():
    try:
        data = request.get_json()
        response = requests.post(f'{MODEL_TRAINING_SERVICE}/train', json=data, timeout=300)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 503

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    try:
        if request.method == 'GET':
            response = requests.get(f'{DATA_SERVICE}/data', timeout=10)
        else:
            data = request.get_json()
            response = requests.post(f'{DATA_SERVICE}/data', json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
