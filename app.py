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
SYSTEM_PROMPT = """You are a strict AI assistant ONLY for StansBooth, an AI-powered trading bot platform.

StansBooth provides automated algorithmic trading services for Forex, crypto, and stocks. Our mission is to make trading accessible, automated, and profitable for everyone - from professionals to beginners.

Key Services:
- Algorithmic Trading (MT5 & TradingView support)
- Copy Trading & Social Trading
- Education & Training
- Market Alerts & AI Signals
- Portfolio Monitoring
- Funds & Asset Management

STRICT RULES:
1. ONLY answer questions about StansBooth services, pricing, features, trading platforms, or related topics
2. If the question is about coding, general knowledge, other companies, or unrelated topics, respond with: "I can only answer questions about StansBooth services. Please ask about our trading bots, pricing plans, or features."
3. Refuse to answer questions about: programming, math problems, general knowledge, other websites, or anything not directly related to StansBooth
4. Always use the knowledge base information when available
5. Mention FREE Starter Plan when relevant

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
        query_lower = query.lower().strip()

        # Handle greetings with StansBooth intro
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if query_lower in greetings or any(query_lower.startswith(g) for g in greetings):
            return """Hello! Welcome to StansBooth - your AI-powered trading bot platform.

We provide automated algorithmic trading for Forex, Crypto, and Stocks. Whether you're a beginner or professional trader, we make trading accessible and profitable.

How can I help you today? You can ask me about:
- Our trading services and features
- Pricing plans (we have a FREE Starter Plan!)
- How our AI trading bot works
- Copy trading and signals

Feel free to ask any questions about StansBooth!"""

        # Get relevant context from knowledge base
        context = get_relevant_context(query)

        # Check if query is related to StansBooth
        stansbooth_keywords = ['stansbooth', 'trading', 'bot', 'forex', 'crypto', 'stock', 'price', 'plan',
                               'service', 'feature', 'signal', 'mt5', 'tradingview', 'algorithmic', 'copy trade',
                               'portfolio', 'fund', 'invest', 'profit', 'market', 'alert']

        is_stansbooth_related = any(keyword in query_lower for keyword in stansbooth_keywords) or len(context) > 0

        # If no context found and not stansbooth related, reject
        if not context and not is_stansbooth_related:
            return "I can only answer questions about StansBooth services. Please ask about our trading bots, pricing plans, features, or contact us at Info@stansbooth.com"

        # Build the prompt with system instructions and context
        if context:
            full_prompt = f"{SYSTEM_PROMPT}\n\n--- Relevant Knowledge Base Information ---\n{context}\n\n--- User Question ---\n{query}\n\nAnswer ONLY if this question is about StansBooth. If not related to StansBooth, respond with: 'I can only answer questions about StansBooth services.'"
        else:
            full_prompt = f"{SYSTEM_PROMPT}\n\n--- User Question ---\n{query}\n\nAnswer ONLY if this question is about StansBooth trading services. Otherwise respond: 'I can only answer questions about StansBooth services.'"

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

@app.route("/chat", methods=["POST"])
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
    # Get port from environment variable for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'

    if debug:
        # Development mode
        app.run(debug=True, host='127.0.0.1', port=port, use_reloader=True, reloader_type='stat')
    else:
        # Production mode
        app.run(host='0.0.0.0', port=port)
