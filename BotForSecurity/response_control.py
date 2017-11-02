import json
import random

with open('../nvdcve-1.0-recent.json') as json_data:
	d = json.load(json_data)

item_list = d["CVE_Items"]
default_msg = "Hi, this is BotForSecurity. Here are a couple of command:\n1. Counts: return how many data entries do we have\n \t\t subcommand: Sample <NUM>\n2. Severity: Get events with specified severity (low, medium, high)\n \t\t subcommand: Specific <ID> \n 3. Search: Search for a specific keyword and get info\n \t\t subcommand: Specific <ID>"

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
		rdm_list = [item_list[i] for i in sorted(random.sample(range(len(item_list)),int(message[1])))]
		response = ""
		for i in range((len(rdm_list))):
			curr_cve = rdm_list[i]
			response += str(i+1) +". " +curr_cve["cve"]["description"]["description_data"][0]["value"] + "\n"
	return response, rtn_msg

def postSearch(message,last_command):
	response = ""
	rtn_msg = "Search"
	if len(message) != 2:
		response = "Invalid input. Search command takes in one argument. Please reenter."
		rtn_msg = last_command
	else :
		keyword = message[1]
		for cve in item_list:
			curr_des = cve["cve"]["description"]["description_data"][0]["value"]
			if keyword.lower() in curr_des.lower():
				response += cve["cve"]["CVE_data_meta"]["ID"]+" "+ str(cve["lastModifiedDate"]) +" "+ curr_des + "\n"
	return response, rtn_msg

def postSeverity(message,last_command):
	response = ""
	rtn_msg = "Severity"
	if len(message) != 2:
		response = "Invalid input. Severity command takes in one argument. Please reenter."
		rtn_msg = last_command
	else:
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