# Deploy to Railway - Complete Guide

## Prerequisites

- GitHub Account
- Railway Account (sign up at https://railway.app)
- OpenAI API Key

## Step 1: Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
git init
git add .
git commit -m "Initial commit - EV Range Chatbot"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "ev-range-chatbot")
3. Push your code:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ev-range-chatbot.git
git branch -M main
git push -u origin main
```

## Step 3: Connect to Railway

### Option A: Deploy via Railway Dashboard (Recommended)

1. Go to https://railway.app
2. Click **"Create New Project"**
3. Select **"Deploy from GitHub"**
4. Connect your GitHub account and authorize
5. Select your **"ev-range-chatbot"** repository
6. Railway will auto-detect your `railway.json` and `Procfile`

### Option B: Use Railway CLI

```powershell
npm install -g @railway/cli
railway login
cd "C:\@study folder\vs code files\ev-range-Chatbot-project"
railway init
railway up
```

## Step 4: Configure Environment Variables

1. In Railway dashboard, go to your project
2. Click on the service (deployment)
3. Go to **Variables** tab
4. Add your OpenAI API key:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-xxx...` (your actual key)

## Step 5: Deploy

- If using Dashboard: Click **"Deploy"** button
- If using CLI: The `railway up` command automatically deploys

Railway will:

1. Detect Python project
2. Install dependencies from `requirements.txt`
3. Run the start command from `Procfile`
4. Assign a public URL

## Step 6: Access Your App

After deployment completes, you'll see a URL like:

```
https://ev-range-chatbot-production-abc123.up.railway.app
```

## Step 7: Update Frontend API Calls

If your HTML makes API calls, update them to use the Railway URL.

In `static/chat_ui.html`, replace API calls:

```javascript
// Change from:
fetch("http://localhost:5000/chat/start", ...)

// To:
fetch("https://YOUR-RAILWAY-URL/chat/start", ...)
```

## Useful Railway Commands

```powershell
# View logs
railway logs

# View project status
railway status

# List all projects
railway list

# Redeploy
railway up
```

## Troubleshooting

### App won't start

- Check logs: `railway logs`
- Verify `Procfile` syntax
- Ensure `requirements.txt` has all dependencies

### 502 Bad Gateway

- Check if app is crashing
- View logs for Python errors
- Verify OpenAI API key is set

### Models/data not found

- Ensure `Models/` folder is in git
- Check file paths are relative (already fixed in updated code)

## Files Created for Railway

- **Procfile** - Tells Railway how to start your app
- **railway.json** - Railway configuration
- **runtime.txt** - Specifies Python version
- **.gitignore** - Prevents uploading unnecessary files

Your project is now ready to deploy! 🚀
