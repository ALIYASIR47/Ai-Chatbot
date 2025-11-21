import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime, timedelta
from config import GEMINI_API_KEY
from mongodb_handler import MongoDBHandler

# ----------------- CONFIG -----------------
# Load Gemini API key from config file
genai.configure(api_key=GEMINI_API_KEY)

# ----------------- FLASK APP -----------------
app = Flask(__name__)

# Chat history file
HISTORY_FILE = "chat_history.json"

# Initialize MongoDB connection
mongo_db = MongoDBHandler()

# System prompt for StansBooth context
SYSTEM_PROMPT = """You are a helpful AI assistant for StansBooth, an AI-powered trading bot platform.

StansBooth provides automated algorithmic trading services for Forex, crypto, and stocks. Our mission is to make trading accessible, automated, and profitable for everyone - from professionals to beginners.

Key Services:
- Algorithmic Trading (MT5 & TradingView support)
- Copy Trading & Social Trading
- Education & Training
- Market Alerts & AI Signals
- Portfolio Monitoring
- Funds & Asset Management

When answering questions:
1. Be professional, friendly, and helpful
2. If asked about StansBooth services, pricing, or features, use the knowledge base information provided
3. For general questions, provide helpful answers while maintaining StansBooth's professional tone
4. Always encourage users to learn more about our services when relevant
5. Mention that we offer a FREE Starter Plan for beginners

Contact: Info@stansbooth.com | Website: stansbooth.com
"""

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

def get_relevant_context(query):
    """Get relevant context from MongoDB knowledge base"""
    if not mongo_db.is_connected():
        return ""

    # Search knowledge base
    results = mongo_db.search_knowledge(query, limit=3)

    if not results:
        return ""

    # Build context string
    context_parts = []
    for result in results:
        result_type = result.get("type", "")
        data = result.get("data", {})

        if result_type == "faq":
            context_parts.append(f"Q: {data.get('question', '')}\nA: {data.get('answer', '')}")
        elif result_type == "service":
            context_parts.append(f"Service - {data.get('name', '')}: {data.get('description', '')}")
        elif result_type == "feature":
            context_parts.append(f"Feature - {data.get('name', '')}: {data.get('description', '')}")
        elif result_type == "pricing_plan":
            plan_name = data.get('name', '')
            monthly = data.get('monthly_price', 'N/A')
            yearly = data.get('yearly_price', 'N/A')
            features = ', '.join(data.get('features', [])[:3])
            context_parts.append(f"Plan - {plan_name}: ${monthly}/month, ${yearly}/year. Features: {features}...")

    return "\n\n".join(context_parts)

def ask_gemini(query):
    try:
        # Get relevant context from knowledge base
        context = get_relevant_context(query)

        # Build the prompt with system instructions and context
        if context:
            full_prompt = f"{SYSTEM_PROMPT}\n\n--- Relevant Knowledge Base Information ---\n{context}\n\n--- User Question ---\n{query}\n\nPlease answer based on the knowledge base information provided above. If the information isn't sufficient, you can supplement with general knowledge while staying true to StansBooth's services."
        else:
            full_prompt = f"{SYSTEM_PROMPT}\n\n--- User Question ---\n{query}\n\nPlease provide a helpful answer while maintaining StansBooth's professional and friendly tone."

        # Use the latest stable Gemini model with safety settings
        model_gemini = genai.GenerativeModel("gemini-2.5-flash")

        # Configure safety settings to be more permissive for trading/financial content
        safety_settings = {
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH",
        }

        response = model_gemini.generate_content(
            full_prompt,
            safety_settings=safety_settings
        )

        # Check if response was blocked
        if not response.parts:
            # Check finish reason
            if hasattr(response, 'prompt_feedback'):
                return "I apologize, but I couldn't generate a response due to content filters. Please try rephrasing your question. If you're asking about StansBooth services, feel free to ask about pricing, features, or trading strategies."
            return "I apologize, but I couldn't generate a response. Please try asking your question in a different way."

        return response.text.strip()

    except AttributeError as e:
        # Handle blocked response specifically
        return "I apologize, but your question triggered content filters. If you're asking about StansBooth trading services, please rephrase and I'll be happy to help!"
    except Exception as e:
        error_msg = str(e)
        if "finish_reason" in error_msg or "blocked" in error_msg.lower():
            return "I couldn't process that request due to safety filters. Please rephrase your question about StansBooth services, and I'll be happy to assist!"
        return f"I encountered an error: {error_msg}. Please try again or contact support at Info@stansbooth.com"

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
