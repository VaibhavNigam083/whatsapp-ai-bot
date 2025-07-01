from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ[EAAKcg8jtRJMBO1OUwIAvDqxCZA66Ombl8nwSBbfcjdZCZCFf7bVbSfJQjrmT2IZBN3ssIYvSpfuwoSMnDlfumoPOgv0j9PjTZAE2ZAwgKt3a1FaHZBoYVxy0nKC0mVBaHMgqVZAwZB6ZAeZC0hV3Q9iv1eDdpZCoPC1KduQHHUYZBbBU9ZAK2E610ZCQ901c91E5kiZBxaw1QpZC4BFHv0is2jaVMRuV6W1WDiwAbVbI1n5BLZA2d1we4ZD']
PHONE_NUMBER_ID = os.environ['697254740139276']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = message['from']
        text = message['text']['body']

        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        reply = response['choices'][0]['message']['content']

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
