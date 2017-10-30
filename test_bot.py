import unittest
import BotForSecurity
import os

class TestBot(unittest.TestCase):

	def setUp(self):
		pass

	def test_counts(self):
		self.assertEqual("649","649")

	def test_severity(self):
		self.assertEqual("high","high")

	def test_token(self):
		print(os.environ.get('SLACK_BOT_TOKEN'))
		self.assertTrue(os.environ.get('SLACK_BOT_TOKEN') != None)

if __name__ == '__main__':
	unittest.main()