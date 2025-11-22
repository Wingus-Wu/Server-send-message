from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
messages = []

# ================= Website HTML =================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Chat</title>
</head>
<body>
    <h1>Roblox Chat</h1>
    <div id="chat" style="height:300px; overflow-y:scroll; border:1px solid black;"></div>
    <input type="text" id="msg" placeholder="Type a message"/>
    <button onclick="sendMessage()">Send</button>

    <script>
        const chatDiv = document.getElementById("chat")
        const input = document.getElementById("msg")

        async function fetchMessages() {
            const res = await fetch("/get")
            const data = await res.json()
            chatDiv.innerHTML = ""
            data.forEach(msg => {
                const el = document.createElement("p")
                el.textContent = msg.username + ": " + msg.message
                chatDiv.appendChild(el)
            })
            chatDiv.scrollTop = chatDiv.scrollHeight
        }

        async function sendMessage() {
            const message = input.value
            if(!message) return
            await fetch("/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({username: "Website", message})
            })
            input.value = ""
            fetchMessages()
        }

        setInterval(fetchMessages, 2000)
        fetchMessages()
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()
        username = data.get("username", "Unknown")
        message = data.get("message", "")
        entry = {"username": username, "message": message, "time": datetime.utcnow().isoformat()}
        messages.append(entry)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get", methods=["GET"])
def get_messages():
    return jsonify(messages), 200

if __name__ == "__main__":
    app.run(debug=True)
