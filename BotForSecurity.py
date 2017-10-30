import os
import time
import json
from slackclient import SlackClient

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = 'U7RM6DJTC'
BOT_NAME = 'alicechen'
SOCKET_DELAY = 1
with open('nvdcve-1.0-recent.json') as json_data:
	d = json.load(json_data)

AT_BOT = "<@U7RM6DJTC:>"
COMMAND1 = "1"
COMMAND2 = "2"
COMMAND3 = "3"
COMMAND4 = "4"
COMMAND5 = "5"

slack_client = SlackClient(BOT_TOKEN)

def get_mention(user):
    return '<@{user}>'.format(user=user)

slack_mention = get_mention(BOT_ID)

def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def is_for_me(event):
    """Know if the message is dedicated to me"""
    type = event.get('type')
    if type and type == 'message' and not(event.get('user')==BOT_ID):
        if is_private(event):
            return True
        text = event.get('text')
        channel = event.get('channel')
        if slack_mention in text.strip().split():
            return True
def handle_message(message, user, channel):
    # TODO Implement later
    default_msg = "Hi, this is BotForSecurity. Here are a couple of command:\n1. Counts: return how many data entries do we have\n2. Recent: Get the description for the most recent insecurity\n 3. Latest: Get the time for the most recent insecure activity\n 4. Types: Get all the types of insecure activities"
    post_message(message=default_msg, channel=channel)

def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)
def run():
    if slack_client.rtm_connect():
        print('is ON...')

        while True:
            event_list = slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__ == "__main__":
    run()