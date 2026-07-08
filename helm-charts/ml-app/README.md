# ML Microservices Helm Chart

A Helm chart for deploying a complete Machine Learning microservices application on Kubernetes.

## Overview

This chart deploys the following components:
- **API Gateway** - Central entry point for all API requests
- **ML Prediction Service** - Handles real-time ML predictions
- **Model Training Service** - Manages model training jobs
- **Data Service** - Handles data storage and retrieval
- **Frontend** - Web UI for interacting with the ML services

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Container images built and available in your registry

## Installation

### Add the chart repository (if hosted)
```bash
helm repo add ml-charts https://your-repo.com/charts
helm repo update
```

### Install the chart
```bash
helm install ml-app ./helm-charts/ml-app
```

Or with a custom release name:
```bash
helm install my-ml-app ./helm-charts/ml-app --namespace ml-system --create-namespace
```

## Configuration

The following table lists the configurable parameters of this chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas for each service | `1` |
| `image.repository` | Docker image repository | `ml-app` |
| `image.tag` | Docker image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `apiGateway.serviceType` | Service type for API Gateway | `LoadBalancer` |
| `apiGateway.port` | Port for API Gateway | `5000` |
| `mlPrediction.port` | Port for ML Prediction Service | `5001` |
| `modelTraining.port` | Port for Model Training Service | `5002` |
| `dataService.port` | Port for Data Service | `5003` |
| `frontend.serviceType` | Service type for Frontend | `LoadBalancer` |
| `frontend.port` | Port for Frontend | `80` |
| `frontend.containerPort` | Container port for Frontend | `3000` |
| `ingress.enabled` | Enable ingress | `false` |

### Custom Values Example

Create a `custom-values.yaml` file:

```yaml
replicaCount: 2

image:
  repository: myregistry.io/ml-app
  tag: "v1.0.0"

apiGateway:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: ml-app.example.com
      paths:
        - path: /
          pathType: Prefix
```

Then install with:
```bash
helm install ml-app ./helm-charts/ml-app -f custom-values.yaml
```

## Uninstall

```bash
helm uninstall ml-app
```

## Verify Deployment

Check that all pods are running:
```bash
kubectl get pods -l "app.kubernetes.io/name=ml-app"
```

View service endpoints:
```bash
kubectl get svc -l "app.kubernetes.io/name=ml-app"
```

## Access the Application

### Via LoadBalancer
```bash
export SERVICE_IP=$(kubectl get svc ml-app-api-gateway -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
echo "API Gateway: http://$SERVICE_IP:5000"
echo "Frontend: http://$SERVICE_IP:80"
```

### Via Port Forward
```bash
# API Gateway
kubectl port-forward svc/ml-app-api-gateway 5000:5000

# Frontend
kubectl port-forward svc/ml-app-frontend 3000:80
```

## API Endpoints

Once deployed, you can access the following endpoints:

- `GET /health` - Health check
- `POST /api/predict` - Make predictions
  ```json
  {
    "features": [1.0, 2.0, 3.0, 4.0]
  }
  ```
- `POST /api/train` - Train models
  ```json
  {
    "model_type": "random_forest",
    "epochs": 10
  }
  ```
- `GET /api/data` - Get all data
- `POST /api/data` - Add new data

## Troubleshooting

### Check pod status
```bash
kubectl describe pod <pod-name>
```

### View logs
```bash
kubectl logs -f <pod-name>
```

### Check events
```bash
kubectl get events --sort-by='.lastTimestamp'
```

## Scaling

To scale a specific service:
```bash
kubectl scale deployment ml-app-ml-prediction --replicas=3
```

Or update values.yaml and run:
```bash
helm upgrade ml-app ./helm-charts/ml-app
```

## License

MIT License
