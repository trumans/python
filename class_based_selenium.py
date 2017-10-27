import unittest
from selenium import webdriver

class WikiTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		print("class setup")

	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_title(self):
		self.driver.get("https://wikipedia.org")
		self.assertEqual(self.driver.title, "Wikipedia")

	@unittest.skip("nothing to see here")
	def test_skip_me(self):
		self.fail("shouldn't see this message")

	def tearDown(self):
		self.driver.quit()

	@classmethod
	def tearDownClass(self):
		print("class tear-down")


if __name__ == '__main__':
	unittest.main(verbosity=2)
