# CENet Azure Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           INTERNET (Users)                           │
└────────────────┬────────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
    ┌────────────┐   ┌──────────────────────┐
    │  Frontend  │   │   Backend API Docs   │
    │   Web App  │   │   (Swagger UI)       │
    │            │   │                      │
    │  React +   │   │ https://cenet-      │
    │  Vite      │   │ backend.azurewebsites│
    │            │   │   .net/docs          │
    │ https://   │   └──────────────────────┘
    │ cenet-     │
    │ frontend.  │
    │azure       │
    │staticapps  │
    │ .net       │
    └─────┬──────┘
          │
          │ HTTP/REST
          │ (API calls)
          │
          ▼
    ┌──────────────────────────┐
    │   Backend API Server     │
    │   (FastAPI + Gunicorn)   │
    │                          │
    │  App Service (B2)        │
    │  - 2 cores               │
    │  - 4 GB RAM              │
    │  - Linux OS              │
    │                          │
    │  Listens on :8000        │
    │  https://cenet-backend   │
    │  .azurewebsites.net      │
    └─────┬──────────────────────┘
          │
          │ PostgreSQL Protocol
          │ (Database queries)
          │
          ▼
    ┌──────────────────────────────────┐
    │   Supabase PostgreSQL Database   │
    │                                  │
    │   - Managed PostgreSQL 15        │
    │   - Automatic backups            │
    │   - Row Level Security (RLS)     │
    │   - Connection pooling           │
    │                                  │
    │   postgres.supabase.co:5432      │
    └──────────────────────────────────┘
