#!/usr/bin/env pwsh
<#
.SYNOPSIS
Deploy CENet monorepo to Azure with Supabase database
.DESCRIPTION
Creates Azure resources (App Service for backend, Static Web App for frontend)
and configures them for the CENet application.
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$ResourceGroup = "cenet-rg",

    [Parameter(Mandatory = $false)]
    [string]$BackendAppName = "cenet-backend",

    [Parameter(Mandatory = $false)]
    [string]$FrontendAppName = "cenet-frontend",

    [Parameter(Mandatory = $false)]
    [string]$Location = "westeurope",

    [Parameter(Mandatory = $false)]
    [string]$DatabaseUrl = "",

    [Parameter(Mandatory = $false)]
    [string]$GithubRepoUrl = ""
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$WarningColor = "Yellow"
$InfoColor = "Cyan"

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $Color = switch ($Type) {
        "Success" { $SuccessColor }
        "Error" { $ErrorColor }
        "Warning" { $WarningColor }
        default { $InfoColor }
    }
    Write-Host "[$Type] $Message" -ForegroundColor $Color
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..." "Info"

    # Check Azure CLI
    try {
        $azVersion = az --version 2>&1
        Write-Status "✓ Azure CLI installed" "Success"
    }
    catch {
        Write-Status "✗ Azure CLI not found. Install from https://aka.ms/installazurecliwindows" "Error"
        exit 1
    }

    # Check Azure login
    try {
        $account = az account show 2>&1
        if ($account -match "error") {
            throw "Not logged in"
        }
        Write-Status "✓ Azure CLI authenticated" "Success"
    }
    catch {
        Write-Status "✗ Not logged in to Azure. Run: az login" "Error"
        exit 1
    }
}

function New-ResourceGroup {
    Write-Status "Creating resource group: $ResourceGroup" "Info"

    $rg = az group create `
        --name $ResourceGroup `
        --location $Location `
        --output json | ConvertFrom-Json

    Write-Status "✓ Resource group created: $($rg.location)" "Success"
    return $rg
}

function New-AppServicePlan {
    Write-Status "Creating App Service Plan..." "Info"

    $plan = az appservice plan create `
        --name "$BackendAppName-plan" `
        --resource-group $ResourceGroup `
        --sku F1 `
        --is-linux `
        --output json | ConvertFrom-Json

    Write-Status "✓ App Service Plan created (SKU: $($plan.sku.name))" "Success"
    return $plan
}

function New-WebApp {
    Write-Status "Creating App Service for backend..." "Info"

    $app = az webapp create `
        --name $BackendAppName `
        --resource-group $ResourceGroup `
        --plan "$BackendAppName-plan" `
        --runtime "PYTHON:3.11" `
        --output json | ConvertFrom-Json

    Write-Status "✓ App Service created: https://$($app.defaultHostName)" "Success"
    return $app
}

function Set-AppSettings {
    param(
        [hashtable]$Settings
    )

    Write-Status "Configuring app settings..." "Info"

    $settingsList = @()
    foreach ($key in $Settings.Keys) {
        $settingsList += "$key=`"$($Settings[$key])`""
    }

    az webapp config appsettings set `
        --name $BackendAppName `
        --resource-group $ResourceGroup `
        --settings $settingsList `
        --output json | Out-Null

    Write-Status "✓ App settings configured" "Success"
}

function Set-StartupCommand {
    Write-Status "Configuring startup command..." "Info"

    az webapp config set `
        --name $BackendAppName `
        --resource-group $ResourceGroup `
        --startup-file "gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app" `
        --output json | Out-Null

    Write-Status "✓ Startup command set" "Success"
}

function Enable-GitDeployment {
    Write-Status "Enabling Git deployment..." "Info"

    $gitUrl = az webapp deployment source config-local-git `
        --name $BackendAppName `
        --resource-group $ResourceGroup `
        --query url `
        --output tsv

    Write-Status "✓ Git deployment enabled" "Success"
    Write-Status "Git remote URL: $gitUrl" "Info"

    return $gitUrl
}

function Update-Requirements {
    Write-Status "Updating requirements.txt for Azure..." "Info"

    # Ensure gunicorn is in requirements
    $requirementsPath = Join-Path "backend" "requirements.txt"

    if (Test-Path $requirementsPath) {
        $content = Get-Content $requirementsPath -Raw
        if ($content -notmatch "gunicorn") {
            Add-Content $requirementsPath "gunicorn"
            Write-Status "✓ Added gunicorn to requirements.txt" "Success"
        }
    }
}

# ============= MAIN EXECUTION =============

Write-Host @"
╔══════════════════════════════════════════════════════════╗
║       CENet Azure + Supabase Deployment Script           ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor $InfoColor

Write-Status "Configuration:" "Info"
Write-Status "  Resource Group: $ResourceGroup"
Write-Status "  Backend App: $BackendAppName"
Write-Status "  Frontend App: $FrontendAppName"
Write-Status "  Region: $Location"
Write-Host ""

# Run checks
Test-Prerequisites

if (-not $DatabaseUrl) {
    Write-Status "⚠ DatabaseUrl not provided. You'll need to set it manually after deployment." "Warning"
    Write-Host "  Run: az webapp config appsettings set --name $BackendAppName --resource-group $ResourceGroup --settings DATABASE_URL=`"your-connection-string`""
    Write-Host ""
}

# Create resources
New-ResourceGroup
New-AppServicePlan
New-WebApp

# Configure app
$settings = @{
    "PYTHONPATH" = "/home/site/wwwroot"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "PYTHON_VERSION" = "3.11"
}

if ($DatabaseUrl) {
    $settings["DATABASE_URL"] = $DatabaseUrl
    $settings["SECRET_KEY"] = (openssl rand -hex 32)
    $settings["SESSION_SECRET"] = (openssl rand -hex 32)
}

Set-AppSettings -Settings $settings
Set-StartupCommand
Update-Requirements
$gitUrl = Enable-GitDeployment

# Display next steps
Write-Host @"

╔══════════════════════════════════════════════════════════╗
║                    NEXT STEPS                             ║
╚══════════════════════════════════════════════════════════╝

1. Add Azure Git remote to your local repo:
   git remote add azure "$gitUrl"

2. Deploy the backend:
   git subtree push --prefix backend azure main

3. After deployment, SSH into the app to verify:
   az webapp ssh --name $BackendAppName --resource-group $ResourceGroup

4. Monitor logs during deployment:
   az webapp log stream --name $BackendAppName --resource-group $ResourceGroup

5. Get your backend app URL:
   https://$BackendAppName.azurewebsites.net

6. Update CORS in backend/main.py with your frontend URL

7. Deploy frontend to Static Web Apps (manually or via GitHub Actions)

For detailed steps, see DEPLOYMENT.md
"@ -ForegroundColor $SuccessColor

# Save configuration
$config = @{
    ResourceGroup = $ResourceGroup
    BackendAppName = $BackendAppName
    FrontendAppName = $FrontendAppName
    Location = $Location
    GitUrl = $gitUrl
    Timestamp = Get-Date
}

$config | ConvertTo-Json | Out-File "azure-deployment-config.json"
Write-Status "✓ Configuration saved to azure-deployment-config.json" "Success"
