import unittest
from BotForSecurity.response_control import *
import os

class TestBot(unittest.TestCase):

	def setUp(self):
		pass

	def test_token(self):
		self.assertTrue(os.environ.get('SLACK_BOT_TOKEN') != None)

	def test_counts(self):
		expected = "There are 689 vulnarable data entries in our current database.\n If you want to access some random ones to see what kind of info we get, enter Sample <NUM_You_Want>"
		self.assertTrue(postCounts(["Counts"],"")[0] == expected and postCounts("Counts","")[1].lower() == "counts")

	def test_specific(self):
		expected_error_output = "Invalid input. Specific command takes in one argument. Please reenter."
		self.assertTrue(postSpecific(["Specific"], "Search")[0] == expected_error_output and postSpecific("Specific", "Search")[1].lower() == "search")
		# ID not fount
		expected_response = "No CVE with this ID."
		actual_response = postSpecific("Specific 123".split(" "), "Search")[0]
		self.assertEqual(expected_response,actual_response)

	def test_Search(self):
		expected_error_output = "Invalid input. Search command takes in one argument. Please reenter."
		self.assertTrue(postSearch(["Search"], "")[0] == expected_error_output and postSearch(["Search"], "")[1].lower() == "")

	def test_Sample(self):
		expected_error_output = "Invalid input. Sample command takes in one argument. Please reenter."
		self.assertTrue(postSample(["Sample"], "Counts")[0] == expected_error_output and postSample(["Sample"], "Counts")[1].lower() == "counts")

	def test_Severity(self):
		expected_error_output = "Invalid input. Severity command takes in one argument. Please reenter."
		self.assertTrue(postSeverity(["Severity"], "Counts")[0] == expected_error_output and postSeverity(["Severity"], "Counts")[1].lower() == "counts")


	# def test_handle(self):
	# 	# Test invalid input
	# 	actual_return_1 = BotForSecurity.handle_message("Hello",None, None, "Counts").lower()
	# 	expected_return_1 = "counts"
	# 	# Test valid subcommand yet not following its master command
	# 	actual_return_2 = BotForSecurity.handle_message("Specific 1",None, None, "Counts").lower()
	# 	expected_return_2 = "counts"
	# 	# Test valid subcommand
	# 	actual_return_3 = BotForSecurity.handle_message("Specific 1",None, None, "Search").lower()
	# 	expected_return_3 = "specific"
	# 	self.assertEqual(actual_return_1 , expected_return_1)
	# 	self.assertEqual(actual_return_2 , expected_return_2)
	# 	self.assertEqual(actual_return_3 , expected_return_3)


	

if __name__ == '__main__':
	unittest.main()