```

## Detailed Azure Resources

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Azure Subscription (West Europe)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Resource Group: cenet-rg                        │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────────────┐     │   │
│  │  │         App Service Plan: cenet-backend-plan       │     │   │
│  │  │                                                     │     │   │
│  │  │         SKU: B2 (2 cores, 3.5GB RAM)              │     │   │
│  │  │         OS: Linux                                  │     │   │
│  │  │         Region: West Europe                        │     │   │
│  │  └────────┬────────────────────────────────────────────┘     │   │
│  │           │                                                   │   │
│  │           │ Host                                              │   │
│  │           │                                                   │   │
│  │  ┌────────▼─────────────────────────────────────────────┐   │   │
│  │  │      App Service: cenet-backend                     │   │   │
│  │  │                                                      │   │   │
│  │  │  Runtime: Python 3.11 (Linux)                       │   │   │
│  │  │  App: FastAPI                                       │   │   │
│  │  │  Server: Gunicorn (4 workers)                       │   │   │
│  │  │  Port: 8000                                         │   │   │
│  │  │  URL: cenet-backend.azurewebsites.net             │   │   │
│  │  │                                                      │   │   │
│  │  │  Environment Variables:                             │   │   │
│  │  │  - DATABASE_URL (← Supabase)                        │   │   │
│  │  │  - SECRET_KEY (← Azure Key Vault)                   │   │   │
│  │  │  - SESSION_SECRET (← Azure Key Vault)               │   │   │
│  │  │  - FRONTEND_URL                                     │   │   │
│  │  │  - PYTHONPATH=/home/site/wwwroot                    │   │   │
│  │  │                                                      │   │   │
│  │  │  Git Deployment:                                    │   │   │
│  │  │  - Remote: azure (via Kudu)                         │   │   │
│  │  │  - Branch: main                                     │   │   │
│  │  │  - Build: Auto (pip install requirements.txt)       │   │   │
│  │  │                                                      │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Static Web App: cenet-frontend                  │  │   │
│  │  │                                                   │  │   │
│  │  │  Framework: React 19 + Vite                      │  │   │
│  │  │  Language: TypeScript                            │  │   │
│  │  │  CSS: Tailwind 4.0                               │  │   │
│  │  │  URL: cenet-frontend.azurestaticapps.net        │  │   │
│  │  │  Region: West US 2 (Static Apps constraint)      │  │   │
│  │  │                                                   │  │   │
│  │  │  Build:                                           │  │   │
│  │  │  - Trigger: Push to main (GitHub Actions)        │  │   │
│  │  │  - Command: npm run build                        │  │   │
│  │  │  - Output: dist/ folder                          │  │   │
│  │  │                                                   │  │   │
│  │  │  Environment Variables:                           │  │   │
│  │  │  - VITE_API_BASE_URL (← cenet-backend)           │  │   │
│  │  │                                                   │  │   │
│  │  │  Features:                                        │  │   │
│  │  │  - CDN (global distribution)                     │  │   │
│  │  │  - SSL/TLS (automatic)                           │  │   │
│  │  │  - SPA routing (handled via config)              │  │   │
│  │  │                                                   │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        External Services                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │             Supabase (PostgreSQL Hosting)                 │     │
│  │                                                            │     │
│  │  Project: CENet                                           │     │
│  │  Database: postgres                                       │     │
│  │  Host: xxx.postgres.supabase.co                          │     │
│  │  Port: 5432 (5432 for direct, 6543 for pooler)           │     │
│  │  Region: (select your preferred region)                  │     │
│  │                                                            │     │
│  │  Features:                                                │     │
│  │  - Automated backups                                      │     │
│  │  - Connection pooling                                     │     │
│  │  - Row Level Security                                     │     │
│  │  - Realtime subscriptions (optional)                      │     │
│  │                                                            │     │
│  │  Authentication:                                          │     │
│  │  - User: postgres                                         │     │
│  │  - Password: [securely stored]                            │     │
│  │                                                            │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │            GitHub (Source Code & CI/CD)                   │     │
│  │                                                            │     │
│  │  Repository: your-username/CENet                         │     │
│  │  Branch: main (default)                                   │     │
│  │                                                            │     │
│  │  Workflows:                                               │     │
│  │  - deploy-frontend.yml (triggers on frontend/ changes)    │     │
│  │    └─ Builds React app                                   │     │
│  │    └─ Deploys to Static Web Apps                         │     │
│  │                                                            │     │
│  │  Secrets:                                                 │     │
│  │  - AZURE_STATICWEB_APPS_API_TOKEN_CENET_FRONTEND        │     │
│  │  - VITE_API_BASE_URL                                     │     │
│  │                                                            │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User opens app
     │
     ▼
Browser requests: https://cenet-frontend.azurestaticapps.net
     │
     ├─ Azure CDN serves static files (HTML, JS, CSS)
     ▼
React app loads in browser
     │
     │ User interacts with app
     │ (clicks button, submits form, etc.)
     │
     ▼
Frontend makes API request:
     │ fetch('https://cenet-backend.azurewebsites.net/api/endpoint')
     │
     ├─ HTTPS (encrypted)
     ├─ CORS headers validated
     ├─ Auth token included (if needed)
     │
     ▼
Backend receives request at:
     │ GET /api/endpoint
     │
     ├─ FastAPI routes to handler
     ├─ Authentication verified
     ├─ Permission checks
     │
     ▼
Handler processes request:
     │
     ├─ Fetch data from Supabase database
     │   └─ Execute SQL query
     │   └─ Return results
     │
     ├─ Transform data (if needed)
     ├─ Apply business logic
     │
     ▼
Return response to Frontend
     │ 200 OK
     │ Content-Type: application/json
     │ Body: {...}
     │
     ▼
Frontend receives response
     │
     ├─ Parse JSON
     ├─ Update React state
     ├─ Re-render components
     │
     ▼
User sees updated UI
```

## Network Flow

```
┌──────────────┐         ┌─────────────────────────────────┐
│              │         │      Internet / Azure CDN        │
│    User      │         │  (All traffic encrypted HTTPS)   │
│              │         │                                  │
└──────┬───────┘         └────────────────────┬─────────────┘
       │                                      │
       │                    ┌─────────────────┘
       │                    │
       ├─ HTTPS ────────────┤
       │ (port 443)         │
       │                    ▼
       │              Static Web App
       │              (Cloudflare CDN)
       │              ├─ index.html
       │              ├─ main.js
       │              ├─ styles.css
       │              └─ (+ other assets)
       │
       │              React app runs
       │              ├─ User clicks button
       │              ├─ Makes API request
       │
       │              FETCH /api/...
       │
       └─ HTTPS ────────────┐
         (port 443)         │
                            ▼
                      App Service
                      ├─ FastAPI
                      ├─ Receives request
                      ├─ Validates auth
                      └─ Queries database
                            │
                            │ postgresql://
                            │ port 5432 or 6543
                            │
                            ▼
                      Supabase
                      PostgreSQL
                      ├─ Execute query
                      ├─ Fetch results
                      └─ Return to app
                            │
                            │ Results
                            │
                            ▼
                      App Service
                      ├─ Format response
                      └─ Return JSON
                            │
                            │ JSON response
                            │
                            ▼
                      Frontend
                      ├─ Parse JSON
                      ├─ Update state
                      └─ Re-render
                            │
                            │ Updated UI
                            ▼
                      User sees result
```

