# 🚀 Quick Deployment Reference

Copy-paste commands for rapid Azure deployment. **Follow the full guide in AZURE_DEPLOYMENT_STEPS.md first!**

## Configuration

```powershell
$ResourceGroup = "cenet-rg"
$BackendApp = "cenet-backend"
$FrontendApp = "cenet-frontend"
$Location = "westeurope"
$DatabaseUrl = "postgresql://YOUR_SUPABASE_CONNECTION_STRING"
$SecretKey = "your-secret-key"
$SessionSecret = "your-session-secret"
```

## 1️⃣ Create Resource Group

```powershell
az group create --name $ResourceGroup --location $Location
```

## 2️⃣ Create App Service Plan & App

```powershell
az appservice plan create --name "$BackendApp-plan" --resource-group $ResourceGroup --sku F1 --is-linux

az webapp create --name $BackendApp --resource-group $ResourceGroup --plan "$BackendApp-plan" --runtime "PYTHON:3.11"
```

## 3️⃣ Configure App Settings

```powershell
az webapp config appsettings set `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --settings `
    DATABASE_URL="$DatabaseUrl" `
    SECRET_KEY="$SecretKey" `
    SESSION_SECRET="$SessionSecret" `
    FRONTEND_URL="https://$FrontendApp.azurestaticapps.net" `
    PYTHONPATH="/home/site/wwwroot" `
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"
```

## 4️⃣ Configure Startup Command

```powershell
az webapp config set `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --startup-file "gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"
```

## 5️⃣ Enable Git Deployment & Get URL

```powershell
$GitUrl = az webapp deployment source config-local-git `
  --name $BackendApp `
  --resource-group $ResourceGroup `
  --query url `
  --output tsv

Write-Host $GitUrl
```

## 6️⃣ Add Azure Remote & Deploy

```powershell
cd c:\Repos\CENet\webapp

git remote add azure $GitUrl

git subtree push --prefix backend azure main
```

## 7️⃣ Monitor Deployment

```powershell
az webapp log stream --name $BackendApp --resource-group $ResourceGroup
```

## 8️⃣ Test Backend

```powershell
$BackendUrl = az webapp show --name $BackendApp --resource-group $ResourceGroup --query defaultHostName --output tsv
Start-Process "https://$BackendUrl/docs"
```

## 9️⃣ Create Static Web App

```powershell
# Note: Static Web Apps only available in specific regions
az staticwebapp create `
  --name $FrontendApp `
  --resource-group $ResourceGroup `
  --location "westus2" `
  --sku free
```

## 🔟 Configure Frontend & Deploy via GitHub

1. Set GitHub secrets (see AZURE_DEPLOYMENT_STEPS.md Step 19)
2. Push to main: `git push origin main`
3. GitHub Actions automatically deploys

## ✅ Verify Deployment

```powershell
# Backend
curl "https://$BackendApp.azurewebsites.net/docs"

# Frontend
Start-Process "https://$FrontendApp.azurestaticapps.net"
```

## 🧹 Cleanup

```powershell
az group delete --name $ResourceGroup --yes
```

---

**Stuck?** See the full guide in [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md)
