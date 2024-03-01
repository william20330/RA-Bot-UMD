import os
import sys
import requests
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Function to check and send a holiday message
def check_and_send_holiday_message():
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
    data = request.get_json()
    log('Received {}'.format(data))
    text = data['text'].lower()

    if data['name'] != 'RA Bot':
        if '/ra bot' in text:
            send_message('Welcome to RA Bot! Choose an option:\n- /menu\n- /exit')
        elif '/exit' in text:
            send_message('Goodbye!')
            # Implement functionality to stop listening to chat messages here if needed
            # For now, we send a goodbye message. Stopping the bot would depend on the deployment setup.
        elif '/menu' in text:
            send_message('Here are the options:\n' +
                         '1 - Phone Number for 4Work (issues regarding facilities, cleanliness, etc)\n' +
                         '2 - Phone Number for the Cumberland Front Desk (contact RA on Duty, lockouts, etc)\n' +
                         '3 - Hours of Operation For Dining Halls\n' +
                         '4 - Important Links (ResLife, 4Work, etc)\n' +
                         '5 - Important Dates (closures, breaks, finals, etc)\n' +
                         '6 - UMD Sports Schedule/Scores')
        else:
            handle_commands(text)

    return "ok", 200

def handle_commands(text):
    if text == '1':
        send_message('Phone Number for 4Work: 301-314-9675')
    elif text == '2':
        send_message('Phone Number for the Cumberland Front Desk: 301-314-2862')
    # Add additional command handling here for options 3 through 6

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
