import os
import sys
import requests
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

app = Flask(__name__)
scheduler = BackgroundScheduler()
bot_active = False  # Variable to keep track of whether the bot is active or not
last_message_sent_time = 0  # Track the last time a message was sent
cooldown_period = 2  # Cooldown period in seconds
current_command = None 

def check_and_send_holiday_message():
    # Replace 'us' with the correct country code
    country_code = 'us'
    url = f'https://date.nager.at/Api/v3/IsTodayPublicHoliday/{country_code}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        holiday_data = response.json()

        if holiday_data['isPublicHoliday']:
            holiday_name = holiday_data['name']
            send_message(f"Happy {holiday_name}!")
    except requests.exceptions.RequestException as e:
        log(f"An error occurred: {e}")

# Function to start the scheduler
def start_scheduler():
    scheduler.add_job(check_and_send_holiday_message, 'cron', day_of_week='mon-sun', hour=9)
    scheduler.start()


@app.route('/', methods=['POST'])
def webhook():
    global bot_active, last_message_sent_time, current_command

    data = request.get_json()
    log('Received {}'.format(data))

    # Activation command
    if data['name'] != 'RA Bot' and '/ra bot' in data['text'].lower() and not bot_active:
        bot_active = True
        send_message('- Type /menu for more options and resources\n- Type /exit at any time to leave the bot')
        return "ok", 200

    if bot_active:
        if time.time() - last_message_sent_time >= cooldown_period:
            # Display the menu only when the '/menu' command is received
            if '/menu' in data['text'].lower():
                send_message('Here are the options (press number associated with choice): \
                              \n1 - Phone Number for 4Work (issues regarding facilities, cleanliness, etc) \
                              \n2 - Phone Number for the Cumberland Front Desk (contact RA on Duty, lockouts, etc) \
                              \n3 - Hours of Operation For Dining Halls \
                              \n4 - Important Links (ResLife, 4Work, etc)\
                              \n5 - Important Dates (closures, breaks, finals, etc)\
                              \n6 - UMD Sports Schedule/Scores')
                last_message_sent_time = time.time()
                # Do not set current_command here; let it wait for the next input
                return "ok", 200

            # Handle the options only if they are selected after the menu has been requested
            # It's safer to check directly for the text instead of using a state variable here
            # since the previous issue was caused by mismanaging the state
            if '1' in data['text']:
                send_message('Phone Number for 4Work: 301-314-9675')
                last_message_sent_time = time.time()
            elif '2' in data['text']:
                send_message('Phone Number for the Cumberland Front Desk: 301-314-2862')
                last_message_sent_time = time.time()
            # Include conditions for other options here...

            if '/exit' in data['text'].lower():
                send_message('Goodbye!')
                bot_active = False
                last_message_sent_time = time.time()

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
    start_scheduler()
    app.run()
