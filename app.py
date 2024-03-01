import os
import sys
import requests
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
scheduler = BackgroundScheduler()

app = Flask(__name__)
scheduler = BackgroundScheduler()

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
    data = request.get_json()
    log('Received {}'.format(data))
    bot_active = False
    # Check if the message contains "ra bot"
    if data['name'] != 'RA Bot' and '/ra bot' in data['text'].lower() and not bot_active:
        bot_active = True
        send_message('- Type /menu for more options and resources\n - Type /exit at anytime to leave the bot')
        if '/menu' in data['text'].lower() and bot_active:
            send_message('Here are the options (press number associated with choice): \
                        \n 1 - Phone Number for 4Work (issues regarding facilites, cleanliness, etc) \
                        \n 2 - Phone Number for the Cumberland Front Desk (contact RA on Duty, lockouts, etc) \
                        \n 3 - Hours of Operation For Dining Halls \
                        \n 4 - Important Links (ResLife, 4Work, etc)\
                        \n 5 - Important Dates (closues, breaks, finals, etc)\
                        \n 6 - UMD Sports Schedule/Scores')
        if '1' in data['text'] and bot_active:
            send_message('Phone Number for 4Work: 301-314-9675')
        if '2' in data['text'] and bot_active:
            send_message('Phone Number for the Cumberland Front Desk: 301-314-2862')
        if '3' in data['text']and bot_active:
            send_message('Dining Hall Hours: \
                        \n Yahentamitsi: Monday - Friday: 7:00am - 9:00pm | Saturday - Sunday: 10:00am - 9:00pm\
                        \n 251 North: Monday - Thursday: 8:00am - 10:00pm | Friday - Sunday: 8:00am - 7:00pm\
                        \n South Campus: Monday - Friday: 7:00am - 9:00pm | Saturday - Sunday: 10:00am - 9:00pm')
        if '4' in data['text'] and bot_active:
            send_message('Important Links: \
                        \n ResLife: https://reslife.umd.edu/ \
                        \n 4Work: https://4work.umd.edu/ \
                        \n UMD: https://www.umd.edu/\
                        \n Dining Services: https://dining.umd.edu/\
                        \n StarRez: https://www.starrez.umd.edu/')
        if '5' in data['text'] and bot_active:
            send_message('Important Dates: \
                        \n Spring Break: March 17-24\
                        \n Last Day of Classes: May 9\
                        \n Reading Day: May 10\
                        \n Finals: May 11-17')
        if '/exit' in data['text'].lower() and bot_active:
            send_message('Goodbye!')
            bot_active = False
            
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
