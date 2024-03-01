import os
import sys
from urllib.request import urlopen
import requests
from flask import Flask, Request, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log('Received {}'.format(data))

    # Check if the message contains "ra bot"
    if '/ra' in data['text'].lower() and data['name'] != 'RA Bot':
        send_message('hi')

    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': os.getenv('GROUPME_BOT_ID'),
        'text': msg,
    }
    data = json.dumps(data).encode('utf-8')  # Encode the data to bytes
    request = Request(url, data)  # Create the request object with data
    request.add_header('Content-Type', 'application/json')  # Correct way to add headers

    response = urlopen(request)
    log('Message sent: {}'.format(response.read().decode()))

def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__ == "__main__":
    app.run()
