# Deployment Specifications for Course Companion FTE

## Overview
The Course Companion FTE deployment strategy ensures a robust, scalable, and secure production environment. The deployment process follows DevOps best practices with automated pipelines, comprehensive monitoring, and disaster recovery procedures.

## Deployment Architecture

### Production Environment Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Load Balancer Layer                          │
│  (Traffic Distribution, SSL Termination, Health Checks)       │
├─────────────────────────────────────────────────────────────────┤
│                    CDN Layer                                  │
│        (Static Asset Caching, Global Distribution)           │
├─────────────────────────────────────────────────────────────────┤
│                    Application Layer                          │
│         (Multiple Server Instances, Auto-Scaling)             │
├─────────────────────────────────────────────────────────────────┤
│                    Database Layer                             │
│           (Managed PostgreSQL, Read Replicas)                │
├─────────────────────────────────────────────────────────────────┤
│                    Storage Layer                              │
│         (Cloudflare R2, File Upload Handling)               │
├─────────────────────────────────────────────────────────────────┤
│                    Monitoring Layer                           │
│        (Logging, Metrics, Alerting, Health Checks)          │
└─────────────────────────────────────────────────────────────────┘
```

### Infrastructure Components
- **Compute**: Containerized applications with auto-scaling
- **Database**: Managed PostgreSQL with automated backups
- **Storage**: Cloudflare R2 for static assets
- **CDN**: Cloudflare for global content delivery
- **Monitoring**: Application Performance Monitoring (APM)
- **Security**: WAF, DDoS protection, SSL certificates

## Environment Specifications

### Development Environment
- **Location**: Local developer machines
- **Database**: SQLite for simplicity
- **Frontend**: Hot reloading development server
- **Backend**: Auto-restarting development server
- **Domain**: localhost:3000 (frontend), localhost:8000 (backend)

### Staging Environment
- **Location**: Cloud-based staging environment
- **Database**: PostgreSQL (same as production)
- **Scale**: Single instance, representative of production
- **Domain**: staging.coursecompanionfte.com
- **Access**: Limited to development team
- **Purpose**: Pre-production testing and validation

### Production Environment
- **Location**: Production cloud infrastructure
- **Database**: Managed PostgreSQL with replication
- **Scale**: Auto-scaling cluster with load balancing
- **Domain**: www.coursecompanionfte.com
- **Access**: Public access
- **SLA**: 99.9% uptime guarantee

## Infrastructure Requirements

### Compute Resources
- **Frontend Servers**:
  - Minimum: 2 instances (high availability)
  - Recommended: 4 instances (auto-scaling)
  - CPU: 2-4 cores per instance
  - RAM: 4-8 GB per instance
  - Storage: SSD, 50-100 GB

- **Backend Servers**:
  - Minimum: 2 instances (high availability)
  - Recommended: 4-8 instances (auto-scaling)
  - CPU: 4-8 cores per instance
  - RAM: 8-16 GB per instance
  - Storage: SSD, 100-200 GB

### Database Requirements
- **Type**: PostgreSQL 13+
- **Storage**: SSD with provisioned IOPS
- **RAM**: 8-16 GB for buffer pool
- **CPU**: 4-8 cores for query processing
- **Backup**: Automated daily backups with point-in-time recovery
- **Replication**: Read replicas for scaling read operations

### Network Requirements
- **Bandwidth**: 100 Mbps minimum, 1 Gbps recommended
- **Latency**: < 50ms for API responses
- **CDN**: Global edge network for content delivery
- **Security**: WAF and DDoS protection

## Deployment Process

### CI/CD Pipeline
```
Code Commit → Build → Test → Staging Deploy → Staging Test → Production Deploy → Monitoring
```

### Deployment Steps
1. **Code Validation**
   - Static analysis and linting
   - Unit and integration tests
   - Security scanning
   - Code coverage validation

2. **Build Process**
   - Frontend bundle optimization
   - Backend container image creation
   - Dependency vulnerability scanning
   - Artifact signing

3. **Staging Deployment**
   - Blue-green deployment to staging
   - Automated integration tests
   - Performance validation
   - Manual QA validation

4. **Production Deployment**
   - Canary deployment (10% traffic)
   - Health monitoring for 10 minutes
   - Gradual rollout (50%, 100%)
   - Post-deployment validation

## Containerization Strategy

### Docker Configuration

#### Backend Container
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Container
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Container Orchestration (Kubernetes)
```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 4
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: course-companion-fe:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: NEXT_PUBLIC_API_BASE_URL
          value: "https://api.coursecompanionfte.com"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Environment Configuration

