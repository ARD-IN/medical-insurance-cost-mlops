# Deployment Guide

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## Local Deployment

### Prerequisites
- Python 3.10+
- Virtual environment
- All dependencies installed

### Steps

1. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Run the API**
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

3. **Test the deployment**
```bash
curl http://localhost:8000/health
```

## Docker Deployment

### Build Image

```bash
docker build -t insurance-api:latest .
```

### Run Container

```bash
docker run -d \
  --name insurance-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  insurance-api:latest
```

### Docker Compose

```bash
docker-compose up -d
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance Type: t2.micro (free tier) or t2.medium
   - Security Group: Open port 8000

2. **Install Docker**
```bash
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
```

3. **Deploy Application**
```bash
# Transfer files
scp -r * ubuntu@<ec2-ip>:/home/ubuntu/app/

# SSH to EC2
ssh ubuntu@<ec2-ip>

# Build and run
cd /home/ubuntu/app
docker build -t insurance-api .
docker run -d -p 8000:8000 insurance-api
```

### Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name insurance-rg --location eastus

# Create container
az container create \
  --resource-group insurance-rg \
  --name insurance-api \
  --image yourusername/insurance-api:latest \
  --dns-name-label insurance-api \
  --ports 8000
```

### Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/insurance-api

# Deploy to Cloud Run
gcloud run deploy insurance-api \
  --image gcr.io/PROJECT_ID/insurance-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Production Considerations

### 1. Environment Variables

Create `.env` file:
```env
ENVIRONMENT=production
LOG_LEVEL=info
MODEL_PATH=/app/models/model.pkl
```

### 2. Logging

Configure production logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 3. HTTPS/SSL

Use reverse proxy (Nginx):
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Monitoring

Implement health checks and monitoring:
- Use Prometheus for metrics
- Grafana for visualization
- CloudWatch/Stackdriver for cloud monitoring

### 5. Auto-scaling

Configure horizontal pod autoscaling (Kubernetes):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: insurance-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: insurance-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 6. Database (Optional)

For storing predictions:
```python
# Add to requirements.txt
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/insurance_db"
```

## Monitoring & Maintenance

### Health Monitoring

```bash
# Create monitoring script
#!/bin/bash
while true; do
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
  if [ $response != "200" ]; then
    echo "API is down! Restarting..."
    docker restart insurance-api
  fi
  sleep 60
done
```

### Log Rotation

Configure log rotation:
```bash
# /etc/logrotate.d/insurance-api
/var/log/insurance-api/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```