# StansBooth AI Chatbot - Deployment Guide

This guide will help you deploy the StansBooth AI chatbot to GitHub and Azure while keeping your API keys secure.

## 🔐 Security First

Your API keys are now stored in environment variables and will NEVER be committed to GitHub!

### What's Protected:
- ✅ `.env` - Your actual API keys (NOT in Git)
- ✅ `config.py` - Loads from environment variables
- ✅ `.env.example` - Template file (safe to commit)

### Files in Git:
- ✓ Application code (app.py, templates, static files)
- ✓ `.env.example` (template only, no real keys)
- ✓ Documentation
- ✗ `.env` (your actual keys - NEVER committed)
- ✗ `config.py` (loads from .env - NOT committed)

## 📤 Step 1: Push to GitHub

### 1.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `stansbooth-ai-chatbot` (or your choice)
3. Description: "AI-powered chatbot for StansBooth trading platform"
4. **Make it PRIVATE** (to keep your code private)
5. DO NOT initialize with README (we already have one)
6. Click "Create repository"

### 1.2 Push Your Code

```bash
cd C:\Users\ADMIN\AI_Chatbot

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/stansbooth-ai-chatbot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.3 Verify Security

After pushing, check GitHub and make sure:
- ✅ `.env` is NOT visible
- ✅ `config.py` is NOT visible
- ✅ `.env.example` IS visible (that's okay - it's just a template)
- ✅ Your API key is NOT anywhere in the code

## ☁️ Step 2: Deploy to Azure

### 2.1 Prerequisites

1. **Azure Account**
   - Sign up: https://azure.microsoft.com/free/
   - Get $200 free credit

2. **Install Azure CLI** (Optional)
   ```bash
   # Download from: https://aka.ms/installazurecliwindows
   ```

### 2.2 Create Azure Web App

#### Option A: Using Azure Portal (Easiest)

1. Go to https://portal.azure.com
2. Click "Create a resource"
3. Search for "Web App" and click "Create"
4. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: Create new "stansbooth-rg"
   - **Name**: `stansbooth-chatbot` (must be unique)
   - **Publish**: Code
   - **Runtime stack**: Python 3.11
   - **Operating System**: Linux
   - **Region**: Choose nearest to you
   - **Pricing plan**: Free F1 (for testing) or Basic B1 (recommended)
5. Click "Review + Create" → "Create"

#### Option B: Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name stansbooth-rg --location eastus

# Create app service plan
az appservice plan create --name stansbooth-plan --resource-group stansbooth-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group stansbooth-rg --plan stansbooth-plan --name stansbooth-chatbot --runtime "PYTHON:3.11"
```

### 2.3 Configure Environment Variables in Azure

**IMPORTANT**: You must set your API keys in Azure's environment variables!

#### Via Azure Portal:

1. Go to your Web App in Azure Portal
2. Click "Configuration" (under Settings)
3. Click "New application setting"
4. Add each of these:

| Name | Value |
|------|-------|
| `GEMINI_API_KEY` | `AIzaSyB_Q44dCKmdrXv_7o78dlUnu61QgvR_R8c` |
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |
| `SECRET_KEY` | Generate random string: `openssl rand -hex 32` |
| `MONGODB_URI` | Your MongoDB Atlas connection string (if using cloud) |

5. Click "Save" at the top

#### Via Azure CLI:

```bash
# Set environment variables
az webapp config appsettings set --resource-group stansbooth-rg --name stansbooth-chatbot --settings \
  GEMINI_API_KEY="AIzaSyB_Q44dCKmdrXv_7o78dlUnu61QgvR_R8c" \
  FLASK_ENV="production" \
  FLASK_DEBUG="False" \
  SECRET_KEY="your-random-secret-key-here"
```

### 2.4 Deploy from GitHub

#### Via Azure Portal:

1. In your Web App, go to "Deployment Center"
2. Source: **GitHub**
3. Authorize Azure to access your GitHub
4. Select:
   - **Organization**: Your GitHub username
   - **Repository**: stansbooth-ai-chatbot
   - **Branch**: main
5. Click "Save"

Azure will automatically deploy from GitHub and redeploy whenever you push changes!

#### Via Azure CLI:

```bash
# Configure GitHub deployment
az webapp deployment source config --name stansbooth-chatbot --resource-group stansbooth-rg \
  --repo-url https://github.com/YOUR_USERNAME/stansbooth-ai-chatbot \
  --branch main --manual-integration
```

### 2.5 Configure Startup Command

1. Go to "Configuration" → "General settings"
2. **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
3. Click "Save"

### 2.6 Access Your Chatbot

Your chatbot will be available at:
```
https://stansbooth-chatbot.azurewebsites.net
```

(Replace `stansbooth-chatbot` with your actual app name)

## 🗄️ Step 3: MongoDB for Production

### Option 1: MongoDB Atlas (Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Add to Azure environment variables:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   ```

### Option 2: Azure Cosmos DB

1. Create Cosmos DB with MongoDB API in Azure
2. Get connection string
3. Add to Azure environment variables

## 🔒 Security Best Practices

### ✅ DO:
- Keep `.env` file LOCAL only
- Set API keys in Azure environment variables
- Use HTTPS (Azure provides this automatically)
- Keep your GitHub repo PRIVATE
- Regularly rotate API keys
- Use strong SECRET_KEY in production

### ❌ DON'T:
- NEVER commit `.env` to Git
- NEVER hardcode API keys in code
- NEVER make repo public with API keys
- NEVER share your `.env` file
- NEVER commit `config.py` with actual keys

## 🧪 Testing Deployment

After deployment:

1. Visit your Azure URL
2. Try these questions:
   - "What services do you offer?"
   - "How much is the Professional plan?"
   - "Do AI trading bots work?"

3. Check logs in Azure Portal:
   - Go to "Log stream" to see real-time logs
   - Go to "Monitoring" → "Logs" for detailed analysis

## 🔄 Updating Your Chatbot

### To deploy updates:

```bash
# Make changes to your code
git add .
git commit -m "Your update description"
git push origin main
```

Azure will automatically redeploy!

## 📊 Monitoring

### View Logs:
```bash
az webapp log tail --name stansbooth-chatbot --resource-group stansbooth-rg
```

### View Metrics:
- Go to Azure Portal → Your Web App → "Metrics"
- Monitor: CPU, Memory, Response Time, Requests

## 🆘 Troubleshooting

### App won't start:
1. Check "Log stream" in Azure Portal
2. Verify environment variables are set
3. Check `requirements.txt` is up to date

### MongoDB connection fails:
1. Check MONGODB_URI in Azure environment variables
2. Whitelist Azure IPs in MongoDB Atlas
3. Check connection string format

### API key errors:
1. Verify `GEMINI_API_KEY` in Azure Portal → Configuration
2. Make sure there are no spaces or quotes in the value
3. Restart the app after setting variables

## 💰 Cost Estimate

### Free Tier:
- **Azure Web App (F1)**: Free (limited resources)
- **MongoDB Atlas**: Free tier (512MB)
- **Total**: $0/month

### Recommended for Production:
- **Azure Web App (B1)**: ~$13/month
- **MongoDB Atlas**: Free to $57/month
- **Total**: $13-70/month

## 🎯 Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Azure
3. ✅ Set environment variables
4. ✅ Test the deployment
5. ✅ Set up custom domain (optional)
6. ✅ Enable HTTPS (auto-enabled by Azure)
7. ✅ Monitor usage and performance

---

**Your API keys are now secure and your chatbot is ready for the world!** 🚀

For issues: Info@stansbooth.com
