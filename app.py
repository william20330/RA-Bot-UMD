import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Variable to track if the bot is active
bot_active = False

# Define a route to handle GroupMe callbacks
@app.route('/callback', methods=['POST'])
def callback():
    global bot_active
    data = request.get_json()

    # Ensure the request is from GroupMe
    if 'text' in data and 'group_id' in data:
        message_text = data['text'].lower()
        group_id = data['group_id']

        if message_text == 'raBot':
            bot_active = True
            send_message(group_id, "RA Bot is now active. Please select an option from the menu.")
        elif bot_active:
            if message_text == '1':
                send_message(group_id, "Number for 4Work (Facilities Issues, Hygiene Issues, etc): 301-314-9675")
            elif message_text == '2':
                send_message(group_id, "UMD Dining Hall Hours: Monday - Friday: 7:00 am - 8:00 pm")
            elif message_text == '3':
                bot_active = False
                send_message(group_id, "RA Bot has been deactivated.")
            else:
                send_message(group_id, "Invalid option. Please select a valid option.")
        
    return jsonify({'status': 'success'})

# Function to send a message to a GroupMe group
def send_message(group_id, text):
    bot_id = os.getenv('GROUPME_BOT_ID')
    url = f'https://api.groupme.com/v3/bots/post'

    payload = {
        'bot_id': bot_id,
        'text': text,
        'attachments': []
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

if __name__ == '__main__':
    app.run(debug=True)
