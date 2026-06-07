# CENet Azure + Supabase Deployment Guide

This guide walks you through deploying the CENet monorepo to Azure with Supabase as the database.

## Prerequisites

- ✅ Azure CLI logged in (`az account show` to verify)
- ✅ Supabase project created with connection string
- ✅ Git repository with clean working tree

## Step 1: Prepare Environment Variables

### Backend Configuration

Create `.env` files for deployment:

**backend/.env** (for local testing before deployment)
```bash
# Database (replace with your Supabase connection string)
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]

# Security - Generate strong secrets
SECRET_KEY=$(openssl rand -hex 32)
SESSION_SECRET=$(openssl rand -hex 32)

# Frontend URL (will update after frontend deployment)
FRONTEND_URL=https://your-static-web-app.azurestaticapps.net

# OAuth (optional - add if you have OAuth providers configured)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

**frontend/.env** (for deployment)
```bash
# Will be set via Static Web Apps environment
VITE_API_BASE_URL=https://your-backend-app.azurewebsites.net
```

## Step 2: Create Azure Resources

### 2a. Resource Group

```bash
# Create resource group
az group create \
  --name cenet-rg \
  --location eastus

# Verify
az group show --name cenet-rg
```

### 2b. Backend - App Service for FastAPI

```bash
# Create App Service Plan (B1 = budget-friendly, B2 = better performance)
az appservice plan create \
  --name cenet-backend-plan \
  --resource-group cenet-rg \
  --sku B2 \
  --is-linux

# Create App Service (Python 3.11)
az webapp create \
  --name cenet-backend-app \
  --resource-group cenet-rg \
  --plan cenet-backend-plan \
  --runtime "PYTHON:3.11"

# Get the app URL
az webapp show \
  --name cenet-backend-app \
  --resource-group cenet-rg \
  --query defaultHostName
```

### 2c. Frontend - Static Web App

```bash
# Create Static Web App (must use eastus or westus2)
az staticwebapp create \
  --name cenet-frontend-app \
  --resource-group cenet-rg \
  --location eastus \
  --source https://github.com/YOUR_USERNAME/CENet \
  --branch main \
  --app-location "frontend" \
  --output-location "dist" \
  --app-build-command "npm install && npm run build" \
  --token YOUR_GITHUB_PAT

# Get the app URL
az staticwebapp show \
  --name cenet-frontend-app \
  --resource-group cenet-rg \
  --query "defaultHostname"
```

> **Note:** Generate a GitHub Personal Access Token (PAT) with `repo` and `workflow` scopes for the Static Web App integration.

## Step 3: Configure Backend App Service

### 3a. Set Environment Variables

```bash
# Set app settings in App Service
az webapp config appsettings set \
  --name cenet-backend-app \
  --resource-group cenet-rg \
  --settings \
    DATABASE_URL="postgresql://[user]:[password]@[host]:[port]/[database]" \
    SECRET_KEY="$(openssl rand -hex 32)" \
    SESSION_SECRET="$(openssl rand -hex 32)" \
    FRONTEND_URL="https://cenet-frontend-app.azurestaticapps.net" \
    PYTHONPATH="/home/site/wwwroot" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Verify settings
az webapp config appsettings list \
  --name cenet-backend-app \
  --resource-group cenet-rg
```

### 3b. Configure Python Environment

```bash
# Set Python version and startup command
az webapp config set \
  --name cenet-backend-app \
  --resource-group cenet-rg \
  --startup-file "gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

# Enable SCM (needed for Git deployment)
az webapp deployment source config-local-git \
  --name cenet-backend-app \
  --resource-group cenet-rg
```

### 3c. Deploy Backend with Git

```bash
# Get Git deployment URL
GIT_URL=$(az webapp deployment source config-local-git \
  --name cenet-backend-app \
  --resource-group cenet-rg \
  --query url \
  --output tsv)

echo "Git remote: $GIT_URL"

# Add Azure Git remote to your repo
git remote add azure "$GIT_URL"

# Deploy backend (push just the backend folder)
git subtree push --prefix backend azure main
```

### 3d. Install Python Dependencies on Azure

Create `requirements.txt` deployment trigger:

```bash
# SSH into the app to install dependencies
az webapp ssh --name cenet-backend-app --resource-group cenet-rg

# Inside the SSH session:
cd /home/site/wwwroot
pip install -r requirements.txt
python -m alembic upgrade head  # if using migrations
```

Or use an Azure Deployment slot startup script:

Create `backend/startup.sh`:
```bash
#!/bin/bash
pip install --no-cache-dir -r requirements.txt
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
```

## Step 4: Configure Frontend Static Web App

### 4a. Set Environment Variables

```bash
# Add environment variables to Static Web App
az staticwebapp appsettings set \
  --name cenet-frontend-app \
  --resource-group cenet-rg \
  --setting-names \
    VITE_API_BASE_URL="https://cenet-backend-app.azurewebsites.net"
```

### 4b. Verify GitHub Actions Workflow

Azure Static Web Apps auto-creates a GitHub Actions workflow. Verify it's set up:
1. Go to `.github/workflows/` in your repo
2. Look for `azure-static-web-apps-*.yml`
3. Workflow should build and deploy on push to `main`

## Step 5: Enable CORS on Backend

Update `backend/main.py` to allow your frontend origin:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",      # Local dev
    "http://localhost:3000",       # Alt local dev
    "https://cenet-frontend-app.azurestaticapps.net",  # Production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 6: Test Deployment

### 6a. Test Backend

```bash
# Get backend URL
BACKEND_URL="https://cenet-backend-app.azurewebsites.net"

# Test health
curl "$BACKEND_URL/docs"

# Check logs
az webapp log stream --name cenet-backend-app --resource-group cenet-rg
```

### 6b. Test Frontend

Navigate to: `https://cenet-frontend-app.azurestaticapps.net`

Open browser DevTools console and verify:
- No CORS errors
- API calls to backend succeed
- Frontend loads and communicates with API

## Step 7: Database Initialization (if needed)

If you need to run migrations or initialize tables:

```bash
# SSH into backend app
az webapp ssh --name cenet-backend-app --resource-group cenet-rg

# Run migrations or setup scripts
python -m alembic upgrade head
# or
python scripts/init_db.py
```

## Monitoring & Logs

```bash
# View real-time backend logs
az webapp log stream --name cenet-backend-app --resource-group cenet-rg

# View Static Web App logs
az staticwebapp logs --name cenet-frontend-app --resource-group cenet-rg

# Check App Service health
az webapp show --name cenet-backend-app --resource-group cenet-rg
```

## Troubleshooting

### Backend returns 500 errors
```bash
# Check logs
az webapp log stream --name cenet-backend-app --resource-group cenet-rg

# SSH and test locally
az webapp ssh --name cenet-backend-app --resource-group cenet-rg
python -c "from database import engine; print(engine.url)"
```

### CORS errors on frontend
- Verify `FRONTEND_URL` is set in backend app settings
- Update `CORS` origins in `backend/main.py`
- Restart app: `az webapp restart --name cenet-backend-app --resource-group cenet-rg`

### Database connection issues
- Verify Supabase connection string is correct
- Check Supabase firewall allows Azure IP ranges
- Ensure `DATABASE_URL` env var is set

## Cleanup (if needed)

```bash
# Delete everything
az group delete --name cenet-rg --yes
```

## Next Steps

1. Set up custom domain names
2. Configure SSL/TLS certificates
3. Set up monitoring/alerts with Azure Monitor
4. Configure auto-scaling rules
5. Set up CI/CD pipelines for automatic deployments
