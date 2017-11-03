import json
import random
import time

with open('data/nvdcve-1.0-recent.json') as json_data:
	d = json.load(json_data)

item_list = d["CVE_Items"]
prompt = "Hi, this is BotForSecurity. Here are a couple of command:"
counts_cmd = "1. Counts: return how many data entries do we have\n \t\t subcommand: Sample <NUM>"
severity_cmd = "2. Severity: Get events with specified severity (low, medium, high) Optional third param: how many entries do you want to see (randomly selected).\n \t\t subcommand: Specific <ID>"
search_cmd = "3. Search: Search for a specific keyword and get info. Optional third param: how many entries do you want to see (randomly selected). \n \t\t subcommand: Specific <ID>"
default_msg = prompt + '\n' + counts_cmd + '\n' + severity_cmd  + '\n' + search_cmd
def postCounts(message, last_command):
	response = "There are %s vulnarable data entries in our current database.\n If you want to access some random ones to see what kind of info we get, enter Sample <NUM_You_Want>" % d["CVE_data_numberOfCVEs"]
	return response, "counts"
	

def postSample(message, last_command):
	response = ""
	rtn_msg = "Sample"
	if len(message) != 2:
		response = "Invalid input. Sample command takes in one argument. Please reenter."
		rtn_msg =  last_command
	else :
		random.seed(time.time())
		rdm_list = [item_list[i] for i in sorted(random.sample(range(len(item_list)),int(message[1])))]
		response = ""
		for i in range((len(rdm_list))):
			curr_cve = rdm_list[i]
			response += str(i+1) +". " +curr_cve["cve"]["description"]["description_data"][0]["value"] + "\n"
	return response, rtn_msg

def postSearch(message,last_command):
	response = ""
	rtn_msg = "Search"
	if len(message) == 2:
		keyword = message[1]
		count = 0
		for cve in item_list:
			curr_des = cve["cve"]["description"]["description_data"][0]["value"]
			if keyword.lower() in curr_des.lower():
				count += 1
				response += str(count) + ". "+ cve["cve"]["CVE_data_meta"]["ID"]+" "+ str(cve["lastModifiedDate"]) +" "+ curr_des + "\n"
		response += "See more info about a specific event by id in form of: Specific CVE-xxxx-xxxx\n"

	elif len(message) == 3 :
		keyword = message[1]
		try:
			num = int(message[2])
		except ValueError:
			response = "You enter an invalid number to specify how many entries you want to see."
			rtn_msg = last_command
			return response, rtn_msg
		search_list = []
		for cve in item_list:
			curr_des = cve["cve"]["description"]["description_data"][0]["value"]
			if keyword.lower() in curr_des.lower():
				search_list.append(cve)
		random.seed(time.time())
		rdm_list = [search_list[i] for i in sorted(random.sample(range(len(search_list)),num))]
		response = ""
		for i in range((len(rdm_list))):
			curr_cve = rdm_list[i]
			response += str(i+1) +". "+curr_cve["cve"]["CVE_data_meta"]["ID"]+" " +curr_cve["cve"]["description"]["description_data"][0]["value"] + "\n"
		response += "See more info about a specific event by id in form of: Specific CVE-xxxx-xxxx\n"
	else:
		response = "Invalid input. Search command takes in at most 2 arguments. Please reenter. \n The valid form is: " + search_cmd
		rtn_msg = last_command
	return response, rtn_msg

def postSeverity(message,last_command):
	response = ""
	rtn_msg = "Severity"
	if len(message) == 2:
		severity = message[1].lower()
		count = 0
		for cve in item_list:
			try:
				curr_severity = cve["impact"]["baseMetricV2"]["severity"]
			except KeyError:
				curr_severity = None
			if curr_severity != None and curr_severity.lower() == severity:
				count += 1
				curr_id = cve["cve"]["CVE_data_meta"]["ID"]
				curr_des = cve["cve"]["description"]["description_data"][0]["value"]
				response += str(count) +". " + curr_id + " " + str(cve["lastModifiedDate"]) + " " +curr_des + "\n\n"
		response += "See more info about a specific event by id in form of: Specific CVE-xxxx-xxxx\n"
	elif len(message) == 3:
		severity = message[1].lower()
		try:
			num = int(message[2])
		except ValueError:
			response = "You enter an invalid number to specify how many entries you want to see."
			rtn_msg = last_command
			return response, rtn_msg
		severity_list = []
		for cve in item_list:
			try:
				curr_severity = cve["impact"]["baseMetricV2"]["severity"]
			except KeyError:
				curr_severity = None
			if curr_severity != None and curr_severity.lower() == severity:
				severity_list.append(cve)
		random.seed(time.time())
		rdm_list = [severity_list[i] for i in sorted(random.sample(range(len(severity_list)),num))]
		for i in range (len(rdm_list)): 
			curr_cve = rdm_list[i]
			curr_id = curr_cve["cve"]["CVE_data_meta"]["ID"]
			curr_des = curr_cve["cve"]["description"]["description_data"][0]["value"]
			response += str(i+1) + " "+ curr_id + " " + str(curr_cve["lastModifiedDate"]) + " " +curr_des + "\n\n"
		response += "See more info about a specific event by id in form of: Specific CVE-xxxx-xxxx\n"

	else:
		response = "Invalid input. Severity command takes in one argument. Please reenter."
		rtn_msg = last_command
	return response, rtn_msg

def postSpecific(message,last_command):
	rtn_msg = "Specific"
	if len(message) != 2:
		response = "Invalid input. Specific command takes in one argument. Please reenter."
		rtn_msg =  last_command
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
		if response == "":
			response = "No CVE with this ID."
	return response, rtn_msg