from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os
import pickle

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.getenv('MODEL_PATH', '/models/model.pkl')
model = None

def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            print("Model loaded successfully")
        else:
            # Create a default simple model if none exists
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression()
            # Train with dummy data
            X_dummy = np.random.rand(100, 4)
            y_dummy = (X_dummy.sum(axis=1) > 2).astype(int)
            model.fit(X_dummy, y_dummy)
            print("Default model created")
    except Exception as e:
        print(f"Error loading model: {e}")
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'ml-prediction'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        if model is None:
            load_model()
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0] if hasattr(model, 'predict_proba') else None
        
        result = {
            'prediction': int(prediction),
            'probability': probability.tolist() if probability is not None else None
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load-model', methods=['POST'])
def load_model_endpoint():
    try:
        load_model()
        return jsonify({'message': 'Model reloaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5001, debug=True)