### Environment Variables

#### Production Environment Variables
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@prod-db.cluster.region.rds.amazonaws.com:5432/course_companion
DATABASE_POOL_SIZE=20
DATABASE_ECHO=false

# Authentication
SECRET_KEY=super_secret_production_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# External Services
CLOUDFLARE_R2_ENDPOINT=https://pub-xxx.r2.dev
CHATGPT_API_KEY=sk-production-key-here
SENTRY_DSN=https://sentry.example.com/project

# Application Settings
LOG_LEVEL=INFO
DEBUG=false
ALLOWED_HOSTS=coursecompanionfte.com,www.coursecompanionfte.com
CORS_ORIGINS=https://coursecompanionfte.com,https://www.coursecompanionfte.com

# Performance
WORKERS_PER_CORE=2
MAX_WORKERS=8
WEB_CONCURRENCY=8
```

#### Staging Environment Variables
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@staging-db.cluster.region.rds.amazonaws.com:5432/course_companion
DATABASE_POOL_SIZE=10
DATABASE_ECHO=false

# Authentication
SECRET_KEY=staging_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# External Services
CLOUDFLARE_R2_ENDPOINT=https://pub-yyy.r2.dev
CHATGPT_API_KEY=sk-staging-key-here

# Application Settings
LOG_LEVEL=INFO
DEBUG=true
ALLOWED_HOSTS=staging.coursecompanionfte.com
CORS_ORIGINS=https://staging.coursecompanionfte.com

# Performance
WORKERS_PER_CORE=1
MAX_WORKERS=4
WEB_CONCURRENCY=4
```

## Monitoring and Observability

### Application Monitoring
- **APM Tool**: Datadog/New Relic for application performance
- **Custom Metrics**: Course completion rates, quiz performance
- **Error Tracking**: Sentry for error monitoring
- **Business Metrics**: User engagement, feature usage

### Infrastructure Monitoring
- **System Metrics**: CPU, memory, disk, network
- **Database Metrics**: Query performance, connection pools
- **Application Metrics**: Response times, throughput, error rates
- **Business Metrics**: User registrations, course enrollments

