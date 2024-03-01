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
    # Encode data as JSON instead of using urlencode
    request = Request(url, json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    response = urlopen(request)
    log('Message sent: {}'.format(response.read().decode()))

def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__ == "__main__":
    app.run()
