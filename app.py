from flask import Flask, request, jsonify
import requests

# ==============================
# CONFIGURATION - EDIT THESE
# ==============================

WHATSAPP_TOKEN = "YOUR_META_ACCESS_TOKEN"      # Meta WhatsApp Cloud API token
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"      # Your WhatsApp phone number ID
VERIFY_TOKEN = "my_secret_token"              # Used for webhook verification
COHERE_API_KEY = "YOUR_COHERE_API_KEY"        # Cohere API key

# ==============================
# FLASK APP
# ==============================

app = Flask(__name__)

# Optional: Keep track of last messages for debugging
last_user_message = ""
last_ai_reply = ""

# ==============================
# COHERE CHAT FUNCTION
# ==============================

def chat_with_cohere(user_message):
    """
    Send user message to Cohere Chat API and return AI reply
    """
    url = "https://api.cohere.ai/v1/chat"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "command-r-plus",  # Latest chat model
        "message": user_message,
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res_data = res.json()
        return res_data.get("text", "Sorry, I couldn't respond.")
    except Exception as e:
        print("Cohere API error:", e)
        return "Sorry, I had trouble replying."

# ==============================
# SEND MESSAGE TO WHATSAPP
# ==============================

def send_whatsapp_message(to, text):
    """
    Send a message back to WhatsApp user
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    try:
        requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print("Error sending message:", e)

# ==============================
# WEBHOOK VERIFY (GET)
# ==============================

@app.route("/webhook", methods=["GET"])
def verify():
    """
    WhatsApp webhook verification
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200

    return "Verification failed", 403

# ==============================
# RECEIVE MESSAGES (POST)
# ==============================

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle incoming messages from WhatsApp
    """
    global last_user_message, last_ai_reply

    data = request.json

    try:
        # Parse incoming message
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"]

        last_user_message = text
        print("Received message:", text)

        # Get AI reply
        last_ai_reply = chat_with_cohere(text)
        print("AI reply:", last_ai_reply)

        # Send reply to WhatsApp
        send_whatsapp_message(sender, last_ai_reply)

    except Exception as e:
        print("Webhook error:", e)

    return jsonify(status="ok")

# ==============================
# RUN FLASK APP
# ==============================

if __name__ == "__main__":
    print("Starting WhatsApp AI bot...")
    app.run(port=5000)