### Logging Strategy
```python
# Logging configuration for production
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s - %(duration)s",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

### Health Checks

#### Backend Health Check
```python
@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancer and monitoring
    """
    import asyncio
    import time

    start_time = time.time()

    # Check database connectivity
    try:
        db_status = await check_database_connection()
    except Exception as e:
        return {"status": "error", "error": "database_unreachable", "timestamp": time.time()}

    # Check external services
    try:
        external_services_status = await check_external_services()
    except Exception as e:
        return {"status": "degraded", "warning": "external_service_issues", "timestamp": time.time()}

    response_time = (time.time() - start_time) * 1000

    return {
        "status": "healthy",
        "response_time_ms": round(response_time, 2),
        "database": db_status,
        "external_services": external_services_status,
        "timestamp": time.time(),
        "version": "1.0.0"
    }
```

#### Frontend Health Check
```javascript
// Health check for frontend
export async function checkHealth() {
  try {
    const response = await fetch('/api/health');
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}
```

## Security Configuration

### SSL/TLS Configuration
- **Certificate Authority**: Let's Encrypt or managed certificates
- **Protocol Versions**: TLS 1.2 and 1.3 only
- **Cipher Suites**: Modern, secure cipher suites
- **HSTS**: Strict transport security enabled

### Firewall Rules
- **Inbound**: HTTPS (443), SSH (22 for admin access)
- **Outbound**: Required external services only
- **Database**: Private network access only
- **Admin Access**: IP-restricted access

### Security Headers
```python
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware

# Security headers
security_headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
```

## Backup and Disaster Recovery

### Database Backup Strategy
- **Frequency**: Daily automated backups
- **Retention**: 30 days of daily backups, weekly for 6 months
- **Point-in-Time Recovery**: Available for last 7 days
- **Offsite Storage**: Encrypted backups stored separately

### Application Backup
- **Configuration**: Version-controlled configuration files
- **Images**: Container images stored in registry
- **Static Assets**: Cloud storage redundancy
- **Database Dumps**: Automated exports

### Disaster Recovery Plan
1. **Detection**: Automated monitoring alerts
2. **Assessment**: Impact evaluation
3. **Recovery**: Automated failover procedures
4. **Verification**: Service restoration validation
5. **Communication**: Stakeholder notification

## Performance Optimization

### Caching Strategy
```python
# Redis configuration for caching
from redis import Redis
import pickle
from functools import wraps

redis_client = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0,
    decode_responses=False
)

def cache_result(expire_seconds=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return pickle.loads(cached_result)

            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_seconds, pickle.dumps(result))
            return result
        return wrapper
    return decorator
```

### CDN Configuration
- **Static Assets**: Images, CSS, JavaScript files
- **Geographic Distribution**: Global edge locations
- **Compression**: Automatic gzip/brotli compression
- **Invalidation**: Automated cache invalidation

### Database Optimization
- **Connection Pooling**: SQLAlchemy connection pooling
- **Query Optimization**: Index optimization and query analysis
- **Read Replicas**: Separate read operations
- **Caching**: Redis for frequently accessed data

## Rollback Procedures

### Automated Rollback Conditions
- **Health Check Failures**: Consecutive health check failures
- **Error Rate Spikes**: Error rate exceeding threshold
- **Performance Degradation**: Response time degradation
- **Manual Trigger**: Operator initiated rollback

### Rollback Process
1. **Detection**: Automated or manual trigger
2. **Verification**: Current deployment issues confirmed
3. **Reversion**: Deploy previous stable version
4. **Validation**: Health checks and monitoring
5. **Notification**: Stakeholder communication

## Deployment Scripts

### Production Deployment Script
```bash
#!/bin/bash
# deploy-production.sh

set -e

echo "Starting production deployment..."

# Validate environment
if [ "$ENVIRONMENT" != "production" ]; then
    echo "Error: This script is for production deployment only"
    exit 1
fi

# Backup current version
echo "Creating backup of current version..."
kubectl get all -o yaml > backup-$(date +%Y%m%d-%H%M%S).yaml

# Update frontend
echo "Deploying frontend..."
kubectl set image deployment/frontend frontend=course-companion-fe:v$(git rev-parse --short HEAD)
kubectl rollout status deployment/frontend

# Update backend
echo "Deploying backend..."
kubectl set image deployment/backend backend=course-companion-be:v$(git rev-parse --short HEAD)
kubectl rollout status deployment/backend

# Run post-deployment tests
echo "Running post-deployment tests..."
python run-smoke-tests.py

# Verify health
echo "Verifying application health..."
sleep 30
curl -f https://www.coursecompanionfte.com/health || { echo "Health check failed"; exit 1; }

echo "Production deployment completed successfully!"
```

### Staging Deployment Script
```bash
#!/bin/bash
# deploy-staging.sh

set -e

echo "Starting staging deployment..."

# Validate environment
if [ "$ENVIRONMENT" != "staging" ]; then
    echo "Error: This script is for staging deployment only"
    exit 1
fi

# Deploy frontend
echo "Deploying frontend to staging..."
kubectl set image deployment/frontend-staging frontend=course-companion-fe:staging-$(git rev-parse --short HEAD)

# Deploy backend
echo "Deploying backend to staging..."
kubectl set image deployment/backend-staging backend=course-companion-be:staging-$(git rev-parse --short HEAD)

# Wait for rollout
kubectl rollout status deployment/frontend-staging
kubectl rollout status deployment/backend-staging

echo "Staging deployment completed successfully!"
```

## Maintenance Windows

### Scheduled Maintenance
- **Frequency**: Monthly maintenance windows
- **Duration**: 2-hour maintenance window
- **Timing**: Sunday 02:00-04:00 UTC
- **Communication**: 48-hour advance notice

### Emergency Maintenance
- **Process**: Immediate response procedures
- **Escalation**: On-call engineer notification
- **Communication**: Real-time status updates
- **Documentation**: Post-incident analysis

## Cost Optimization

### Resource Optimization
- **Auto-scaling**: Scale based on demand
- **Reserved Instances**: Cost savings for steady-state workloads
- **Spot Instances**: For non-critical batch jobs
- **Right-sizing**: Regular resource optimization reviews

### Monitoring Costs
- **Resource Utilization**: Track resource usage
- **Cost Alerts**: Budget threshold notifications
- **Optimization Reports**: Monthly cost analysis
- **ROI Tracking**: Business value measurement

## Compliance and Governance

### Security Compliance
- **SOC 2**: Type II compliance for data security
- **GDPR**: Data privacy and protection compliance
- **PCI DSS**: Payment card industry standards (if applicable)
- **Audit Trails**: Comprehensive logging and monitoring

### Change Management
- **Approval Process**: Required approvals for changes
- **Documentation**: Change request documentation
- **Testing**: Mandatory testing for changes
- **Rollback Plans**: Prepared rollback procedures

This deployment specification ensures the Course Companion FTE system is deployed securely, scalably, and reliably in production environments.