from flask import Flask, request, jsonify, render_template_string
import requests
import threading
import webbrowser

app = Flask(__name__)

OLLAMA_API_URL = "http://ollama-1:11434/api/generate"  # <-- service name, not localhost

# Store conversation in memory
conversation_history = []

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Chat</title>
    <style>
        body { background-color: #111827; color: #e0e0e0; font-family: Arial, sans-serif; }
        textarea { width: 80%; height: 80px; font-size: 16px; background-color: #1f2937; color: #fff; border: none; padding: 10px; border-radius: 5px; }
        input[type=submit] { padding: 10px 20px; font-size: 16px; background-color: #3b82f6; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        input[type=submit]:disabled { background-color: #6b7280; cursor: not-allowed; }
        #chatBox { border: 1px solid #374151; padding: 10px; width: 80%; max-height: 400px; overflow-y: auto; margin-bottom: 10px; background-color: #1f2937; border-radius: 5px; }
        .user { color: #0022ff; }
        .bot { color: #189900; }
        .thinking { font-style: italic; color: #8b0000; } 
    </style>
</head>
<body>
    <h2>Ollama Chat</h2>
    <div id="chatBox">
        {% for entry in conversation %}
            {% if entry.sender == 'user' %}
                <p class="user"><b>You:</b> {{entry.message}}</p>
            {% else %}
                <p class="bot"><b>Bot:</b> {{entry.message}}</p>
            {% endif %}
        {% endfor %}
    </div>
    <form id="chatForm" onsubmit="submitPrompt(event)">
        <textarea id="prompt" placeholder="Type your prompt here"></textarea><br>
        <input type="submit" id="submitBtn" value="Send">
    </form>
    
    <script>
        let isGenerating = false;

        function submitPrompt(event) {
            event.preventDefault();
            const promptInput = document.getElementById("prompt");
            const submitButton = document.getElementById("submitBtn");
            const chatBox = document.getElementById("chatBox");
            const promptText = promptInput.value.trim();
            if (!promptText) return;

            if (isGenerating) return; // prevent multiple submits
            isGenerating = true;
            submitButton.disabled = true;

            // Clear input immediately
            promptInput.value = "";

            chatBox.innerHTML += "<p class='user'><b>You:</b> " + promptText + "</p>";
            chatBox.innerHTML += "<p class='thinking'><i>Thinking...</i></p>";
            chatBox.scrollTop = chatBox.scrollHeight;

            fetch("/generate", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({prompt: promptText})
            })
            .then(response => response.json())
            .then(data => {
                chatBox.querySelector("p.thinking:last-child").remove();
                chatBox.innerHTML += "<p class='bot'><b>Bot:</b> " + (data.response || data.error) + "</p>";
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(err => {
                chatBox.querySelector("p.thinking:last-child").remove();
                chatBox.innerHTML += "<p class='bot'><b>Error:</b> " + err + "</p>";
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .finally(() => {
                isGenerating = false;
                submitButton.disabled = false;
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(html_template, conversation=conversation_history)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty."})

    # Add user message to conversation
    conversation_history.append({"sender": "user", "message": prompt})

    payload = {"model": "mistral", "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        bot_message = result.get("response", "")
    except Exception as e:
        bot_message = f"Error: {str(e)}"

    # Add bot response to conversation
    conversation_history.append({"sender": "bot", "message": bot_message})
    return jsonify({"response": bot_message})

if __name__ == "__main__":
    threading.Timer(1.5, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(host="0.0.0.0", port=5000)
