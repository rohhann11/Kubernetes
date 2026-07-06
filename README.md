# ML Microservices Application

A complete microservices-based machine learning application with frontend and backend services.

## Architecture

```
┌─────────────┐
│  Frontend   │ (Port 80)
│   (Nginx)   │
└──────┬──────┘
       │
┌──────▼──────┐
│API Gateway  │ (Port 5000)
└──────┬──────┘
       │
   ┌───┴─────────────┬──────────────┐
   ▼                 ▼              ▼
┌─────────┐   ┌──────────────┐  ┌──────────┐
│   ML    │   │   Model      │  │   Data   │
│Prediction│   │  Training    │  │ Service  │
│(Port 5001)│  │ (Port 5002)  │  │(Port 5003)│
└─────────┘   └──────────────┘  └──────────┘
```

## Services

### 1. API Gateway (Port 5000)
- Routes requests to appropriate microservices
- Handles CORS for frontend communication
- Endpoints:
  - `GET /health` - Health check
  - `POST /api/predict` - Make ML predictions
  - `POST /api/train` - Train new models
  - `GET/POST /api/data` - Data management

### 2. ML Prediction Service (Port 5001)
- Loads and serves trained ML models
- Makes real-time predictions
- Endpoints:
  - `GET /health` - Health check
  - `POST /predict` - Get predictions
  - `POST /load-model` - Reload model

### 3. Model Training Service (Port 5002)
- Trains new ML models
- Manages training data
- Endpoints:
  - `GET /health` - Health check
  - `POST /train` - Train model
  - `POST /add-training-data` - Add training samples
  - `GET /training-data` - View training data

### 4. Data Service (Port 5003)
- Stores and manages data samples
- Provides data persistence
- Endpoints:
  - `GET /health` - Health check
  - `GET /data` - Retrieve data
  - `POST /data` - Add data sample
  - `POST /data/batch` - Add batch data
  - `POST /data/clear` - Clear all data

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost
# API Gateway: http://localhost:5000
```

### Manual Setup

```bash
# Install dependencies for each service
cd backend/api-gateway && pip install -r requirements.txt
cd ../ml-prediction-service && pip install -r requirements.txt
cd ../model-training-service && pip install -r requirements.txt
cd ../data-service && pip install -r requirements.txt

# Start each service in separate terminals
cd backend/api-gateway && python app.py
cd backend/ml-prediction-service && python app.py
cd backend/model-training-service && python app.py
cd backend/data-service && python app.py

# Serve frontend (requires a web server)
# Option 1: Python HTTP server
cd frontend && python -m http.server 80

# Option 2: Nginx (configured in docker-compose)
```

## Usage

### 1. Access the Dashboard
Open your browser and navigate to `http://localhost` (or `http://localhost:80`)

### 2. Check Service Status
Click "Check Services" to verify all microservices are running

### 3. Make Predictions
- Enter 4 feature values (0.0 to 1.0)
- Click "Get Prediction" to see the ML model's prediction

### 4. Train Models
- Set the number of training samples
- Click "Train New Model" to train a new model
- View training accuracy and statistics

### 5. Manage Data
- Add data samples with labels and values
- View stored data samples
- Use batch operations for multiple samples

## API Examples

### Make a Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 0.3, 0.7, 0.9]}'
```

### Train a Model
```bash
curl -X POST http://localhost:5000/api/train \
  -H "Content-Type: application/json" \
  -d '{"samples": 200}'
```

### Add Data Sample
```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"label": "sample1", "value": 42.5}'
```

### Get Data
```bash
curl http://localhost:5000/api/data
```

## Development

### Project Structure
```
/workspace
├── backend/
│   ├── api-gateway/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── ml-prediction-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── model-training-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── data-service/
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
├── frontend/
│   └── index.html
├── docker/
├── docker-compose.yml
└── README.md
```

### Adding New Services
1. Create a new directory in `backend/`
2. Add `app.py`, `requirements.txt`, and `Dockerfile`
3. Update `docker-compose.yml` to include the new service
4. Update the API Gateway to route to the new service

## Features

- ✅ Microservices architecture
- ✅ RESTful APIs
- ✅ Real-time ML predictions
- ✅ Model training capabilities
- ✅ Data management
- ✅ Interactive dashboard
- ✅ Service health monitoring
- ✅ Docker containerization
- ✅ CORS enabled for cross-origin requests
- ✅ Activity logging

## Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **ML**: scikit-learn, numpy, joblib
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (for frontend)

## License

MIT License