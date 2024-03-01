import os
import sys
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log('Received {}'.format(data))

    # Check if the message contains "ra bot"
    if 'ra bot' in data['text'].lower() and data['name'] != 'RA Bot':
        send_message('hi')

    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': os.getenv('GROUPME_BOT_ID'),
        'text': msg,
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    log('Message sent: {}'.format(response.text))

def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__ == "__main__":
    app.run()
