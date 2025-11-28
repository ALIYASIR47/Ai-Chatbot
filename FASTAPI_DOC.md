# API Documentation

## Base URL

**Development**
```
http://127.0.0.1:5000
```

**Local Network Access**
```
http://<your-ip>:5000
```

**Protocol:** HTTP
**Port:** 5000
**Host:** 127.0.0.1 (localhost)

## Endpoints

### GET /
**URL:** `http://127.0.0.1:5000/`

Home page rendering

**Response**
HTML page

**Full Request Example**
```bash
curl http://127.0.0.1:5000/
```

---

### POST /chat
**URL:** `http://127.0.0.1:5000/chat`

Send message to AI chatbot

**Request Body**
```json
{
  "msg": "string"
}
```

**Response**
```json
{
  "response": "string"
}
```

**Full Request Example**
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"msg": "What is StansBooth?"}'
```

**JavaScript Example**
```javascript
fetch('http://127.0.0.1:5000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({msg: 'What is StansBooth?'})
})
.then(res => res.json())
.then(data => console.log(data.response));
```

**Python Example**
```python
import requests
response = requests.post('http://127.0.0.1:5000/chat',
  json={'msg': 'What is StansBooth?'})
print(response.json()['response'])
```

---

### GET /history/{filter_type}
**URL:** `http://127.0.0.1:5000/history/{filter_type}`

Get chat history

**Path Parameters**
- filter_type: `today` | `week` | `older` | `all`

**Response**
```json
{
  "history": [
    {
      "timestamp": "ISO8601 string",
      "user": "string",
      "bot": "string"
    }
  ]
}
```

**Full Request Examples**
```bash
# Get today's history
curl http://127.0.0.1:5000/history/today

# Get this week's history
curl http://127.0.0.1:5000/history/week

# Get older history
curl http://127.0.0.1:5000/history/older

# Get all history
curl http://127.0.0.1:5000/history/all
```

**JavaScript Example**
```javascript
fetch('http://127.0.0.1:5000/history/today')
  .then(res => res.json())
  .then(data => console.log(data.history));
```

**Python Example**
```python
import requests
response = requests.get('http://127.0.0.1:5000/history/today')
print(response.json()['history'])
```

---

### POST /clear-history
**URL:** `http://127.0.0.1:5000/clear-history`

Clear all chat history

**Response**
```json
{
  "status": "success"
}
```

**Full Request Example**
```bash
curl -X POST http://127.0.0.1:5000/clear-history
```

**JavaScript Example**
```javascript
fetch('http://127.0.0.1:5000/clear-history', {method: 'POST'})
  .then(res => res.json())
  .then(data => console.log(data.status));
```

**Python Example**
```python
import requests
response = requests.post('http://127.0.0.1:5000/clear-history')
print(response.json()['status'])
```

---

## Architecture

### RAG System
Retrieval-Augmented Generation using Gemini API and MongoDB

**Flow**
```
User Query → MongoDB Search → Context Retrieval → Gemini API → Response
```

### Components
- Flask web framework
- Google Gemini 2.5-flash model
- MongoDB knowledge base
- JSON chat history storage

### Knowledge Base Schema
```json
{
  "type": "faq | service | feature | pricing_plan | blog",
  "name": "string",
  "data": {}
}
```

### Context Retrieval
- Top 3 relevant results from MongoDB
- Text search across all collections
- Injected into Gemini prompt

---

## Configuration

### Environment Variables
```env
GEMINI_API_KEY=your_key_here
MONGODB_URI=mongodb://localhost:27017/
```

### Safety Settings
```python
HARM_CATEGORY_DANGEROUS_CONTENT: BLOCK_NONE
HARM_CATEGORY_HATE_SPEECH: BLOCK_ONLY_HIGH
HARM_CATEGORY_HARASSMENT: BLOCK_ONLY_HIGH
HARM_CATEGORY_SEXUALLY_EXPLICIT: BLOCK_ONLY_HIGH
```

---

## Files Structure
```
app.py - Main Flask application
mongodb_handler.py - Database operations
config.py - Environment configuration
chat_history.json - Conversation storage
knowledge_base.json - Initial KB data
setup_mongodb.py - Database initialization
templates/ - HTML templates
static/ - CSS/JS assets
```

---

## Error Handling
- Empty message: "Please type something."
- Blocked response: Content filter fallback message
- MongoDB unavailable: App runs without knowledge base
- API errors: User-friendly error messages

---

## Run Application
```bash
pip install -r requirements.txt
python app.py
```

Access at: http://127.0.0.1:5000
