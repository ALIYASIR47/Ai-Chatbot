# GitHub Repository Setup & Collaboration Guide

## Step 1: Create Repository on GitHub

### Option A: Create on Your Account (ALIYASIR47)

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name:** `stansbooth-chatbot`
   - **Description:** StansBooth AI Trading Chatbot with RAG
   - **Visibility:** Public or Private
   - **DO NOT** initialize with README, .gitignore, or license
3. Click **"Create repository"**

### Option B: Create via Command Line

If you have GitHub CLI installed:
```bash
gh repo create stansbooth-chatbot --public --source=. --remote=origin
```

## Step 2: Push Your Code

After creating the repository on GitHub:

```bash
# Push master branch
git checkout master
git push -u origin master

# Push yasir-devin branch
git checkout yasir-devin
git push -u origin yasir-devin
```

When prompted, enter:
- **Username:** `ALIYASIR47`
- **Password:** Your Personal Access Token (create at https://github.com/settings/tokens)

## Step 3: Collaborate with Stansbooth Organization

### Method 1: Get Added to Stansbooth Organization (Recommended)

1. **Ask Stansbooth owner** to invite you to the organization
2. They go to: https://github.com/orgs/Stansbooth/people
3. Click **"Invite member"**
4. Enter your email or username: `ALIYASIR47`
5. You accept the invitation from your email
6. Now you can create repositories directly under Stansbooth

### Method 2: Fork and Contribute

If you don't have organization access:

1. **Create repo in Stansbooth org** (if you have permission) or ask owner to create it
2. **Add your repo as a fork/contributor:**
   ```bash
   # Add Stansbooth repo as another remote
   git remote add stansbooth https://github.com/Stansbooth/chatbot.git

   # Push to both
   git push origin yasir-devin
   git push stansbooth yasir-devin
   ```

### Method 3: Transfer Repository Ownership

After creating on your account, transfer to Stansbooth:

1. Go to your repo: https://github.com/ALIYASIR47/stansbooth-chatbot
2. Settings → Danger Zone → Transfer ownership
3. Enter: `Stansbooth`
4. Stansbooth owner accepts the transfer

## Step 4: Team Workflow

### Working with Multiple Developers

```bash
# Your workflow
git checkout -b yasir-devin          # Your development branch
# Make changes
git add .
git commit -m "Your changes"
git push origin yasir-devin

# Create Pull Request on GitHub
# Team reviews and merges to master
```

### Keep Your Branch Updated

```bash
# Update from master
git checkout master
git pull origin master
git checkout yasir-devin
git merge master
```

## Repository Structure

```
ALIYASIR47/stansbooth-chatbot (Your personal repo)
    ├── master (main code)
    └── yasir-devin (your development branch)

Stansbooth/chatbot (Organization repo - after transfer/invite)
    ├── master (production)
    ├── yasir-devin (your branch)
    └── other-dev (other team members)
```

## Quick Commands

### Create repository and push (first time)

1. Create repository on GitHub: https://github.com/new
2. Run:
```bash
git remote add origin https://github.com/ALIYASIR47/stansbooth-chatbot.git
git push -u origin master
git push -u origin yasir-devin
```

### Daily workflow

```bash
# Start work
git checkout yasir-devin
git pull origin yasir-devin

# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Description of changes"
git push origin yasir-devin
```

## Current Remote Configuration

```bash
origin → https://github.com/ALIYASIR47/stansbooth-chatbot.git
```

## Next Steps

1. ✅ Create repository on GitHub (https://github.com/new)
2. ✅ Push code: `git push -u origin yasir-devin`
3. ✅ Contact Stansbooth owner for organization access
4. ✅ Transfer repo or set up dual remotes

## Contact Stansbooth

To collaborate with Stansbooth organization:
- Ask the organization owner to invite `ALIYASIR47` to the team
- Or ask them to create `Stansbooth/chatbot` repository and give you access
