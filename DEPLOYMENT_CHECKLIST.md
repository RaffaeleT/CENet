# CENet Azure Deployment Checklist

Use this checklist to track your progress through the deployment process.

## 📋 Pre-Deployment

- [ ] **Azure CLI installed**
  ```powershell
  az --version
  ```

- [ ] **Azure CLI logged in**
  ```powershell
  az account show
  ```

- [ ] **Supabase connection string obtained**
  - Format: `postgresql://postgres:[PASSWORD]@[HOST].postgres.supabase.co:5432/postgres`
  - Obtained from: Supabase Dashboard → Settings → Database → Connection String
  - Saved securely (not in git)

- [ ] **GitHub account with CENet repo**
  - Fork or clone of: your GitHub CENet repo
  - Can push to main branch

## 🏗️ Phase 1: Create Azure Resources

### Resource Group
- [ ] Created resource group: `rgCenet` in `italynorth`
  ```powershell
  az group create --name rgCenet --location italynorth
  ```

### App Service Plan (Backend)
- [ ] Created App Service Plan: `cenet-backend-plan`
  ```powershell
  az appservice plan create --name cenet-backend-plan --resource-group rgCenet --sku F1 --is-linux
  ```

### App Service (Backend API)
- [ ] Created App Service: `cenet-backend` (Python 3.11)
  ```powershell
  az webapp create --name cenet-backend --resource-group rgCenet --plan cenet-backend-plan --runtime "PYTHON:3.11"
  ```

- [ ] Verified app URL
  ```powershell
  az webapp show --name cenet-backend --resource-group rgCenet --query defaultHostName
  ```
  - Should show: `cenet-backend.azurewebsites.net`

## ⚙️ Phase 2: Configure Backend App Service

### Environment Variables
- [ ] Set `DATABASE_URL`
  - Value: Your Supabase PostgreSQL connection string
  
- [ ] Set `SECRET_KEY`
  - Generated random 32-char value
  
- [ ] Set `SESSION_SECRET`
  - Generated random 32-char value
  
- [ ] Set `FRONTEND_URL`
  - Value: `https://cenet-frontend.azurestaticapps.net`
  
- [ ] Set `PYTHONPATH`
  - Value: `/home/site/wwwroot`
  
- [ ] Set `SCM_DO_BUILD_DURING_DEPLOYMENT`
  - Value: `true`

- [ ] Verified all settings saved
  ```powershell
  az webapp config appsettings list --name cenet-backend --resource-group rgCenet --output table
  ```

### Startup Configuration
- [ ] Set startup command
  ```powershell
  az webapp config set --name cenet-backend --resource-group rgCenet --startup-file "gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"
  ```

### Git Deployment
- [ ] Enabled Git deployment
  ```powershell
  az webapp deployment source config-local-git --name cenet-backend --resource-group rgCenet
  ```

- [ ] Saved Git URL: `_____________________________`

- [ ] Added Azure remote to local repo
  ```powershell
  git remote add azure [GIT_URL]
  ```

- [ ] Verified remotes
  ```powershell
  git remote -v
  ```
  - Should show both `origin` and `azure`

## 🚀 Phase 3: Deploy Backend

- [ ] Deployed backend code to Azure
  ```powershell
  git subtree push --prefix backend azure main
  ```

- [ ] Monitored deployment logs
  ```powershell
  az webapp log stream --name cenet-backend --resource-group rgCenet
  ```

- [ ] Verified deployment success
  - Look for: "Application started successfully" or "gunicorn" running
  - Deployment time: 2-5 minutes

- [ ] Tested backend API
  ```powershell
  curl https://cenet-backend.azurewebsites.net/docs
  ```
  - Should return Swagger UI (HTTP 200)

- [ ] Tested API health endpoint
  ```powershell
  curl https://cenet-backend.azurewebsites.net/api/health
  ```
  - (or test a real endpoint like `/api/pages`)

## 📦 Phase 4: Create Frontend Infrastructure

### Static Web App
- [ ] Created Static Web App: `cenet-frontend` in `italynorth`
  ```powershell
  az staticwebapp create --name cenet-frontend --resource-group rgCenet --location italynorth --sku free
  ```

