# 🚀 START HERE - CENet Azure Deployment

Welcome! Your CENet app is ready to deploy to Azure with Supabase.

## ⚡ In 30 Seconds

**What you need:**
1. Your Supabase PostgreSQL connection string
2. Azure CLI (already logged in)
3. This file + the guides provided

**What you'll get:**
- ✅ Backend API: `https://cenet-backend.azurewebsites.net`
- ✅ Frontend Web: `https://cenet-frontend.azurestaticapps.net`
- ✅ Database: Your Supabase PostgreSQL
- ✅ Auto-deployment: GitHub Actions on push to main

## 📋 3 Steps to Deploy

### Step 1: Get Your Supabase Connection String
```
supabase.com → Your Project → Settings → Database
→ Connection String (PostgreSQL tab)
Format: postgresql://postgres:[PASSWORD]@[HOST].postgres.supabase.co:5432/postgres
```

### Step 2: Choose Your Guide

**Option A: Detailed Guide (Recommended)** ⭐
- Open: [`DEPLOYMENT_README.md`](./DEPLOYMENT_README.md)
- Then: [`AZURE_DEPLOYMENT_STEPS.md`](./AZURE_DEPLOYMENT_STEPS.md)
- Time: 30-45 minutes
- Best for: First-time deployers, learning

**Option B: Quick Reference**
- Open: [`QUICK_DEPLOY.md`](./QUICK_DEPLOY.md)
- Time: 15-20 minutes
- Best for: Experienced cloud users

### Step 3: Follow the Guide
Use [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) to track progress.

## 🎯 What Each File Does

| File | Purpose | Read Time |
|------|---------|-----------|
| **DEPLOYMENT_README.md** | Overview & entry point | 5 min |
| **AZURE_DEPLOYMENT_STEPS.md** | Step-by-step guide (detailed) | 30-45 min |
| **QUICK_DEPLOY.md** | Copy-paste commands | 15-20 min |
| **DEPLOYMENT_CHECKLIST.md** | Track your progress | During deployment |
| **ARCHITECTURE_DIAGRAM.md** | Visual diagrams | 10 min |
| **DEPLOYMENT_SUMMARY.md** | Reference material | As needed |

## 📦 What Gets Deployed

```
Your CENet App
├── Frontend (React + Vite)
│   └── Azure Static Web Apps
│       └── Global CDN + HTTPS
├── Backend (FastAPI + Gunicorn)
│   └── Azure App Service
│       └── Auto-scaling capable
└── Database (PostgreSQL)
    └── Supabase
        └── Managed backups + security
```

## ✅ Quick Checklist

Before you start:
- [ ] Azure CLI installed (`az --version`)
- [ ] Logged into Azure (`az account show`)
- [ ] Supabase connection string ready
- [ ] GitHub account with your CENet repo

## 🚀 Timeline

| Phase | Time |
|-------|------|
| Read guide | 10 min |
| Prepare Supabase | 5 min |
| Create Azure resources | 10 min |
| Deploy backend | 10 min |
| Deploy frontend | 5 min |
| Test & verify | 15 min |
| **Total** | **~55 min** |

## 💰 Cost

| Service | Cost |
|---------|------|
| Azure App Service (F1) | Free |
| Static Web Apps | Free |
| Supabase (free tier) | Free |
| **Total** | **€0/month** |

F1 is free. App sleeps after 20 min inactivity; first request takes ~30s (fine for testing).

## 📞 Need Help?

1. **Check the docs:**
   - [AZURE_DEPLOYMENT_STEPS.md](./AZURE_DEPLOYMENT_STEPS.md) → Troubleshooting section
   - [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md) → FAQ

2. **Verify your setup:**
   ```powershell
   az account show                    # Check Azure login
   az group list                      # Check resources
   ```

3. **Check logs:**
   ```powershell
   az webapp log stream --name cenet-backend --resource-group cenet-rg
   ```

## 🎯 Success Looks Like

After deployment:
- ✅ Can visit `https://cenet-frontend.azurestaticapps.net`
- ✅ Frontend loads without errors
- ✅ Can see API docs at `https://cenet-backend.azurewebsites.net/docs`
- ✅ Frontend can call backend API
- ✅ Database operations work

## 🔐 Important Security Notes

**DO:**
- ✅ Keep Supabase connection string private
- ✅ Use strong SECRET_KEY and SESSION_SECRET values
- ✅ Enable Row Level Security (RLS) in Supabase for production
- ✅ Use Azure Key Vault for production secrets

**DON'T:**
- ❌ Commit connection strings to Git
- ❌ Use default/weak secrets
- ❌ Share your Supabase credentials
- ❌ Expose API keys in frontend code

## 🚀 Let's Go!

**👉 Next Step:**

1. Open [`DEPLOYMENT_README.md`](./DEPLOYMENT_README.md)
2. Follow the step-by-step guide
3. Use [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) to track progress

**Estimated time to full production deployment: ~1 hour**

---

**Questions?** Check the troubleshooting section in the guides.

**Ready?** → Open `DEPLOYMENT_README.md` now! 🚀
