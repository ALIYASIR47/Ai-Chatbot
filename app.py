import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime, timedelta
from config import GEMINI_API_KEY

# ----------------- CONFIG -----------------
# Load Gemini API key from config file
genai.configure(api_key=GEMINI_API_KEY)

# ----------------- FLASK APP -----------------
app = Flask(__name__)

# Chat history file
HISTORY_FILE = "chat_history.json"

# ----------------- HELPER FUNCTIONS -----------------
def load_chat_history():
    """Load chat history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(history):
    """Save chat history to JSON file"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def add_to_history(user_msg, bot_msg):
    """Add a new conversation to history"""
    history = load_chat_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_msg
    })
    save_chat_history(history)

def ask_gemini(query):
    try:
        # Use the latest stable Gemini model
        model_gemini = genai.GenerativeModel("gemini-2.5-flash")
        response = model_gemini.generate_content(query)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API error: {str(e)}"

# ----------------- ROUTES -----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    msg = data.get("msg", "").strip()

    if not msg:
        return jsonify({"response": "Please type something."})

    # Get Gemini response
    gemini_res = ask_gemini(msg)

    # Save to history
    add_to_history(msg, gemini_res)

    return jsonify({"response": gemini_res})

@app.route("/history/<filter_type>", methods=["GET"])
def get_history(filter_type):
    """Get filtered chat history"""
    history = load_chat_history()
    now = datetime.now()

    filtered = []
    for chat in history:
        chat_time = datetime.fromisoformat(chat["timestamp"])

        if filter_type == "today":
            if chat_time.date() == now.date():
                filtered.append(chat)
        elif filter_type == "week":
            week_ago = now - timedelta(days=7)
            if week_ago <= chat_time < now - timedelta(days=1):
                filtered.append(chat)
        elif filter_type == "older":
            week_ago = now - timedelta(days=7)
            if chat_time < week_ago:
                filtered.append(chat)
        elif filter_type == "all":
            filtered = history
            break

    return jsonify({"history": filtered})

@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear all chat history"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({"status": "success"})

# ----------------- RUN -----------------
if __name__ == "__main__":
    # Use stat reloader to prevent monitoring site-packages
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=True, reloader_type='stat')
