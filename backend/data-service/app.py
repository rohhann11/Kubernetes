from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = os.getenv('DATA_DIR', '/data')
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory data store (in production, use a proper database)
data_store = {
    'samples': [],
    'metadata': {
        'created_at': datetime.now().isoformat(),
        'total_samples': 0
    }
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'data-service'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({
            'count': len(data_store['samples']),
            'data': data_store['samples'][-limit:],
            'metadata': data_store['metadata']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = len(data_store['samples']) + 1
        
        data_store['samples'].append(data)
        data_store['metadata']['total_samples'] = len(data_store['samples'])
        
        return jsonify({
            'message': 'Data added successfully',
            'id': data['id'],
            'total_samples': data_store['metadata']['total_samples']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/batch', methods=['POST'])
def add_batch_data():
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({'error': 'No samples provided'}), 400
        
        count = 0
        for sample in data['samples']:
            sample['timestamp'] = datetime.now().isoformat()
            sample['id'] = len(data_store['samples']) + 1
            data_store['samples'].append(sample)
            count += 1
        
        data_store['metadata']['total_samples'] = len(data_store['samples'])
        
        return jsonify({
            'message': f'{count} samples added successfully',
            'total_samples': data_store['metadata']['total_samples']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/clear', methods=['POST'])
def clear_data():
    try:
        data_store['samples'] = []
        data_store['metadata']['total_samples'] = 0
        data_store['metadata']['updated_at'] = datetime.now().isoformat()
        
        return jsonify({'message': 'Data cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
