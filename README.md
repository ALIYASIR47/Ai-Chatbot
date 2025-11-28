# StansBooth AI Chatbot

AI-powered chatbot for StansBooth trading platform with RAG (Retrieval-Augmented Generation) using Google Gemini API and MongoDB knowledge base.

## Features

- AI-powered responses using Google Gemini 2.5-flash
- MongoDB knowledge base integration (FAQs, services, pricing)
- Context-aware responses with RAG architecture
- Chat history with filtering (today/week/older/all)
- RESTful API endpoints
- Production-ready with Gunicorn support
- Clean, responsive web interface

## Tech Stack

- **Backend:** Flask (Python)
- **AI Model:** Google Gemini 2.5-flash
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Gunicorn, Render/Railway/Heroku ready

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017/
```

Get Gemini API key: https://makersuite.google.com/app/apikey

### 3. Setup MongoDB (Optional)

MongoDB provides the knowledge base. The app works without it but with reduced functionality.

```bash
python setup_mongodb.py
```

### 4. Run Application

```bash
python app.py
```

Visit: http://127.0.0.1:5000

## API Documentation

Complete API documentation available in [FASTAPI_DOC.md](FASTAPI_DOC.md)

### Endpoints

- `GET /` - Web interface
- `POST /chat` - Send message to chatbot
- `GET /history/{filter_type}` - Get chat history
- `POST /clear-history` - Clear all history

### Example Request

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"msg": "What is StansBooth?"}'
```

## Project Structure

```
AI_Chatbot/
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── mongodb_handler.py     # MongoDB operations
├── setup_mongodb.py       # Database initialization
├── requirements.txt       # Python dependencies
├── Procfile              # Production deployment
├── .env                  # Environment variables (not in git)
├── templates/            # HTML templates
│   └── index.html
├── static/              # CSS, JS, images
│   ├── style.css
│   └── script.js
├── FASTAPI_DOC.md       # Complete API documentation
├── DEPLOYMENT.md        # Deployment guide
├── RUN_GUIDE.md         # How to run locally
└── GITHUB_SETUP.md      # GitHub collaboration guide
```

## Documentation

- **[FASTAPI_DOC.md](FASTAPI_DOC.md)** - Complete API reference with examples
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to Render, Railway, Heroku, PythonAnywhere
- **[RUN_GUIDE.md](RUN_GUIDE.md)** - Local setup and troubleshooting
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - GitHub collaboration workflow

## Deployment

### Deploy to Render (Free)

1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service → Connect repository
4. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
5. Add environment variables (GEMINI_API_KEY, MONGODB_URI)
6. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GEMINI_API_KEY | Yes | Google Gemini API key |
| MONGODB_URI | No | MongoDB connection string (default: localhost) |
| PORT | No | Server port (default: 5000) |
| FLASK_ENV | No | development/production (default: development) |

## Architecture

### RAG System

```
User Query → MongoDB Search → Context Retrieval → Gemini API → Response
                                     ↓
                              History Storage
```

The chatbot uses Retrieval-Augmented Generation:
1. User sends a query
2. System searches MongoDB for relevant context (FAQs, services, pricing)
3. Top 3 results are injected into Gemini prompt
4. Gemini generates contextually aware response
5. Conversation saved to history

## Development

### Run in Development Mode

```bash
python app.py
```

Server runs on http://127.0.0.1:5000 with debug mode and auto-reload.

### Run in Production Mode

```bash
export FLASK_ENV=production
gunicorn app:app
```

Or use the included Procfile:
```bash
web: gunicorn app:app
```

## Requirements

- Python 3.8+
- MongoDB (optional, for knowledge base)
- Gemini API key

## Knowledge Base

MongoDB stores:
- FAQs (Frequently Asked Questions)
- Services (Trading services offered)
- Features (Platform features)
- Pricing Plans (Subscription tiers)
- Blog Posts (Educational content)

Schema:
```json
{
  "type": "faq|service|feature|pricing_plan|blog",
  "name": "string",
  "data": {}
}
```

## Troubleshooting

**MongoDB Connection Failed**
- Check MongoDB is running: `mongod`
- Verify MONGODB_URI in .env
- App works without MongoDB (reduced functionality)

**Gemini API Errors**
- Verify API key is correct
- Check API quota at https://makersuite.google.com
- Content filters may block some responses

**Port Already in Use**
- Change PORT in .env or app.py
- Kill existing process: `lsof -ti:5000 | xargs kill`

See [RUN_GUIDE.md](RUN_GUIDE.md) for more troubleshooting.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for collaboration workflow.

## License

This project is proprietary software owned by StansBooth.

## Contact

**StansBooth**
- Website: https://stansbooth.com
- Email: Info@stansbooth.com

## Credits

Developed by Yasir (ALIYASIR47) for StansBooth trading platform.

---

© 2025 StansBooth. All rights reserved.
