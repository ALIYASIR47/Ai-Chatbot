# Security Checklist - Before Pushing to GitHub

## ✅ Verification Steps

Run these checks before pushing to GitHub:

### 1. Check .env is NOT in Git
```bash
git ls-files | grep ".env"
```
**Should return**: Nothing (empty)

If it shows `.env`, STOP and run:
```bash
git rm --cached .env
git commit -m "Remove .env from Git"
```

### 2. Check config.py is NOT in Git
```bash
git ls-files | grep "config.py"
```
**Should return**: Nothing (empty)

If it shows `config.py`, STOP and run:
```bash
git rm --cached config.py
git commit -m "Remove config.py from Git"
```

### 3. Verify .gitignore includes sensitive files
```bash
type .gitignore
```
**Should include**:
- `config.py`
- `.env`
- `.env.local`
- `.env.production`
- `*.key`
- `*.pem`

### 4. Check for API keys in code
```bash
git grep -i "AIzaSy"
```
**Should return**: Nothing in tracked files

If found, you need to remove them from code!

### 5. Verify .env.example has NO real keys
```bash
type .env.example
```
**Should show**: `your-gemini-api-key-here` (template only)

## 🔐 Files That Should NEVER Be in Git

- ❌ `.env` - Your actual environment variables
- ❌ `config.py` - Contains API key loading logic
- ❌ `chat_history.json` - User chat data
- ❌ `*.key` / `*.pem` - Any key files
- ❌ MongoDB backups

## ✅ Files That ARE Safe to Commit

- ✓ `.env.example` - Template file only
- ✓ `config.example.py` - Template file only
- ✓ `.gitignore` - Protects sensitive files
- ✓ All code files (app.py, templates, static)
- ✓ Documentation (README.md, etc.)

## 🚨 Emergency: If You Accidentally Committed Keys

### If you already pushed to GitHub:

1. **Rotate your API keys immediately!**
   - Get new Gemini API key: https://makersuite.google.com/app/apikey
   - Update your `.env` file

2. **Remove from Git history**:
   ```bash
   # Remove the file from all commits
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push
   git push origin --force --all
   ```

3. **Verify on GitHub**:
   - Check your repo to ensure keys are gone
   - Even from commit history!

## 📋 Pre-Push Checklist

Before running `git push origin main`:

- [ ] Ran `git grep -i "AIzaSy"` (no results)
- [ ] Checked `.env` is not in `git ls-files`
- [ ] Checked `config.py` is not in `git ls-files`
- [ ] Verified `.gitignore` includes `.env` and `config.py`
- [ ] `.env.example` contains only templates
- [ ] Local `.env` file has your real API key
- [ ] Tested app locally with `python app.py`

## 🎯 Safe to Push!

If all checks pass, you can safely push:

```bash
git push origin main
```

Your API keys will remain secure on your local machine only!

## 🔄 Setting Up on New Machine

When cloning the repo on a new machine:

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/stansbooth-ai-chatbot.git
cd stansbooth-ai-chatbot
```

2. Copy `.env.example` to `.env`
```bash
copy .env.example .env
```

3. Edit `.env` and add your actual API key
```
GEMINI_API_KEY=your-actual-key-here
```

4. Install dependencies and run
```bash
pip install -r requirements.txt
python app.py
```

## 📞 Questions?

If you're unsure about security, DON'T push to GitHub until you've verified!

Contact: Info@stansbooth.com
