import os
import sys
from urllib.parse import urlencode
from urllib.request import urlopen
from flask import Flask, Request, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log('Recieved {}'.format(data))

  # We don't want to reply to ourselves!
  if data['name'] != 'ra-bot-umdt':
    msg = '{}, you sent "{}".'.format(data['name'], data['text'])
    send_message(msg)

  return "ok", 200

def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()
  
def log(msg):
  print(str(msg))
  sys.stdout.flush()
