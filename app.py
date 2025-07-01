from flask import Flask, request
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ['WHATSAPP_TOKEN']
PHONE_NUMBER_ID = os.environ['PHONE_NUMBER_ID']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

# Set your Copilot Studio webhook URL (Power Automate HTTP Request trigger)
COPILOT_WEBHOOK_URL = os.environ['COPILOT_WEBHOOK_URL']  # Set this in Render

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = message['from']
        user_text = message['text']['body']

        # Send message to Microsoft Copilot Studio via Power Automate HTTP POST
        copilot_response = requests.post(
            COPILOT_WEBHOOK_URL,
            json={"text": user_text}
        )

        if copilot_response.status_code == 200:
            copilot_data = copilot_response.json()
            reply = copilot_data.get('reply', 'Sorry, I did not understand that.')
        else:
            reply = "Bot error: could not get response."

        # Send reply via WhatsApp
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "text": {"body": reply}
        }
        requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print(f"Error: {e}")

    return "OK", 200

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403
