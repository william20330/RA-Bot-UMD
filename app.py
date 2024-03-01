import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log('Received {}'.format(data))

    # Check if the message contains "ra bot"
    if 'ra bot' in data['text'].lower() and data['name'] != 'ra bot':
        send_message('hi')

    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': os.getenv('d333dc538150f9a45a0072029b'),
        'text': msg,
    }
    request = Request(url, urlencode(data).encode())
    response = urlopen(request)
    log('Message sent: {}'.format(response.read().decode()))

def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__ == "__main__":
    app.run()
