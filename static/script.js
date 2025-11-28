// Global variables
let currentFilter = 'today';
let isFirstMessage = true;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadHistory('today');

    // Add click handlers to example questions
    document.querySelectorAll('.example-question').forEach(question => {
        question.addEventListener('click', function() {
            const text = this.textContent.replace(/['"]/g, ''); // Remove quotes
            document.getElementById('user-input').value = text;
            sendMessage();
        });
    });
});

// Toggle sidebar (mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

// Send message function
async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();
    const sendBtn = document.getElementById("send-btn");

    if (!message) return;

    // Hide welcome message on first message
    if (isFirstMessage) {
        const welcomeMsg = document.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.style.display = 'none';
        }
        isFirstMessage = false;
    }

    // Disable input and button
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message
    appendMessage("user", message);
    userInput.value = "";

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ msg: message })
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response
        appendMessage("bot", data.response);

        // Reload history
        loadHistory(currentFilter);

    } catch (err) {
        removeTypingIndicator();
        appendMessage("bot", "⚠️ Error contacting server. Please try again.");
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Append message to chat
function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    if (sender === "user") {
        messageDiv.innerHTML = `
            <div class="message-content">${escapeHtml(text)}</div>
            <div class="user-avatar">U</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="bot-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    <circle cx="9" cy="16" r="1"></circle>
                    <circle cx="15" cy="16" r="1"></circle>
                </svg>
            </div>
            <div class="message-content">${formatBotMessage(text)}</div>
        `;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const chatBox = document.getElementById("chat-box");
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot typing-message";
    typingDiv.innerHTML = `
        <div class="bot-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                <circle cx="9" cy="16" r="1"></circle>
                <circle cx="15" cy="16" r="1"></circle>
            </svg>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingMsg = document.querySelector('.typing-message');
    if (typingMsg) {
        typingMsg.remove();
    }
}

// Format bot message (preserve line breaks, etc.)
function formatBotMessage(text) {
    // Replace line breaks with <br>
    text = escapeHtml(text);
    text = text.replace(/\n/g, '<br>');
    return text;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Filter history
function filterHistory(filter, btnElement) {
    currentFilter = filter;

    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (btnElement) {
        btnElement.classList.add('active');
    }

    // Load filtered history
    loadHistory(filter);
}

// Load chat history
async function loadHistory(filter) {
    try {
        const response = await fetch(`/history/${filter}`);
        const data = await response.json();

        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';

        if (data.history.length === 0) {
            historyList.innerHTML = '<div style="padding: 20px; text-align: center; color: #999; font-size: 14px;">No chat history</div>';
            return;
        }

        // Display history items (reverse to show newest first)
        data.history.reverse().forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';

            const timestamp = new Date(item.timestamp);
            const timeStr = formatTimestamp(timestamp);

            historyItem.innerHTML = `
                <div class="history-item-text">${escapeHtml(item.user)}</div>
                <div class="history-item-time">${timeStr}</div>
            `;

            historyItem.onclick = () => loadConversation(item);
            historyList.appendChild(historyItem);
        });

    } catch (err) {
        console.error('Error loading history:', err);
    }
}

// Load a specific conversation into chat
function loadConversation(item) {
    // Hide welcome message
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
    isFirstMessage = false;

    // Clear current chat (except welcome message)
    const chatBox = document.getElementById('chat-box');
    const messages = chatBox.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());

    // Add the conversation
    appendMessage('user', item.user);
    appendMessage('bot', item.bot);

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        toggleSidebar();
    }
}

// Clear all history
async function clearHistory() {
    if (!confirm('Are you sure you want to clear all chat history? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/clear-history', {
            method: 'POST'
        });

        if (response.ok) {
            // Reload history
            loadHistory(currentFilter);

            // Clear chat display
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = `
                <div class="welcome-message">
                    <div class="bot-avatar-large">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                            <circle cx="9" cy="16" r="1"></circle>
                            <circle cx="15" cy="16" r="1"></circle>
                        </svg>
                    </div>
                    <h2>Welcome to AI Assistant</h2>
                    <p>I'm here to help you with any questions or tasks. How can I assist you today?</p>
                </div>
            `;
            isFirstMessage = true;

            alert('Chat history cleared successfully!');
        }
    } catch (err) {
        console.error('Error clearing history:', err);
        alert('Failed to clear history. Please try again.');
    }
}

// Format timestamp
function formatTimestamp(date) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const dateToCheck = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    const timeStr = date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });

    if (dateToCheck.getTime() === today.getTime()) {
        return `Today at ${timeStr}`;
    } else if (dateToCheck.getTime() === yesterday.getTime()) {
        return `Yesterday at ${timeStr}`;
    } else if (now - date < 7 * 24 * 60 * 60 * 1000) {
        const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        return `${days[date.getDay()]} at ${timeStr}`;
    } else {
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        }) + ` at ${timeStr}`;
    }
}

// Handle Enter key
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    if (userInput) {
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }
});
