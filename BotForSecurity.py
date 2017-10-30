import os
import time
import json
from slackclient import SlackClient
import random

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = 'U7RM6DJTC'
BOT_NAME = 'alicechen'
SOCKET_DELAY = 1
with open('nvdcve-1.0-recent.json') as json_data:
	d = json.load(json_data)

item_list = d["CVE_Items"]
default_msg = "Hi, this is BotForSecurity. Here are a couple of command:\n1. Counts: return how many data entries do we have\n \t\t subcommand: Sample <NUM>\n2. Severity: Get events with specified severity (low, medium, high)\n \t\t subcommand: Specific <ID> \n 3. Search: Search for a specific keyword and get info\n \t\t subcommand: Specific <ID>"

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
def postCounts(message, user, channel,last_command):
	response = "There are %s vulnarable data entries in our current database.\n If you want to access some random ones to see what kind of info we get, enter Sample <NUM_You_Want>" % d["CVE_data_numberOfCVEs"]
	post_message(message=response, channel=channel)
	return "Counts"

def postSample(message, user, channel,last_command):
	print("Sample start")
	if len(message) != 2:
		response = "Invalid input. Sample command takes in one argument. Please reenter"
		post_message(message=response, channel=channel)
		return "Counts"
	else :
		rdm_list = [item_list[i] for i in sorted(random.sample(range(len(item_list)),int(message[1])))]
		response = ""
		for i in range((len(rdm_list))):
			curr_cve = rdm_list[i]
			response += str(i+1) +" " +curr_cve["cve"]["description"]["description_data"][0]["value"] + "\n"
		post_message(message=response, channel=channel)
		return "Sample"

def postSearch(message, user, channel,last_command):
	if len(message) != 2:
		response = "Invalid input. Sample command takes in one argument. Please reenter."
		post_message(message=response, channel=channel)
	else :
		response = ""
		keyword = message[1]
		for cve in item_list:
			curr_des = cve["cve"]["description"]["description_data"][0]["value"]
			if keyword.lower() in curr_des.lower():
				response += cve["cve"]["CVE_data_meta"]["ID"]+" "+ str(cve["lastModifiedDate"]) +" "+ curr_des + "\n"
		post_message(message=response, channel=channel)
	return "Search"

def postSeverity(message, user, channel,last_command):
	if len(message) != 2:
		response = "Invalid input. Severity command takes in one argument. Please reenter."
		post_message(message=response, channel=channel)
	else:
		response = ""
		severity = message[1].lower()
		for cve in item_list:
			try:
				curr_severity = cve["impact"]["baseMetricV2"]["severity"]
			except KeyError:
				curr_severity = None
			if curr_severity != None and curr_severity.lower() == severity:
				curr_id = cve["cve"]["CVE_data_meta"]["ID"]
				curr_des = cve["cve"]["description"]["description_data"][0]["value"]
				response += curr_id + " " + str(cve["lastModifiedDate"]) + " " +curr_des + "\n\n"
		response += "See more info about a specific event by id in form of: Specific CVE-xxxx-xxxx\n"
		post_message(message=response, channel=channel)
	return "Severity"

def postSpecific(message, user, channel,last_command):
	if len(message) != 2:
		response = "Invalid input. Specific command takes in one argument. Please reenter."
		post_message(message=response,channel=channel)
		return "Severity"
	else:
		response = ""
		for cve in item_list:
			curr_id = cve["cve"]["CVE_data_meta"]["ID"]
			if curr_id == message[1]:
				curr_des = cve["cve"]["description"]["description_data"][0]["value"]
				try :
					curr_severity = cve["impact"]["baseMetricV2"]["severity"]
				except KeyError:
					curr_severity = ""
				curr_time = cve["lastModifiedDate"]
				response += "ID:" + curr_id + "\n"
				response += "Severity:" + curr_severity + "\n"
				response += "Time: " + curr_time + '\n'
				response += "Description: " + curr_des + '\n'
				response += "References: \n"
				for url in cve["cve"]["references"]["reference_data"]:
					response += url["url"] +"\n"
				break
		post_message(message=response,channel=channel)
		return "Specific"


def handle_message(message, user, channel,last_command):
	if type(message) is not str:
		return last_command
    # TODO Implement later
	message = message.split(" ")
	if message[0].lower() == 'counts':
		return postCounts(message, user, channel,last_command)
	elif last_command.lower() == "counts" and message[0].lower() == "sample":
		return postSample(message, user, channel,last_command)
	elif message[0].lower() == 'severity':
		return postSeverity(message, user, channel,last_command)
	elif message[0].lower() == 'search':
		return postSearch(message, user, channel,last_command)
	elif last_command.lower() == "severity" or last_command.lower() == "search" and message[0].lower() == "specific":
		return postSpecific(message, user, channel,last_command)
	else:
		post_message(message=default_msg, channel=channel)
		return last_command

    

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
                    if is_for_me(event):
                        last_command = handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'), last_command=last_command)
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__ == "__main__":
    run()