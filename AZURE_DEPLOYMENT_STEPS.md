# Azure Deployment - Step-by-Step Instructions

This guide walks through deploying CENet to Azure with Supabase. Follow each step in order.

## Phase 1: Prerequisites & Setup

### Step 1: Verify Azure CLI is installed and you're logged in

```powershell
# Check Azure CLI version
az --version

# You should see output like: azure-cli 2.xx.x

# Verify you're logged in
az account show

# If not logged in:
az login
```

### Step 2: Get your Supabase PostgreSQL Connection String

1. Go to [supabase.com](https://supabase.com)
2. Select your project
3. Go to **Settings** → **Database**
4. Under **Connection string**, click the **POSTGRESQL** tab
5. Copy the full connection string (it will look like):
   ```
   postgresql://postgres.xxxx:[PASSWORD]@xxxx.postgres.supabase.co:5432/postgres
   ```
6. Replace `[PASSWORD]` with your actual database password (from Supabase dashboard)
7. **Save this value**, we'll use it in Step 3

### Step 3: Prepare Environment Variables

Create `.env` file in the backend folder with your Supabase credentials:

**File: `backend/.env`**
```bash
DATABASE_URL=postgresql://postgres.xxxx:[PASSWORD]@xxxx.postgres.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-change-me
SESSION_SECRET=your-session-secret-change-me
FRONTEND_URL=http://localhost:5173
PYTHON_PATH=/home/site/wwwroot
```

> To generate secure secrets on Windows PowerShell:
> ```powershell
> [System.Convert]::ToBase64String([System.Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes(32))
> ```

## Phase 2: Create Azure Resources

### Step 4: Create Resource Group

```powershell
# Set variables
$ResourceGroup = "cenet-rg"
$Location = "westeurope"

# Create resource group
az group create `
  --name $ResourceGroup `
  --location $Location

# Verify
az group show --name $ResourceGroup
```

Expected output: Shows resource group in westeurope region.

### Step 5: Create App Service Plan (for backend)

```powershell
$BackendPlan = "cenet-backend-plan"

az appservice plan create `
  --name $BackendPlan `
  --resource-group $ResourceGroup `
  --sku F1 `
  --is-linux

# Verify
az appservice plan show --name $BackendPlan --resource-group $ResourceGroup
```

**Explanation:**
- **F1**: Free tier. Sufficient for 1-5 test users. App sleeps after 20 min inactivity (~30s cold start on next request).
- **--is-linux**: Python requires Linux runtime

### Step 6: Create App Service (for FastAPI backend)

```powershell
$BackendApp = "cenet-backend"

az webapp create `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --plan $BackendPlan `
  --runtime "PYTHON:3.11"

# Get the URL
$BackendUrl = az webapp show `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --query defaultHostName `
  --output tsv

Write-Host "Backend URL: https://$BackendUrl"
```

Expected: Shows `cenet-backend.azurewebsites.net`

## Phase 3: Configure Backend App Service

### Step 7: Set Application Settings

```powershell
# Read your Supabase connection string
$DatabaseUrl = "postgresql://postgres.xxxx:[PASSWORD]@xxxx.postgres.supabase.co:5432/postgres"
$SecretKey = "your-generated-secret-key"
$SessionSecret = "your-generated-session-secret"

# Set all environment variables
az webapp config appsettings set `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --settings `
    DATABASE_URL="$DatabaseUrl" `
    SECRET_KEY="$SecretKey" `
    SESSION_SECRET="$SessionSecret" `
    FRONTEND_URL="https://cenet-frontend.azurestaticapps.net" `
    PYTHONPATH="/home/site/wwwroot" `
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
    PYTHON_VERSION="3.11"

# Verify settings were saved
az webapp config appsettings list `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --output table
```

### Step 8: Configure Startup Command

```powershell
az webapp config set `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --startup-file "gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

# Verify
az webapp config show `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --query appCommandLine
```

Expected: Shows the gunicorn command

### Step 9: Enable Git Deployment

```powershell
# Get the Git deployment URL
$GitUrl = az webapp deployment source config-local-git `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --query url `
  --output tsv

Write-Host "Git URL: $GitUrl"
Write-Host "Save this URL! You'll need it next."
```

## Phase 4: Deploy Backend Code

### Step 10: Add Azure as Git Remote

```powershell
# Navigate to your repo root
cd c:\Repos\CENet\webapp

# Add Azure remote
# Replace {GIT_URL} with the URL from Step 9
git remote add azure "{GIT_URL}"

# Verify
git remote -v
# Should show both "origin" and "azure"
```

### Step 11: Deploy Backend Code

```powershell
# This pushes only the backend/ folder to Azure
# The backend/ code becomes the app root
git subtree push --prefix backend azure main

# This will:
# 1. Build the app on Azure (install pip requirements)
# 2. Start the Gunicorn server
# 3. May take 2-5 minutes
```

### Step 12: Monitor Deployment

While deployment runs, monitor logs:

```powershell
# Watch logs in real-time
az webapp log stream `
  --name $BackendApp `
  --resource-group $ResourceGroup

# In another terminal, you can also check status
az webapp deployment list `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --output table
```

**What to look for:**
- ✅ `Successfully installed pip requirements`
- ✅ `Starting gunicorn...`
- ✅ `Application started successfully`

**If there are errors:**
- Check the DATABASE_URL format is correct
- Verify Supabase firewall allows Azure IPs
- Check app settings were saved correctly

### Step 13: Test Backend API

```powershell
# Once deployment completes, test the API
$BackendUrl = "https://$BackendApp.azurewebsites.net"

# Test health check
Invoke-WebRequest "$BackendUrl/docs" -UseBasicParsing
# Should return 200 and show Swagger UI

# Or open in browser: https://cenet-backend.azurewebsites.net/docs
```

## Phase 5: Create Static Web App (for React frontend)

### Step 14: Create Static Web App

```powershell
$FrontendApp = "cenet-frontend"
$StaticLocation = "westus2"  # Static Web Apps require specific regions

# Create the Static Web App
az staticwebapp create `
  --name $FrontendApp `
  --resource-group $ResourceGroup `
  --location $StaticLocation `
  --sku free

# Get URL
$FrontendUrl = az staticwebapp show `
  --name $FrontendApp `
  --resource-group $ResourceGroup `
  --query defaultHostname `
  --output tsv

Write-Host "Frontend URL: https://$FrontendUrl"
```

> **Note:** Static Web Apps are only available in `westus2`, `eastus2`, `westeurope`, `eastasia`, `centralindia`. Use `westeurope` equivalent to `westus2`.

### Step 15: Configure Frontend Environment

```powershell
$FrontendUrl = "https://$FrontendApp.azurestaticapps.net"
$BackendUrl = "https://$BackendApp.azurewebsites.net"

# Set environment variables for frontend
az staticwebapp appsettings set `
  --name $FrontendApp `
  --resource-group $ResourceGroup `
  --setting-names `
    VITE_API_BASE_URL="$BackendUrl" `
    VITE_ENVIRONMENT="production"
```

### Step 16: Deploy Frontend to Static Web App

For now, we'll do a manual deployment. Later, GitHub Actions will automate this.

```powershell
# Build the frontend locally first
cd frontend
npm install
npm run build

# Files are now in frontend/dist/

# Deploy using Azure CLI (or use GitHub Actions - see next phase)
# For simplicity, we'll use GitHub Actions which is already configured
```

## Phase 6: Setup GitHub Actions for Automated Deployments

### Step 17: Create GitHub Personal Access Token

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name: `azure-cenet-deployment`
4. Select scopes:
   - ✅ `repo` (full access to repositories)
   - ✅ `workflow` (for GitHub Actions)
5. Click "Generate token"
6. **Copy the token** (you won't see it again)

### Step 18: Get Static Web App Deployment Token

```powershell
# Get the deployment token for GitHub Actions
$DeploymentToken = az staticwebapp secrets list `
  --name $FrontendApp `
  --resource-group $ResourceGroup `
  --query "properties.apiKey" `
  --output tsv

Write-Host "Deployment Token: $DeploymentToken"
Write-Host "Copy this for the next step!"
```

### Step 19: Add Secrets to GitHub Repository

1. Go to your GitHub repo settings: `https://github.com/YOUR_USERNAME/CENet/settings/secrets/actions`
2. Click "New repository secret" and add:

**Secret 1: AZURE_STATICWEB_APPS_API_TOKEN_CENET_FRONTEND**
- Value: (paste the deployment token from Step 18)

**Secret 2: VITE_API_BASE_URL**
- Value: `https://cenet-backend.azurewebsites.net`

**Secret 3: GITHUB_TOKEN**
- Value: (your GitHub PAT from Step 17)

### Step 20: Trigger Frontend Deployment

Push a change to trigger GitHub Actions:

```powershell
git add .
git commit -m "Deploy: configure Azure Static Web Apps"
git push origin main

# Go to your GitHub repo Actions tab to watch the deployment
```

## Phase 7: Configure CORS & Final Setup

### Step 21: Update CORS Configuration

Edit `backend/main.py` to allow your frontend origin:

```python
from fastapi.middleware.cors import CORSMiddleware

# Add this after app = FastAPI(...)
origins = [
    "http://localhost:5173",           # Local development
    "http://localhost:3000",            # Alternative local
    "https://cenet-frontend.azurestaticapps.net",  # Production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy backend:

```powershell
git add backend/main.py
git commit -m "chore: update CORS for production"
git subtree push --prefix backend azure main
```

### Step 22: Test the Full Application

1. Navigate to: `https://cenet-frontend.azurestaticapps.net`
2. Open browser DevTools (F12 → Console tab)
3. Check for:
   - ✅ No CORS errors
   - ✅ API calls succeed
   - ✅ UI loads correctly
4. Test key features:
   - Login/authentication
   - Data fetching
   - Form submissions

### Step 23: Monitor Production

```powershell
# Backend logs
az webapp log stream `
  --name $BackendApp `
  --resource-group $ResourceGroup

# Frontend analytics
# (Static Web Apps dashboard in Azure Portal)
```

## Troubleshooting

### "Connection refused" / Database won't connect

```powershell
# 1. Verify connection string
az webapp config appsettings list `
  --name $BackendApp `
  --resource-group $ResourceGroup | findstr DATABASE_URL

# 2. Check Supabase firewall
# Go to Supabase → Project Settings → Network → IP Whitelist
# Add Azure IP ranges (or allow all for testing): 0.0.0.0/0

# 3. Test connection locally first
cd backend
python -c "from database import engine; print(engine.url)"
```

### 500 errors in API

```powershell
# Check detailed logs
az webapp log stream --name $BackendApp --resource-group $ResourceGroup

# SSH into app to debug
az webapp ssh --name $BackendApp --resource-group $ResourceGroup
# Then: python -c "import sys; print(sys.path)"
```

### Frontend won't load

```powershell
# Check build output
az staticwebapp show --name $FrontendApp --resource-group $ResourceGroup

# Redeploy
git push origin main  # Triggers GitHub Actions
```

### CORS errors when frontend calls API

- Verify `FRONTEND_URL` in backend env vars
- Verify CORS config in `backend/main.py`
- Restart backend: `az webapp restart --name $BackendApp --resource-group $ResourceGroup`

## Cleanup (if needed)

```powershell
# Delete all resources
az group delete --name $ResourceGroup --yes

# This will delete:
# - App Service (backend)
# - App Service Plan
# - Static Web App (frontend)
# - All associated resources
```

## Summary of Deployed URLs

Once complete, you'll have:

| Component | URL |
|-----------|-----|
| **Backend API** | https://cenet-backend.azurewebsites.net |
| **API Docs** | https://cenet-backend.azurewebsites.net/docs |
| **Frontend** | https://cenet-frontend.azurestaticapps.net |

## Next Steps (Optional)

- [ ] Add custom domain names
- [ ] Configure SSL/TLS certificates
- [ ] Set up Azure Monitor & alerts
- [ ] Configure auto-scaling rules
- [ ] Add application insights for monitoring
- [ ] Set up database backups in Supabase

---

**Need help?** Check the detailed [DEPLOYMENT.md](./DEPLOYMENT.md) or Azure docs.
