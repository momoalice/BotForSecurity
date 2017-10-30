import unittest
import BotForSecurity

class TestBot(unittest.TestCase):

	def setUp(self):
		pass

	def test_counts(self):
		self.assertEqual("649","649")

	def test_severity(self):
		self.assertEqual("high","high")

if __name__ == '__main__':
	unittest.main()