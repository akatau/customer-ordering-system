# Deployment Guide

## Quick Start

### Local Development with Docker

```bash
# Start all services (PostgreSQL, Redis, Backend)
make docker-up

# Wait for services to be healthy
docker ps

# Run migrations
make migrate-up

# Backend is ready at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## Deployment Environments

### Staging Deployment

```bash
# Deploy to staging
git push origin main

# GitHub Actions will automatically:
# 1. Run tests
# 2. Lint code
# 3. Build Docker image
# 4. Push to ECR
# 5. Deploy to staging EKS cluster
# 6. Run migrations
# 7. Health check

# Monitor deployment
kubectl get deployments -n staging
kubectl logs -f deployment/backend-api -n staging

# Verify functionality
curl https://staging-api.example.com/health
```

### Production Deployment

```bash
# Create release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# In GitHub: Actions > Deployment Pipeline
# Select: environment=production, revision=v1.0.0

# Or via CLI:
gh workflow run deploy.yml -f environment=production -f revision=v1.0.0
```

---

## Environment Variables

### Development (.env.local)

```bash
DATABASE_URL=postgresql://customer_user:local_dev_password@localhost:5432/customer_ordering
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Customer Ordering System API
DEBUG=true
ENVIRONMENT=development
```

### Staging (.env.staging)

```bash
DATABASE_URL=postgresql://user:password@staging-db.rds.amazonaws.com:5432/customer_ordering
REDIS_URL=redis://staging-redis.elasticache.amazonaws.com:6379/0
SECRET_KEY=<use-secrets-manager>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Customer Ordering System API
DEBUG=false
ENVIRONMENT=staging
```

### Production (.env.production)

```bash
DATABASE_URL=postgresql://user:password@prod-db.rds.amazonaws.com:5432/customer_ordering
REDIS_URL=redis://prod-redis.elasticache.amazonaws.com:6379/0
SECRET_KEY=<use-secrets-manager>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Customer Ordering System API
DEBUG=false
ENVIRONMENT=production
```

**Note**: Store sensitive values in AWS Secrets Manager or GitHub Secrets, not in environment files.

---

## Docker Container Operations

### Build Locally

```bash
cd backend
docker build -t customer-ordering-backend:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/app \
  -e REDIS_URL=redis://redis:6379/0 \
  -e SECRET_KEY=your-secret \
  customer-ordering-backend:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Remove volumes (WARNING: data loss)
docker-compose down -v
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Install kubectl
brew install kubectl

# Configure AWS credentials
aws configure

# Get kubeconfig
aws eks update-kubeconfig --name customer-ordering-prod --region us-east-1
```

### Deploy Manifest

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
    spec:
      containers:
      - name: backend-api
        image: <account>.dkr.ecr.us-east-1.amazonaws.com/customer-ordering-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: redis-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      
      - name: nginx-sidecar
        image: nginx:alpine
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: backend-api-service
  namespace: production
spec:
  selector:
    app: backend-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Deploy to Kubernetes

```bash
# Create secrets first
kubectl create secret generic backend-secrets \
  --from-literal=database-url=<DATABASE_URL> \
  --from-literal=redis-url=<REDIS_URL> \
  -n production

# Deploy
kubectl apply -f backend-deployment.yaml

# Check status
kubectl get deployments -n production
kubectl get pods -n production
kubectl describe pod <pod-name> -n production

# View logs
kubectl logs -f deployment/backend-api -n production

# Port forward for testing
kubectl port-forward service/backend-api-service 8000:80 -n production

# Update image (for new versions)
kubectl set image deployment/backend-api backend-api=<new-image>:tag -n production

# Rollback if needed
kubectl rollout undo deployment/backend-api -n production
kubectl rollout status deployment/backend-api -n production
```

---

## Database Migrations

### Run Migrations

```bash
cd backend
alembic upgrade head
```

### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Add user_preferences table"
```

### Review Migration

```bash
# Check migration file
cat alembic/versions/<migration_id>_*.py

# Review SQL
alembic downgrade <previous_revision> --sql
```

### Rollback

```bash
# Rollback one step
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

---

## Monitoring & Logging

### Application Logs

```bash
# Docker
docker logs customer-ordering-backend

# Kubernetes
kubectl logs -f deployment/backend-api -n production

# AWS CloudWatch
aws logs tail /aws/ecs/customer-ordering-backend --follow
```

### Health Checks

```bash
# Local
curl http://localhost:8000/health

# Staging
curl https://staging-api.example.com/health

# Production
curl https://api.example.com/health
```

### Performance Monitoring

```bash
# Check endpoint response times
curl -w "Time taken: %{time_total}s\n" http://localhost:8000/api/v1/products

# Load test
# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/products

# Using Apache Bench
ab -n 1000 -c 100 http://localhost:8000/api/v1/products
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -h <host> -U <user> -d <database> -c "SELECT 1"

# Check connection pool
curl http://localhost:8000/health | jq .db_pool_size
```

### Redis Connection Issues

```bash
# Test Redis connection
redis-cli -h <host> -p 6379 ping

# Check memory usage
redis-cli INFO memory
```

### Container Won't Start

```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id> | grep -A 10 "Env"

# Run with interactive shell
docker run -it --entrypoint /bin/bash <image>
```

### High Memory Usage

```bash
# Check Python process memory
ps aux | grep python

# Profile memory in app
pip install memory_profiler
python -m memory_profiler app/main.py
```

---

## Backup & Recovery

### Database Backup

```bash
# Full backup
pg_dump -h <host> -U <user> <database> > backup.sql

# Compressed backup
pg_dump -h <host> -U <user> <database> | gzip > backup.sql.gz

# Restore
psql -h <host> -U <user> <database> < backup.sql
```

### Point-in-Time Recovery

```bash
# AWS RDS PITR (automated backups)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier customer-ordering-db \
  --db-instance-identifier customer-ordering-db-recovered \
  --restore-time 2026-05-18T10:30:00Z
```

---

## Scaling

### Horizontal Scaling (Add Replicas)

```bash
# Kubernetes
kubectl scale deployment backend-api --replicas=5 -n production

# Auto-scaling (HPA)
kubectl autoscale deployment backend-api --min=3 --max=10 -n production
```

### Vertical Scaling (More Resources)

Edit deployment manifest to increase resource limits:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

---

## Rollback Procedures

### Rollback Failed Deployment

```bash
# Kubernetes
kubectl rollout undo deployment/backend-api -n production
kubectl rollout status deployment/backend-api -n production

# Via Docker (manual)
docker rm <container-id>
docker run -d --name backend-api-old <previous-image>
```

---

## Security Checklist

- ✅ SSL/TLS certificates installed
- ✅ Environment variables not committed to git
- ✅ Database credentials in secrets manager
- ✅ API keys rotated every 90 days
- ✅ WAF rules configured for production
- ✅ Firewall rules restrict access to database
- ✅ Container images scanned for vulnerabilities
- ✅ Logs centralized and encrypted

---

## Support & Issues

For deployment issues:
- Check logs: `kubectl logs -f deployment/backend-api`
- Health check: `curl {BASE_URL}/health`
- Metrics: View in monitoring dashboard
- Contact: #DevOps channel or deployment team