- [ ] Saved frontend URL: `https://cenet-frontend.azurestaticapps.net`

### Frontend Configuration
- [ ] Set `VITE_API_BASE_URL` environment variable
  - Value: `https://cenet-backend.azurewebsites.net`

- [ ] Verified settings saved
  ```powershell
  az staticwebapp appsettings set --name cenet-frontend --resource-group rgCenet --setting-names VITE_API_BASE_URL="https://cenet-backend.azurewebsites.net"
  ```

## 🤖 Phase 5: Setup GitHub Actions

### GitHub Secrets
- [ ] Created GitHub Personal Access Token (PAT)
  - Scopes: `repo`, `workflow`
  - Token saved: `_____________________________`

- [ ] Created Static Web App deployment token
  ```powershell
  az staticwebapp secrets list --name cenet-frontend --resource-group rgCenet --query "properties.apiKey"
  ```
  - Token saved: `_____________________________`

- [ ] Added GitHub secret: `AZURE_STATICWEB_APPS_API_TOKEN_CENET_FRONTEND`
  - Value: Static Web App deployment token
  - Location: https://github.com/YOUR_REPO/settings/secrets/actions

- [ ] Added GitHub secret: `VITE_API_BASE_URL`
  - Value: `https://cenet-backend.azurewebsites.net`

- [ ] Added GitHub secret: `GITHUB_TOKEN`
  - Value: Your GitHub Personal Access Token

### GitHub Actions Workflow
- [ ] Verified `.github/workflows/deploy-frontend.yml` exists
  - Should be created automatically by Azure or manually added

- [ ] Pushed changes to trigger workflow
  ```powershell
  git add .
  git commit -m "Deploy: configure Azure + Supabase"
  git push origin main
  ```

- [ ] Monitored GitHub Actions
  - Go to: https://github.com/YOUR_REPO/actions
  - Watch "Deploy Frontend to Azure Static Web Apps" workflow

- [ ] Verified frontend deployment success
  - Deployment time: 2-5 minutes
  - Check for: "✓ Deploy to Azure Static Web Apps" in workflow logs

## 🔐 Phase 6: Security & CORS

### Update CORS Configuration
- [ ] Updated `backend/main.py` with production origin
  ```python
  origins = [
      "http://localhost:5173",
      "https://cenet-frontend.azurestaticapps.net",
  ]
  ```

- [ ] Committed CORS changes
  ```powershell
  git add backend/main.py
  git commit -m "chore: add production CORS origin"
  git subtree push --prefix backend azure main
  ```

- [ ] Restarted backend app
  ```powershell
  az webapp restart --name cenet-backend --resource-group rgCenet
  ```

- [ ] Verified no CORS errors in frontend
  - Open frontend in browser
  - Open DevTools (F12) → Console
  - Should see no CORS errors

## ✅ Phase 7: Testing & Verification

### Backend Testing
- [ ] Tested API endpoint: `https://cenet-backend.azurewebsites.net/docs`
  - Should show Swagger UI

- [ ] Tested database connection
  - Make a request that queries the database
  - Verify data returns successfully

- [ ] Checked backend logs
  ```powershell
  az webapp log stream --name cenet-backend --resource-group rgCenet
  ```
  - Should show: Request logs, no major errors

- [ ] Tested environment variables loaded
  - Frontend URL should match production
  - Database connection should work

### Frontend Testing
- [ ] Opened frontend: `https://cenet-frontend.azurestaticapps.net`
  - Page should load without errors
  - No CORS errors in DevTools console

- [ ] Tested API calls from frontend
  - Make a request that calls backend API
  - Verify response returns successfully
  - Check DevTools → Network tab

- [ ] Tested key features
  - [ ] Login/authentication
  - [ ] Data fetching
  - [ ] Form submissions
  - [ ] Navigation between pages

### Full Integration Test
- [ ] **Happy path test**: Complete user workflow
  - [ ] User logs in
  - [ ] User navigates app
  - [ ] User performs main action
  - [ ] Data persists in database

## 🔄 Phase 8: Monitoring & Maintenance

