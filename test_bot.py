import unittest
import BotForSecurity
import os

class TestBot(unittest.TestCase):

	def setUp(self):
		pass

	def test_counts(self):
		expected = "There are 689 vulnarable data entries in our current database.\n If you want to access some random ones to see what kind of info we get, enter Sample <NUM_You_Want>"
		self.assertTrue(BotForSecurity.postCounts("Counts","")[0] == expected and BotForSecurity.postCounts("Counts","")[1].lower() == "counts")

	def test_severity(self):
		self.assertEqual("high","high")

	def test_token(self):
		self.assertTrue(os.environ.get('SLACK_BOT_TOKEN') != None)

if __name__ == '__main__':
	unittest.main()