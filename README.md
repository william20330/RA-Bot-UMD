# RA-Bot-UMD
RA Bot is a chatbot designed to assist residents in accessing information and services within a residential community. It integrates with the GroupMe messaging platform to provide residents with quick access to important resources, services, and community updates.

# Features
Command-Based Interaction: Users can interact with the bot by sending commands to access various services and information.
Holiday Message Notification: The bot automatically sends holiday messages to residents based on the current date and public holiday data.
Information Retrieval: Users can retrieve information such as contact numbers, operating hours, important dates, and links to relevant resources.
Webhook Integration: Utilizes a Flask web application with a webhook endpoint to receive and process incoming messages from GroupMe.
Scheduled Tasks: Background scheduler is employed to execute tasks such as checking for public holidays at specified intervals.
# Usage
Commands:

/ra bot: Introduction to the bot and available options.
/menu: Displays a menu of available commands.
/exit: Closes the interaction with the bot.
Numbered commands (e.g., /1, /2) for accessing specific information or services.
Sending Messages:

Send messages to the bot with the desired command to trigger a response.
# Setup
Prerequisites:

Python 3.x
Flask
APScheduler
GroupMe Bot ID (Obtain from GroupMe Developer API)
Installation:

bash
Copy code
pip install -r requirements.txt
Configuration:

Set the environment variable GROUPME_BOT_ID with your GroupMe Bot ID.
Running the Application:

bash
Copy code
python app.py

Acknowledgments
GroupMe API for providing the platform for bot integration.
Nager.Date API for public holiday data.