## Deployment Pipeline

```
Developer pushes code to GitHub
        │
        ├─────────────────────────────────┐
        │                                 │
        │                          Commit to main
        │                                 │
        ├─ Backend (backend/)      GitHub Actions triggers
        │  ├─ git subtree push     ├─ Build: npm install + npm run build
        │  │                       ├─ Test: npm run lint
        │  │                       ├─ Deploy: Azure Static Web Apps
        │  └─ Azure Git remote     └─ Time: 2-5 minutes
        │     ├─ Kudu service
        │     ├─ Install deps
        │     ├─ Start gunicorn    Frontend (frontend/)
        │     └─ Port: 8000        ├─ Compiled dist/
        │                          ├─ Uploaded to CDN
        │                          └─ Cache invalidated
        │
        └─ Azure App Service
           ├─ Health check
           ├─ Start/restart
           └─ Ready to serve
```

## Security Architecture

```
┌────────────────────────────────────────────────────────┐
│              Security Layers                            │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: Transport Security                          │
│  ├─ HTTPS (TLS 1.2+)                                  │
│  ├─ Certificates: Auto-managed by Azure               │
│  └─ All traffic encrypted end-to-end                  │
│                                                         │
│  Layer 2: Application Security                        │
│  ├─ CORS (Cross-Origin Resource Sharing)              │
│  │  ├─ Frontend origin whitelisted                    │
│  │  └─ Prevents unauthorized requests                │
│  ├─ JWT tokens for authentication                     │
│  └─ Session management                                │
│                                                         │
│  Layer 3: Database Security                           │
│  ├─ Connection pooling (Supabase)                     │
│  ├─ Role-based access control (RLS)                   │
│  ├─ Parameterized queries (SQLAlchemy ORM)            │
│  └─ Prevents SQL injection                            │
│                                                         │
│  Layer 4: Infrastructure Security                     │
│  ├─ Resource Group isolation                          │
│  ├─ Network security (Azure NSGs)                     │
│  ├─ Access control (RBAC)                             │
│  └─ Managed by Azure                                  │
│                                                         │
│  Layer 5: Secret Management                           │
│  ├─ Environment variables (not in code)               │
│  ├─ GitHub Secrets for CI/CD tokens                   │
│  └─ Consider: Azure Key Vault (advanced)              │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Scaling Considerations

```
Current Setup (B2 App Service)
├─ 2 CPU cores
├─ 3.5 GB RAM
├─ Max ~1000 concurrent connections
└─ Supports ~100-500 simultaneous users

Scaling Path
│
├─ Single requests slow?
│  └─ Check database query performance
│
├─ High CPU usage?
│  ├─ Upgrade to B3 (3 cores, €75/month)
│  └─ Or optimize code
│
├─ High memory usage?
│  ├─ Reduce worker processes in Gunicorn
│  └─ Or upgrade tier
│
├─ Many users needed?
│  ├─ Switch to S1 tier (€65/month, auto-scaling)
│  ├─ Add Application Insights
│  └─ Consider Load Balancer
│
└─ Database bottleneck?
    ├─ Upgrade Supabase plan
    ├─ Add read replicas
    ├─ Implement caching (Redis)
    └─ Optimize queries
```

---

**This architecture is:**
- ✅ Scalable (can handle growing user base)
- ✅ Reliable (managed services with SLAs)
- ✅ Secure (HTTPS, authentication, RLS)
- ✅ Cost-effective (pay for what you use)
- ✅ Easy to maintain (minimal infrastructure management)

See [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) to get this deployed!