### Logging
- [ ] Set up log streaming for backend
  ```powershell
  az webapp log stream --name cenet-backend --resource-group rgCenet
  ```

- [ ] Checked Azure Portal for Static Web App logs
  - Location: Azure Portal → cenet-frontend → Overview

### Performance
- [ ] Verified backend response times (should be <1s)
  - Check in browser DevTools → Network tab

- [ ] Verified frontend load time (should be <3s)
  - Check PageSpeed Insights: https://pagespeed.web.dev/

### Monitoring Alerts (Optional)
- [ ] Set up Azure Monitor (Application Insights)
  - Tracks: API errors, response times, availability

- [ ] Set up email alerts for failures
  - Triggers: High error rate, slow responses

## 📚 Documentation

- [ ] Updated `README.md` with deployment URLs
  - Backend: `https://cenet-backend.azurewebsites.net`
  - Frontend: `https://cenet-frontend.azurestaticapps.net`

- [ ] Documented environment variables
  - Where they're set (Azure App Service, Static Web App)
  - How to update them

- [ ] Created or updated `DEPLOYMENT.md`
  - Includes: How to deploy, troubleshoot, scale

## 🎯 Post-Deployment Tasks

- [ ] Backup old deployment URLs (if migrating)

- [ ] Update DNS records (if using custom domain)
  - CNAME: your-api.yourdomain.com → cenet-backend.azurewebsites.net
  - CNAME: your-app.yourdomain.com → cenet-frontend.azurestaticapps.net

- [ ] Configure SSL/TLS certificates (auto-handled by Azure)

- [ ] Set up automated backups for Supabase
  - Location: Supabase Dashboard → Backups

- [ ] Enable Supabase Row Level Security (RLS)
  - For production security

- [ ] Test OAuth providers (if configured)
  - Google OAuth
  - Microsoft OAuth
  - LinkedIn OAuth

## 🆘 Troubleshooting

If something isn't working:

### Backend won't start
- [ ] Check logs: `az webapp log stream --name cenet-backend --resource-group rgCenet`
- [ ] Verify `DATABASE_URL` format is correct
- [ ] Verify Supabase firewall allows Azure IPs
- [ ] Restart app: `az webapp restart --name cenet-backend --resource-group rgCenet`

### Frontend won't deploy
- [ ] Check GitHub Actions logs
- [ ] Verify `VITE_API_BASE_URL` secret is set
- [ ] Check `npm run build` works locally
- [ ] Verify `.github/workflows/deploy-frontend.yml` exists

### CORS errors
- [ ] Update `backend/main.py` with correct origin
- [ ] Verify `FRONTEND_URL` in app settings
- [ ] Restart backend app

### Database connection fails
- [ ] Verify connection string format
- [ ] Test connection locally: `psql "connection-string"`
- [ ] Check Supabase firewall rules
- [ ] Verify password is correct (special chars might need escaping)

### API calls timeout
- [ ] Check backend logs for slowness
- [ ] Verify database is responding
- [ ] Check network connectivity between Azure services
- [ ] Consider upgrading App Service tier

## ✨ Success Metrics

Your deployment is successful when:

- ✅ Backend API is accessible and returning data
- ✅ Frontend loads without errors
- ✅ Frontend can call backend API without CORS errors
- ✅ User authentication works
- ✅ Database operations work (CRUD)
- ✅ No console errors in browser DevTools
- ✅ Logs show requests being processed
- ✅ GitHub Actions auto-deploys on push to main

## 📞 Support & Next Steps

**If you need help:**

1. Review [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md)
2. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for technical details
3. Review [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for copy-paste reference
4. Check Azure logs and GitHub Actions logs
5. Verify Supabase connection and firewall settings

**Next improvements (optional):**

- [ ] Set up custom domain names
- [ ] Enable Application Insights for monitoring
- [ ] Configure auto-scaling rules
- [ ] Set up cost alerts
- [ ] Implement CI/CD status checks (tests must pass before merge)
- [ ] Add smoke tests for automated monitoring

---

**Deployment Date:** `_____/_____/_____`

**Deployed By:** `_____________________________`

**Notes:** 
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```
