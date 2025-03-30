# Security Best Practices

This document outlines security best practices for deploying and maintaining your FastAPI application in production environments.

## IP Blacklisting Strategies

When implementing IP blacklisting for your application, you have options at both the load balancer level and the API level. Each approach has its own advantages and use cases.

### Load Balancer Level IP Blacklisting

**Advantages:**
- More efficient as rejected traffic is blocked before reaching your application servers
- Reduces unnecessary load on your application
- Centralized management across all your application instances
- Usually better performance for handling network-level rules

**Disadvantages:**
- Less flexibility for complex rules that might depend on application context
- Changes might require infrastructure modifications (potential deployment delays)
- May lack detailed logging of rejected requests

**Implementation Example (AWS ALB):**
```json
{
  "Rules": [
    {
      "Priority": 1,
      "Conditions": [
        {
          "Field": "ip-address",
          "IpAddressConfig": {
            "Values": ["203.0.113.0/24", "198.51.100.1"]
          }
        }
      ],
      "Actions": [
        {
          "Type": "fixed-response",
          "FixedResponseConfig": {
            "StatusCode": "403",
            "ContentType": "text/plain",
            "MessageBody": "Access denied"
          }
        }
      ]
    }
  ]
}
```

**Implementation Example (Nginx):**
```nginx
http {
    # Define a blacklist
    geo $blacklist {
        default 0;
        192.168.1.1/32 1;
        203.0.113.0/24 1;
    }

    server {
        listen 80;
        server_name example.com;

        # Block blacklisted IPs
        if ($blacklist) {
            return 403 "Access denied";
        }

        location / {
            proxy_pass http://backend;
        }
    }
}
```

### API Level IP Blacklisting

**Advantages:**
- More granular control with application context (e.g., block by IP + endpoint combination)
- Easier to implement dynamic blocking rules
- Better visibility with detailed logging
- Can be updated without infrastructure changes

**Disadvantages:**
- Consumes application resources as the request reaches your application before being rejected
- Must be implemented across all instances
- Additional processing overhead

**Implementation Example (FastAPI Middleware):**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# IP blacklist (could be loaded from a database or environment variable)
BLACKLISTED_IPS = {"203.0.113.1", "198.51.100.1"}

@app.middleware("http")
async def ip_blacklist_middleware(request: Request, call_next):
    client_ip = request.client.host
    # Check if IP is blacklisted
    if client_ip in BLACKLISTED_IPS:
        return JSONResponse(
            status_code=403,
            content={"detail": "Access denied from this IP address"}
        )
    return await call_next(request)
```

**Dynamic Blacklisting Example:**
```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.blacklist import IPBlacklist

app = FastAPI()

async def is_ip_blacklisted(client_ip: str, db: Session):
    """Check if IP is blacklisted in the database"""
    blacklisted = db.query(IPBlacklist).filter(
        IPBlacklist.ip_address == client_ip,
        IPBlacklist.is_active == True
    ).first()
    return blacklisted is not None

@app.middleware("http")
async def ip_blacklist_middleware(request: Request, call_next):
    client_ip = request.client.host
    
    # Get DB connection
    db = next(get_db())
    
    # Check if IP is blacklisted
    if await is_ip_blacklisted(client_ip, db):
        # Log the blocked request
        print(f"Blocked request from blacklisted IP: {client_ip}")
        return JSONResponse(
            status_code=403,
            content={"detail": "Access denied from this IP address"}
        )
    
    return await call_next(request)
```

### Best Practice Recommendation

**Implement at both levels with different responsibilities:**

1. **Load Balancer Level:**
   - Block known malicious IPs
   - Block entire IP ranges from untrusted regions
   - Implement rate limiting for basic DDoS protection

2. **API Level:**
   - Implement more sophisticated rules
   - Handle temporary bans based on application behavior
   - Provide detailed rejection responses and logging

## Additional Security Measures

### Rate Limiting

Implement rate limiting to prevent abuse:

```python
from fastapi import FastAPI, Request
import time
from collections import defaultdict

app = FastAPI()

# Simple in-memory rate limiting (use Redis for production)
request_counts = defaultdict(list)
RATE_LIMIT = 10  # requests
TIME_WINDOW = 60  # seconds

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Remove old requests
    request_counts[client_ip] = [t for t in request_counts[client_ip] 
                               if current_time - t < TIME_WINDOW]
    
    # Check if rate limit exceeded
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    
    # Add current request timestamp
    request_counts[client_ip].append(current_time)
    
    return await call_next(request)
```

### Authentication Protection

Implement protections against brute force authentication attempts:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Track failed login attempts
failed_attempts = defaultdict(list)
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    current_time = datetime.now()
    
    # Remove old failed attempts
    failed_attempts[username] = [t for t in failed_attempts[username] 
                                if current_time - t < LOCKOUT_DURATION]
    
    # Check if account is locked
    if len(failed_attempts[username]) >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to multiple failed login attempts"
        )
    
    # Authenticate user
    user = authenticate_user(db, username, form_data.password)
    if not user:
        # Track failed attempt
        failed_attempts[username].append(current_time)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Clear failed attempts on successful login
    failed_attempts[username] = []
    
    # Generate token...
```

## Secure Headers

Implement secure headers to protect against common web vulnerabilities:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

## Security Checklist

- ✅ Implement IP blacklisting (load balancer and/or API level)
- ✅ Enable rate limiting
- ✅ Set up brute force protection
- ✅ Use HTTPS in production
- ✅ Implement secure headers
- ✅ Validate all input data (handled by Pydantic in FastAPI)
- ✅ Use parameterized queries (handled by SQLAlchemy)
- ✅ Set proper CORS policies
- ✅ Keep dependencies updated
- ✅ Enable security monitoring and logging
- ✅ Implement proper authentication and authorization
- ✅ Use secure password hashing (already included in the template)
