import requests
from flask import Flask, request, Response, jsonify
import re

app = Flask(__name__)

TOKEN = '6660002426:AAGPvSnzcppqv414X6ppk9wQYttaA0tT5Os'
SERVER_URL = "https://f234-147-235-200-167.ngrok.io"
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={SERVER_URL}'
requests.get(BASE_URL)
PORT = 5002


# Indicates the server is running.
@app.route('/sanity')
def sanity():
    return "Server is running"


# Extracts chat_id and text from the received message.
def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt


# Sends a message to a specific chat_id.
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'url': SERVER_URL,
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


# Handles incoming messages and responds accordingly.
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)

        if re.search(r'\bhi\b', txt, re.IGNORECASE):
            tel_send_message(chat_id, "Hello!!")
        elif re.search(r'\bhello\b', txt, re.IGNORECASE):
            tel_send_message(chat_id, "Hi there!")
        else:
            tel_send_message(chat_id, "Thank you for using BetterFarm Bot!")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


# Handles detected events and sends reports to the chat_id
@app.route('/detected', methods=['GET', 'POST'])
def report_detection():
    if request.method == 'POST':
        try:
            msg = request.get_json()
            text = msg.get('text', '')
            chat_id = msg.get('chat_id', '')

            response = tel_send_message(chat_id, text)
            if response.status_code == 200:
                print("Response sent successfully")
            print("Response:", response.text)

            return Response('ok', status=200)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return jsonify(error=error_message), 500
    else:
        return "<h1>Nothing to report.</h1>"


def run():
    app.run(port=PORT)


if __name__ == '__main__':
    run()

