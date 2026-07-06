from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
import pickle
from datetime import datetime

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.getenv('MODEL_PATH', '/models/model.pkl')
DATA_DIR = os.getenv('DATA_DIR', '/data')

# In-memory storage for training data (in production, use a database)
training_data = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'model-training'}), 200

@app.route('/train', methods=['POST'])
def train():
    try:
        from sklearn.linear_model import LogisticRegression
        
        data = request.get_json()
        
        # Get training data from request or use stored data
        if data and 'X' in data and 'y' in data:
            X = np.array(data['X'])
            y = np.array(data['y'])
        elif training_data:
            X = np.array([item['features'] for item in training_data])
            y = np.array([item['label'] for item in training_data])
        else:
            # Generate synthetic training data
            print("Generating synthetic training data...")
            X = np.random.rand(200, 4)
            y = (X[:, 0] + X[:, 1] > 1).astype(int)
        
        # Train model
        print(f"Training model with {len(X)} samples...")
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        
        # Save model
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        accuracy = model.score(X, y)
        
        return jsonify({
            'message': 'Model trained successfully',
            'accuracy': float(accuracy),
            'samples_used': len(X),
            'model_path': MODEL_PATH,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-training-data', methods=['POST'])
def add_training_data():
    try:
        data = request.get_json()
        
        if 'features' not in data or 'label' not in data:
            return jsonify({'error': 'Missing features or label'}), 400
        
        training_data.append({
            'features': data['features'],
            'label': data['label'],
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'message': 'Training data added',
            'total_samples': len(training_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/training-data', methods=['GET'])
def get_training_data():
    return jsonify({
        'count': len(training_data),
        'data': training_data[-100:]  # Return last 100 samples
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
