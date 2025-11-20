# StansBooth AI Chatbot - Complete Setup Guide

Your AI chatbot is now fully integrated with StansBooth knowledge base and MongoDB! Follow these steps to get everything running.

## 🎯 What's New

Your chatbot now:
- ✅ Knows everything about StansBooth services, pricing, and features
- ✅ Uses MongoDB for intelligent knowledge retrieval
- ✅ Has StansBooth branding and professional UI
- ✅ Provides context-aware responses
- ✅ Handles both StansBooth questions AND general queries

## 📋 Quick Start (3 Steps)

### Step 1: Install MongoDB

**Option A: Local Installation (Recommended)**

**Windows:**
1. Download: https://www.mongodb.com/try/download/community
2. Run installer, choose "Complete" installation
3. Install as Windows Service
4. MongoDB will start automatically

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**Linux (Ubuntu):**
```bash
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

**Option B: MongoDB Atlas (Cloud - Free)**
- Sign up at: https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string
- See [MONGODB_SETUP.md](MONGODB_SETUP.md) for details

### Step 2: Load Knowledge Base

```bash
cd C:\Users\ADMIN\AI_Chatbot
python setup_mongodb.py
```

You should see:
```
✓ Connected to MongoDB: stansbooth_db
✓ Loaded XX knowledge base entries into MongoDB
✓ Setup Complete!
```

### Step 3: Run the Chatbot

```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

## 🧪 Test the Chatbot

Try these questions to test the knowledge base:

1. **"What services do you offer?"**
   - Should list 6 StansBooth services

2. **"Show me your pricing plans"**
   - Should describe Starter, Professional, Business, Premium, Enterprise plans

3. **"What is algorithmic trading?"**
   - Should explain with StansBooth context

4. **"How much does the Professional plan cost?"**
   - Should give exact pricing: $25/month or $250/year

5. **"Do AI trading bots actually work?"**
   - Should answer from FAQ knowledge base

## 📁 Project Structure

```
AI_Chatbot/
├── app.py                      # Main Flask app with MongoDB integration
├── config.py                   # API keys (not in Git)
├── mongodb_handler.py          # MongoDB operations
├── knowledge_base.json         # StansBooth data
├── setup_mongodb.py            # Database setup script
├── chat_history.json           # Your chat history (auto-created)
├── templates/
│   └── index.html             # StansBooth branded UI
├── static/
│   ├── style.css              # Updated styles
│   └── script.js              # Updated functionality
├── MONGODB_SETUP.md           # Detailed MongoDB guide
├── README.md                  # General documentation
└── GIT_RECOVERY_GUIDE.md      # Git backup instructions
```

## 🔧 Configuration

### Using MongoDB Atlas (Cloud)

1. Edit `config.py`:
```python
# Add after GEMINI_API_KEY
MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/"
```

2. Edit `app.py` line 20:
```python
# Change from:
mongo_db = MongoDBHandler()

# To:
from config import MONGODB_URI
mongo_db = MongoDBHandler(connection_string=MONGODB_URI)
```

## 🎨 Customization

### Update Knowledge Base

1. Edit `knowledge_base.json`
2. Re-run setup:
   ```bash
   python setup_mongodb.py
   ```

### Change Branding

**Company Name:**
- Edit `templates/index.html` (search for "StansBooth")
- Edit `app.py` SYSTEM_PROMPT

**Colors:**
- Edit `static/style.css` gradients

**Welcome Message:**
- Edit `templates/index.html` welcome section

## 🔍 How It Works

1. **User asks a question** →
2. **App searches MongoDB** for relevant knowledge →
3. **Context is retrieved** (services, pricing, FAQs) →
4. **Gemini AI generates response** using context + system prompt →
5. **User gets accurate, StansBooth-specific answer**

## 📊 MongoDB Collections

The `knowledge_base` collection contains:
- Company info (name, contact, social media)
- Services (6 automated trading services)
- Features (5 smart analysis features)
- Pricing plans (5 plans with details)
- Trading sessions (ASIA, LONDON, NEWYORK)
- FAQs (8 common questions)
- Vision & mission statements
- Blog posts

## 🚨 Troubleshooting

### MongoDB Not Connected

**Symptom:** Chatbot works but doesn't know about StansBooth

**Solution:**
```bash
# Check MongoDB is running
mongod --version

# Windows: Start service
net start MongoDB

# Mac: Check status
brew services list

# Linux: Check status
sudo systemctl status mongod

# Then run setup
python setup_mongodb.py
```

### Knowledge Base Not Loading

**Error:** `⚠️ MongoDB is not running!`

**Solution:**
1. Install MongoDB (see Step 1 above)
2. Start MongoDB service
3. Run `python setup_mongodb.py`
4. Restart Flask app

### Chatbot Gives Generic Answers

**Issue:** Responses don't mention StansBooth

**Check:**
```bash
# Verify MongoDB has data
mongosh
use stansbooth_db
db.knowledge_base.find().count()
# Should return 40+ documents
```

## 🔐 Security Notes

- `config.py` is NOT in Git (contains your API key)
- `chat_history.json` is NOT in Git (private conversations)
- MongoDB connection strings should be kept secure
- For production, use environment variables

## 🔄 Updating the Chatbot

Made changes? Commit them:

```bash
git add .
git commit -m "Description of changes"
```

Need to recover? See [GIT_RECOVERY_GUIDE.md](GIT_RECOVERY_GUIDE.md)

## 📈 Next Steps

1. **Test thoroughly** - Ask various questions
2. **Customize branding** - Match your style
3. **Add more knowledge** - Update knowledge_base.json
4. **Deploy** - Use services like Heroku, AWS, or DigitalOcean
5. **Monitor** - Check chat_history.json for user questions

## 💡 Tips

- MongoDB runs locally on port 27017 by default
- Knowledge base auto-updates when you re-run setup
- Chatbot falls back to general AI if MongoDB is offline
- Example questions help users discover features

## 📞 Support

- MongoDB Issues: See [MONGODB_SETUP.md](MONGODB_SETUP.md)
- Git/Recovery: See [GIT_RECOVERY_GUIDE.md](GIT_RECOVERY_GUIDE.md)
- General Info: See [README.md](README.md)

---

**You're all set!** Run the 3 steps above and your StansBooth AI assistant will be live! 🚀
