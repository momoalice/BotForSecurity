import os
import time
from slackclient import SlackClient
from response_control import *

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = 'U7RM6DJTC'
BOT_NAME = 'alicechen'
SOCKET_DELAY = 1

slack_client = SlackClient(BOT_TOKEN)


def get_mention(user):
    return '<@{user}>'.format(user=user)

slack_mention = get_mention(BOT_ID)

def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def is_for_me(event):
    """Know if the message is dedicated to me"""
    my_type = event.get('type')
    if my_type and my_type == 'message' and not(event.get('user')==BOT_ID):
        if is_private(event):
            return True
        text = event.get('text')
        channel = event.get('channel')
        if type(text) is not str:
            return False
        if slack_mention in text.strip().split():
            return True



def handle_message(message, user, channel,last_command):
    if type(message) is not str:
        return last_command
    response = default_msg
    rtn_msg = last_command
    print(message)
    message = message.split(" ")
    message.remove(slack_mention)
    print(message)
    if len(message) != 0:
        if message[0].lower() == 'counts':
            response, rtn_msg = postCounts(message, last_command)
        elif last_command.lower() == "counts" and message[0].lower() == "sample":
            response, rtn_msg =  postSample(message, last_command)
        elif message[0].lower() == 'severity':
            response, rtn_msg = postSeverity(message, last_command)
        elif message[0].lower() == 'search':
            response, rtn_msg = postSearch(message, last_command)
        elif last_command.lower() == "severity" or last_command.lower() == "search" or last_command.lower() == "specific" and message[0].lower() == "specific":
            response, rtn_msg = postSpecific(message, last_command)
        else:
            rtn_msg = last_command
    post_message(message = response, channel=channel)
    return rtn_msg

    

def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)
def run():
    if slack_client.rtm_connect():
        print('is ON...')
        last_command = ""
        while True:
            event_list = slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if event.get('type') == 'message':
                        if is_for_me(event):
                            last_command = handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'), last_command=last_command)
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__ == "__main__":
    run()