# Deployment Guide - StansBooth Chatbot

## Prerequisites

- Git installed
- GitHub account
- Python 3.8+
- MongoDB (optional for knowledge base)

## Step 1: Setup Git Remote

If you haven't connected to GitHub repository yet:

```bash
git remote add origin https://github.com/Stansbooth/chatbot.git
```

Verify remote:
```bash
git remote -v
```

## Step 2: Commit Your Changes

Add all files:
```bash
git add .
```

Commit with message:
```bash
git commit -m "Update chatbot with /chat endpoint and complete API documentation"
```

## Step 3: Push to GitHub

Push to master branch:
```bash
git push -u origin master
```

If prompted for authentication, use:
- Username: Your GitHub username
- Password: Your Personal Access Token (not your GitHub password)

### Create Personal Access Token

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy the token and use it as password

## Step 4: Deploy to Hosting Platform

### Option A: Deploy to Render (Recommended)

1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `stansbooth-chatbot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: Free

6. Add Environment Variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `MONGODB_URI`: Your MongoDB connection string

7. Click "Create Web Service"

### Option B: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Select your repository
5. Add environment variables:
   - `GEMINI_API_KEY`
   - `MONGODB_URI`
6. Railway auto-detects Python and deploys

### Option C: Deploy to PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create account (free tier available)
3. Open Bash console
4. Clone repository:
   ```bash
   git clone https://github.com/Stansbooth/chatbot.git
   ```
5. Setup virtual environment:
   ```bash
   mkvirtualenv chatbot --python=python3.10
   pip install -r requirements.txt
   ```
6. Configure Web app in dashboard
7. Set environment variables in WSGI file

### Option D: Deploy to Heroku

1. Install Heroku CLI
2. Login:
   ```bash
   heroku login
   ```
3. Create app:
   ```bash
   heroku create stansbooth-chatbot
   ```
4. Add Procfile to project root:
   ```
   web: gunicorn app:app
   ```
5. Set environment variables:
   ```bash
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set MONGODB_URI=your_uri
   ```
6. Deploy:
   ```bash
   git push heroku master
   ```

## Step 5: Setup Production MongoDB

### MongoDB Atlas (Free Tier)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Create database user
4. Whitelist IP: `0.0.0.0/0` (allow all)
5. Get connection string
6. Update `.env` with MongoDB Atlas URI

## Step 6: Required Files for Deployment

Ensure these files exist:

### Procfile (for Heroku/Render)
```
web: gunicorn app:app
```

### runtime.txt (optional)
```
python-3.10.0
```

### .gitignore
```
.env
__pycache__/
*.pyc
chat_history.json
.claude/
```

## Step 7: Update Requirements for Production

Add to requirements.txt:
```
gunicorn==21.2.0
```

## Environment Variables Needed

```env
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/stansbooth_db
```

## Testing Deployed App

After deployment, test endpoints:

```bash
# Replace with your deployed URL
curl https://your-app.onrender.com/

curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"msg": "Hello"}'
```

## Troubleshooting

**Issue: App crashes on startup**
- Check logs: `heroku logs --tail` or check Render/Railway dashboard
- Verify all environment variables are set
- Check requirements.txt has all dependencies

**Issue: MongoDB connection fails**
- Verify MONGODB_URI is correct
- Check IP whitelist in MongoDB Atlas
- App works without MongoDB (reduced functionality)

**Issue: Port binding error**
- Ensure app uses `PORT` environment variable:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

## Post-Deployment

1. Update repository README with live URL
2. Test all endpoints
3. Monitor logs for errors
4. Set up MongoDB with knowledge base data
5. Configure custom domain (optional)

## Quick Deploy Commands

```bash
# Add all changes
git add .

# Commit
git commit -m "Deploy chatbot to production"

# Push to GitHub
git push origin master

# Deploy to Render/Railway (auto-deploys from GitHub)
# Or push to Heroku
git push heroku master
```

## Support

For issues:
- Check deployment logs
- Verify environment variables
- Test locally first: `python app.py`
- Contact: Info@stansbooth.com
