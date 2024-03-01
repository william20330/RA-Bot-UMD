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
# Define a variable to track the last time a message was sent
last_message_sent_time = 0
# Define a cooldown period in seconds (e.g., 60 seconds)
cooldown_period = 60

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
    global bot_active, last_message_sent_time
    
    data = request.get_json()
    log('Received {}'.format(data))
    
    # Check if the message contains "/ra bot" to activate the bot
    if data['name'] != 'RA Bot' and '/ra bot' in data['text'].lower() and not bot_active:
        bot_active = True
        send_message('- Type /menu for more options and resources\n - Type /exit at anytime to leave the bot')
    # Check if the bot is active and respond to user commands
    elif bot_active:
        # Check if the cooldown period has elapsed since the last message was sent
        if time.time() - last_message_sent_time >= cooldown_period:
            if '/menu' in data['text'].lower():
                send_message('Here are the options (press number associated with choice): \
                            \n 1 - Phone Number for 4Work (issues regarding facilites, cleanliness, etc) \
                            \n 2 - Phone Number for the Cumberland Front Desk (contact RA on Duty, lockouts, etc) \
                            \n 3 - Hours of Operation For Dining Halls \
                            \n 4 - Important Links (ResLife, 4Work, etc)\
                            \n 5 - Important Dates (closues, breaks, finals, etc)\
                            \n 6 - UMD Sports Schedule/Scores')
            elif '1' in data['text'] and bot_active:
                send_message('Phone Number for 4Work: 301-314-9675')
                # Update the last message sent time
                last_message_sent_time = time.time()
            # Add other command cases here...
        else:
            # If the cooldown period hasn't elapsed, do not send any messages
            log("Cooldown period hasn't elapsed yet. Skipping message sending.")
    
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
