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
cooldown_period = 5  # Cooldown period in seconds
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

    if data['name'] != 'RA Bot' and '/ra bot' in data['text'].lower() and not bot_active:
        bot_active = True
        current_command = 'menu'  # Set the initial command state to 'menu'
        send_message('- Type /menu for more options and resources\n - Type /exit at any time to leave the bot')
        return "ok", 200

    if bot_active:
        if time.time() - last_message_sent_time >= cooldown_period:
            # Only show the menu if the '/menu' command is received or it's the initial state after activation
            if ('/menu' in data['text'].lower() or current_command == 'menu') and current_command != 'exit':
                send_message('Here are the options (press number associated with choice): \
                              \n 1 - Phone Number for 4Work (issues regarding facilities, cleanliness, etc) \
                              \n 2 - Phone Number for the Cumberland Front Desk (contact RA on Duty, lockouts, etc) \
                              \n 3 - Hours of Operation For Dining Halls \
                              \n 4 - Important Links (ResLife, 4Work, etc)\
                              \n 5 - Important Dates (closures, breaks, finals, etc)\
                              \n 6 - UMD Sports Schedule/Scores')
                current_command = 'waiting_for_choice'  # Update state to wait for user's choice
                last_message_sent_time = time.time()
                return "ok", 200

            if current_command == 'waiting_for_choice':
                if '1' in data['text']:
                    send_message('Phone Number for 4Work: 301-314-9675')
                elif '2' in data['text']:
                    send_message('Phone Number for the Cumberland Front Desk: 301-314-2862')
                elif '3' in data['text']:
                    # Example response for option 3
                    pass
                # Include additional elif blocks for options 4, 5, 6...
                current_command = None  # Reset command state to allow new commands
                last_message_sent_time = time.time()

            if '/exit' in data['text'].lower():
                send_message('Goodbye!')
                bot_active = False
                current_command = None  # Reset command state
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
