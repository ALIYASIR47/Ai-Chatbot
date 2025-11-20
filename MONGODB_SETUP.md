# MongoDB Setup Guide for StansBooth AI Chatbot

This guide will help you set up MongoDB for the StansBooth AI chatbot's knowledge base.

## Option 1: Install MongoDB Locally (Recommended for Development)

### Windows Installation

1. **Download MongoDB Community Edition**
   - Visit: https://www.mongodb.com/try/download/community
   - Select: Windows, Latest Version
   - Download and run the installer

2. **Install MongoDB**
   - Choose "Complete" installation
   - Install "MongoDB as a Service" (recommended)
   - Keep default settings

3. **Verify Installation**
   ```bash
   mongod --version
   ```

4. **Start MongoDB Service** (if not auto-started)
   ```bash
   net start MongoDB
   ```

### Mac Installation

```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community@7.0

# Start MongoDB
brew services start mongodb-community@7.0
```

### Linux (Ubuntu/Debian) Installation

```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Create list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

## Option 2: Use MongoDB Atlas (Cloud - Free Tier Available)

1. **Create Account**
   - Visit: https://www.mongodb.com/cloud/atlas/register
   - Sign up for free

2. **Create Cluster**
   - Choose "Shared" (Free tier)
   - Select your preferred region
   - Click "Create Cluster"

3. **Setup Access**
   - Database Access: Add a database user with password
   - Network Access: Add your IP address (or 0.0.0.0/0 for testing)

4. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Example: `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/`

5. **Update config.py**
   ```python
   # Add this to config.py
   MONGODB_URI = "your-mongodb-atlas-connection-string"
   ```

6. **Update mongodb_handler.py**
   ```python
   # Change initialization in app.py
   from config import MONGODB_URI
   mongo_db = MongoDBHandler(connection_string=MONGODB_URI)
   ```

## Setup Knowledge Base

Once MongoDB is installed and running:

1. **Run the setup script**
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

2. **Verify the data**
   ```bash
   # Using MongoDB Shell (optional)
   mongosh
   use stansbooth_db
   db.knowledge_base.find().count()
   ```

## Run the Application

```bash
python app.py
```

Visit: http://127.0.0.1:5000

## Troubleshooting

### MongoDB Connection Failed

**Error:** `MongoDB connection failed: [Errno 10061] No connection could be made`

**Solutions:**
1. Check if MongoDB is running:
   ```bash
   # Windows
   net start MongoDB

   # Mac
   brew services list

   # Linux
   sudo systemctl status mongod
   ```

2. If using MongoDB Atlas, check:
   - Connection string is correct
   - Username/password are correct
   - IP address is whitelisted

### Setup Script Failed

**Error:** `⚠️ MongoDB is not running!`

**Solution:**
- Install MongoDB following steps above
- Start MongoDB service
- Run setup script again

### Port Already in Use

**Error:** Port 27017 already in use

**Solution:**
- MongoDB is already running (this is good!)
- Continue with setup script

## Fallback Mode (Without MongoDB)

If you can't install MongoDB right now, the chatbot will still work but without the StansBooth knowledge base. It will use only general AI responses.

To add MongoDB later:
1. Install MongoDB
2. Run `python setup_mongodb.py`
3. Restart the Flask app

## Data Structure

The knowledge base includes:
- ✓ Company information
- ✓ Services (6 services)
- ✓ Features (5 features)
- ✓ Pricing plans (5 plans)
- ✓ Trading sessions (3 sessions)
- ✓ FAQs (8 questions)
- ✓ Vision & mission
- ✓ Why choose StansBooth
- ✓ Blog posts

## Backup & Restore

### Backup MongoDB Data
```bash
mongodump --db stansbooth_db --out ./mongodb_backup
```

### Restore MongoDB Data
```bash
mongorestore --db stansbooth_db ./mongodb_backup/stansbooth_db
```

## Need Help?

- MongoDB Documentation: https://docs.mongodb.com/
- MongoDB University (Free): https://university.mongodb.com/
- StansBooth Support: Info@stansbooth.com

---

**Ready?** Run `python setup_mongodb.py` and you're all set! 🚀
