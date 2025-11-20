# AI Chatbot - Gemini Powered

A beautiful, modern AI chatbot powered by Google's Gemini 2.5 Flash model with chat history management and a stunning UI.

![AI Chatbot](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-orange)

## Features

- **Modern UI Design**
  - Animated gradient background with glassmorphic effects
  - Robot avatar icons throughout the interface
  - Smooth animations and transitions
  - Responsive design (works on mobile!)

- **Chat History Management**
  - Sidebar with organized chat history
  - Filter by time period (Today, Previous Week, Older, All)
  - Click any chat to reload conversation
  - Clear history functionality
  - Persistent storage using JSON

- **User Experience**
  - Typing indicator with animated dots
  - Message bubbles with avatars
  - Welcome screen
  - Auto-scrolling chat
  - Enter key to send messages

## Technologies Used

- **Backend:** Flask (Python)
- **AI Model:** Google Gemini 2.5 Flash
- **Frontend:** HTML5, CSS3, JavaScript
- **Storage:** JSON file-based chat history

## Installation

### Prerequisites

- Python 3.11 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd AI_Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Copy `config.example.py` to `config.py`
   ```bash
   copy config.example.py config.py
   ```
   - Edit `config.py` and add your Gemini API key:
   ```python
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to: `http://127.0.0.1:5000`

## Project Structure

```
AI_Chatbot/
├── app.py                    # Main Flask application
├── config.py                 # API key configuration (not in Git)
├── config.example.py         # Template for config file
├── requirements.txt          # Python dependencies
├── chat_history.json         # Chat history storage (auto-created)
├── templates/
│   └── index.html           # Main HTML template
├── static/
│   ├── style.css            # Styling and animations
│   └── script.js            # Frontend JavaScript
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Usage

### Starting a Conversation
1. Type your message in the input box at the bottom
2. Press Enter or click the Send button
3. The AI will respond using Gemini 2.5 Flash

### Viewing Chat History
1. Click the menu icon (☰) to open the sidebar
2. Use the filter buttons to view chats by time period:
   - **Today:** Chats from today
   - **Previous Week:** Chats from the last 7 days
   - **Older:** Chats older than 7 days
   - **All:** View all chat history
3. Click any chat to reload that conversation

### Clearing History
- Click the "Clear All History" button at the bottom of the sidebar
- Confirm the action to delete all chat history

## Recovery & Backup

This project uses Git for version control. To restore to a previous working state:

```bash
# View commit history
git log

# Restore to last commit (discard changes)
git checkout .

# Restore to specific commit
git checkout <commit-hash>
```

## Customization

### Change Background Colors
Edit `static/style.css` - Look for the gradient definitions:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change AI Model
Edit `app.py` and modify the model name:
```python
model_gemini = genai.GenerativeModel("gemini-2.5-flash")
```

Available models: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash, etc.

## Troubleshooting

### API Key Error
- Make sure you've created `config.py` from `config.example.py`
- Verify your API key is correct and active
- Check that you have API quota remaining

### Port Already in Use
- Change the port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Chat History Not Saving
- Check that the application has write permissions in the directory
- Ensure `chat_history.json` is not being blocked by antivirus

## Security Notes

- Never commit `config.py` to Git (it contains your API key)
- Keep your Gemini API key private
- The `.gitignore` file prevents accidental commits of sensitive data
- Chat history is stored locally and not shared

## License

This project is free to use for personal and educational purposes.

## Credits

- Built with Flask
- Powered by Google Gemini AI
- UI inspired by modern chat applications

## Support

For issues or questions, check the configuration and ensure all dependencies are installed correctly.

---

**Enjoy your AI Assistant!** 🤖
