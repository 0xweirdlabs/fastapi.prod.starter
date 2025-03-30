# Production Deployment Guide

This guide outlines how to deploy this FastAPI framework in a resilient, horizontally scalable production environment. These strategies will help you build an architecture that can handle increasing loads by adding more instances rather than increasing the size of individual servers.

## Architecture Overview

A production-ready, horizontally scalable deployment typically includes:

![Horizontal Scaling Architecture](https://miro.medium.com/max/1400/1*xJCYx9TL7nFRxfkxjGLQng.png)

## Load Balancing Layer

### Load Balancer Options
- **Cloud Provider Load Balancers**: AWS ELB/ALB, Google Cloud Load Balancer, Azure Load Balancer
- **Software Load Balancers**: Nginx, HAProxy, Traefik

### Configuration Recommendations
- Enable health checks to route traffic only to healthy instances
- Configure proper timeouts (typically 30-60 seconds for API endpoints)
- Set up SSL termination at the load balancer level
- For WebSocket support (if needed), ensure proper idle timeout configurations

### Sample Nginx Configuration
```nginx
upstream fastapi_backend {
    server fastapi_app_1:8000;
    server fastapi_app_2:8000;
    server fastapi_app_3:8000;
    # Add more servers as you scale
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check configuration
        health_check interval=10 fails=3 passes=2;
    }
}
```

## Application Layer Scaling

### Containerization
The application is already containerized with Docker. For production:

1. Use multi-stage builds to keep images small
2. Pin specific versions of base images
3. Use non-root users in containers

### Kubernetes Deployment
Sample Kubernetes deployment manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  namespace: production
spec:
  replicas: 3  # Start with 3 replicas
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-app
        image: your-registry/fastapi-app:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
          - name: DATABASE_URL
            valueFrom:
              secretKeyRef:
                name: app-secrets
                key: database-url
          - name: SUPABASE_URL
            valueFrom:
              secretKeyRef:
                name: app-secrets
                key: supabase-url
          # Add other environment variables
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
```

### Autoscaling Configuration
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Database Layer

### PostgreSQL Configuration
This application already supports PostgreSQL. For production:

1. Use a managed PostgreSQL service (AWS RDS, Google Cloud SQL, Azure Database for PostgreSQL)
2. Set up read replicas for read-heavy workloads
3. Implement proper backup strategies
4. Configure connection pooling

### Connection Pooling with PgBouncer
PgBouncer sits between your application and database to manage connection pools effectively:

```ini
[databases]
* = host=database.example.com port=5432

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

Update your application's DATABASE_URL to point to PgBouncer instead of directly to PostgreSQL.

## Resilience Mechanisms

### Circuit Breakers and Retries
The application already implements circuit breakers and retries via Stamina. Ensure proper configuration in production:

1. Set appropriate timeout values
2. Configure retry limits and backoff strategies
3. Monitor circuit breaker state

### Health Checks
Add dedicated health check endpoints:

```python
@app.get("/health")
async def health_check():
    # Basic health check
    return {"status": "healthy"}

@app.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    # Database health check
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")
```

## Monitoring and Observability

### Prometheus and Grafana
The application already has Prometheus metrics. In production:

1. Deploy Prometheus server to scrape metrics
2. Set up Grafana dashboards for visualization
3. Configure alerts for critical conditions

### Logging
Implement centralized logging:

1. Use structured logging (JSON format)
2. Ship logs to a centralized system (ELK Stack, Loki, etc.)
3. Add request IDs for tracing requests across services

```python
# Add correlation ID middleware
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    
    return response
```

## Security Considerations

1. **API Security**:
   - Rate limiting
   - Input validation (already handled by Pydantic)
   - Authentication (JWT or Supabase Auth as configured)

2. **Infrastructure Security**:
   - Network policies to restrict traffic between services
   - Secrets management (Kubernetes Secrets, HashiCorp Vault)
   - Regular security updates

## CI/CD Pipeline

Set up a CI/CD pipeline for automated testing and deployment:

1. **Testing Stage**:
   - Run unit and integration tests
   - Perform security scanning
   - Check code quality

2. **Deployment Strategies**:
   - Blue/Green deployment
   - Canary releases
   - Rollback capabilities

Example GitHub Actions workflow:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      - name: Run tests
        run: python -m pytest

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: .docker/Dockerfile.prod
          push: true
          tags: your-registry/fastapi-app:${{ github.sha }}
  
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        uses: steebchen/kubectl@v2
        with:
          config: ${{ secrets.KUBE_CONFIG_DATA }}
          command: set image deployment/fastapi-app fastapi-app=your-registry/fastapi-app:${{ github.sha }} -n production
```

## Cost Optimization

1. **Right-sizing resources**:
   - Start with modest resource allocations
   - Scale based on actual usage patterns
   - Use spot instances for non-critical workloads

2. **Autoscaling**:
   - Scale down during low-traffic periods
   - Set appropriate minimum and maximum replica counts

## Implementation Roadmap

1. **Phase 1: Basic Production Setup**
   - Set up PostgreSQL database
   - Configure basic load balancing
   - Deploy multiple application instances

2. **Phase 2: Advanced Scaling**
   - Implement Kubernetes deployment
   - Configure autoscaling
   - Add connection pooling

3. **Phase 3: Monitoring and Observability**
   - Set up Prometheus and Grafana
   - Implement centralized logging
   - Configure alerts

4. **Phase 4: Optimizations**
   - Fine-tune performance
   - Implement caching strategies
   - Optimize database queries

This implementation roadmap allows for a gradual transition to a fully horizontally scalable architecture while maintaining application stability throughout the process.

## Conclusion

The current FastAPI template is already well-designed for horizontal scaling with its modular structure, support for PostgreSQL, and built-in resilience patterns. The main work will be in setting up the infrastructure and deployment configurations rather than making significant changes to the application code itself.
