# 🚀 CENet Azure + Supabase Deployment - Start Here

Welcome! Your CENet monorepo is now fully configured for deployment to Azure with Supabase.

## ⚡ Quick Start (5 minutes)

1. **Read this file** ← You're here
2. **Provide Supabase connection string** (see below)
3. **Open the appropriate guide:**
   - 📚 **[AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md)** - Detailed step-by-step (recommended)
   - ⚡ **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** - Copy-paste commands (for experienced users)

## 📋 What's Been Set Up For You

✅ **Backend infrastructure** - FastAPI configured for Azure App Service  
✅ **Frontend infrastructure** - React Vite configured for Azure Static Web Apps  
✅ **Database** - Configured for Supabase PostgreSQL  
✅ **CI/CD** - GitHub Actions workflow for automatic frontend deployment  
✅ **Documentation** - Complete deployment guides and checklists  

## 🎯 You Need To Provide

### 1️⃣ Supabase PostgreSQL Connection String

**Get it here:**
- Go to [supabase.com](https://supabase.com)
- Click on your project
- Settings → Database → Connection String (PostgreSQL tab)
- Copy the full string (format: `postgresql://postgres:[PASSWORD]@[HOST].postgres.supabase.co:5432/postgres`)
- Replace `[PASSWORD]` with your actual password

**Share it when ready** - I'll guide you through the deployment.

### 2️⃣ Your GitHub Repository URL

- Need the URL of your GitHub repo containing this code
- Used for Static Web App setup

## 📖 Which Guide Should I Use?

### 👉 Use [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) if:

- ✅ You want detailed explanations for each step
- ✅ This is your first time deploying to Azure
- ✅ You want to understand what's happening
- ✅ You have time (30-45 minutes)

**Contains:** 23 detailed steps with explanations, screenshots guidance, troubleshooting tips

### 👉 Use [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) if:

- ✅ You're experienced with Azure/cloud deployments
- ✅ You want copy-paste commands only
- ✅ You're in a hurry
- ✅ You understand the architecture already

**Contains:** Minimal explanations, just the commands to run

### 👉 Use [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) if:

- ✅ You want to track your progress
- ✅ You're following the detailed guide
- ✅ You need to verify each step is complete
- ✅ You want a record of what was done

**Contains:** Checkbox format for marking completion

## 🏗️ Architecture Overview

```
Your Azure Subscription
├── Resource Group (cenet-rg)
│   ├── App Service (cenet-backend)
│   │   └── FastAPI running on Gunicorn
│   └── Static Web App (cenet-frontend)
│       └── React + Vite (compiled to static files)
│
└── External: Supabase PostgreSQL Database
```

**How it works:**
1. Frontend (React) deployed to Azure Static Web Apps
2. Frontend calls backend API (HTTPS, no CORS issues)
3. Backend calls Supabase database
4. All traffic encrypted with SSL/TLS

## 💰 Estimated Costs

| Service | Free/Tier | Monthly Cost |
|---------|-----------|--------------|
| Azure App Service | F1 (Free) | €0 |
| Azure Static Web Apps | Free | €0 |
| Supabase | Free tier | €0 |
| **Total** | | **€0** |

**Note:** F1 sleeps after 20 min inactivity. First request after sleep takes ~30s. Fine for 1-5 test users.

## ⏱️ Time Estimates

| Activity | Time |
|----------|------|
| Read detailed guide | 10 min |
| Prepare Supabase | 5 min |
| Create Azure resources | 10 min |
| Deploy backend | 10 min |
| Deploy frontend | 5 min |
| Test & verify | 15 min |
| **Total** | ~55 min |

## 📦 Files Created For You

| File | What it does |
|------|-------------|
| **AZURE_DEPLOYMENT_STEPS.md** | 📚 Main guide - read this first |
| **QUICK_DEPLOY.md** | ⚡ Quick reference with commands |
| **DEPLOYMENT_CHECKLIST.md** | ✅ Track your progress |
| **DEPLOYMENT_SUMMARY.md** | 📋 Overview of deployment |
| **DEPLOYMENT.md** | 📖 Technical reference |
| **backend/startup.sh** | 🚀 Azure startup script |
| **backend/requirements.txt** | 📦 Updated with gunicorn |
| **.github/workflows/deploy-frontend.yml** | 🤖 GitHub Actions automation |
| **staticwebapp.config.json** | ⚙️ Static Web Apps config |
| **deploy-azure.ps1** | 🔧 PowerShell deployment helper |

## 🎓 Prerequisites

Before starting, verify you have:

- ✅ Azure CLI installed (`az --version`)
- ✅ Logged into Azure (`az account show`)
- ✅ Your Supabase connection string
- ✅ GitHub account with your CENet repo
- ✅ PowerShell or Bash terminal

**Missing something?**
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
- Supabase: Create free account at https://supabase.com

## ✅ Success Looks Like

After deployment, you'll have:

```
Backend API:  https://cenet-backend.azurewebsites.net/docs
Frontend Web: https://cenet-frontend.azurestaticapps.net
Database:     Supabase PostgreSQL (connected & working)
```

And you can:
- ✅ Visit the frontend URL and use the app
- ✅ See API docs at `/docs` endpoint
- ✅ Make database queries from the app
- ✅ Push to GitHub and auto-deploy via GitHub Actions

## 🚨 Important Notes

### 🔐 Security
- **Don't** commit your Supabase connection string to git
- **Do** use Azure Key Vault for production secrets
- **Do** enable Row Level Security (RLS) in Supabase for production

### 📊 Monitoring
- Monitor costs in Azure Portal (might surprise you!)
- Set cost alerts to avoid unexpected bills
- Check logs regularly for errors

### 🔄 Updates
- Backend updates: Push to git, then run `git subtree push --prefix backend azure main`
- Frontend updates: Push to main branch, GitHub Actions handles it automatically

## 🆘 Getting Help

**If you get stuck:**

1. ✅ Check the **Troubleshooting** section in [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md)
2. ✅ Review the **DEPLOYMENT_CHECKLIST.md** to verify you completed each step
3. ✅ Check the **[DEPLOYMENT.md](./DEPLOYMENT.md)** for technical details
4. ✅ Run these commands to check status:
   ```powershell
   # Check Azure resources exist
   az group show --name cenet-rg
   az webapp show --name cenet-backend --resource-group cenet-rg
   az staticwebapp show --name cenet-frontend --resource-group cenet-rg
   
   # Check logs
   az webapp log stream --name cenet-backend --resource-group cenet-rg
   ```

## 🎯 Next Steps

### Right Now
1. **Gather your Supabase connection string**
2. **Open [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md)**
3. **Follow the steps in order**

### During Deployment
- Keep the terminal open to monitor logs
- Be patient - deployments take 2-5 minutes per step
- Use [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) to track progress

### After Deployment
- Test the application thoroughly
- Monitor logs for errors
- Consider adding custom domains
- Set up backup procedures
- Plan capacity needs

## 📚 Documentation Structure

```
Deployment Documents
├── DEPLOYMENT_README.md          ← You are here
├── AZURE_DEPLOYMENT_STEPS.md     ← Read this next (detailed guide)
├── QUICK_DEPLOY.md               ← For experienced users (commands only)
├── DEPLOYMENT_CHECKLIST.md       ← Use to track progress
├── DEPLOYMENT_SUMMARY.md         ← Overview & reference
└── DEPLOYMENT.md                 ← Deep technical reference
```

## 🎉 You're All Set!

Your CENet app is ready to deploy. Everything is configured and documented.

**👉 Next step:** Open [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) and follow the detailed guide.

---

### Quick Links

| What you need | Link |
|---------------|------|
| Detailed deployment guide | [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) |
| Quick reference (copy-paste) | [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) |
| Progress tracking | [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) |
| Troubleshooting | [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md#troubleshooting) |
| Cost information | [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md#-estimated-costs-per-month) |

### External Resources

| Service | Link |
|---------|------|
| Azure Portal | [portal.azure.com](https://portal.azure.com) |
| Supabase | [supabase.com](https://supabase.com) |
| GitHub | [github.com](https://github.com) |
| Azure CLI Docs | [Microsoft Docs](https://learn.microsoft.com/en-us/cli/azure/) |

---

**Ready to deploy? → Open [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) now!** 🚀
