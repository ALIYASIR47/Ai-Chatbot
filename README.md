# StansBooth AI Assistant

AI-powered chatbot for StansBooth trading platform support.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
copy .env.example .env
```

3. Edit `.env` and add your Gemini API key

4. Setup MongoDB (optional):
```bash
python setup_mongodb.py
```

5. Run:
```bash
python app.py
```

Visit: http://127.0.0.1:5000

## Requirements

- Python 3.11+
- MongoDB (local or Atlas)
- Gemini API key

## Environment Variables

Required in `.env` file:
- `GEMINI_API_KEY` - Get from https://makersuite.google.com/app/apikey
- `MONGODB_URI` - Optional, defaults to localhost

---

© 2025 StansBooth - Info@stansbooth.com
