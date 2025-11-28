# How to Run

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Configure Environment
```bash
copy .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY=your-key-from-google
```
Get key: https://makersuite.google.com/app/apikey

## 3. Setup MongoDB (Optional)
```bash
python setup_mongodb.py
```

## 4. Run Application
```bash
python app.py
```

## 5. Access
Open browser: http://127.0.0.1:5000

## Quick Start (No MongoDB)
```bash
pip install flask python-dotenv google-generativeai pymongo
copy .env.example .env
# Edit .env and add GEMINI_API_KEY
python app.py
```

## Troubleshooting
- MongoDB connection failed → App runs without knowledge base
- Invalid API key → Check `.env` file
- Port 5000 busy → Change port in `app.py`
