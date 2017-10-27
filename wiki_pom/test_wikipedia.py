import sys
import time
import unittest
import re
import pages
from selenium import webdriver

class TestHomePage(unittest.TestCase):
	def setUp(self):
		if browser_param == 'firefox':
			self.driver = webdriver.Firefox()
		elif browser_param == 'ie':
			self.driver = webdriver.Ie()
		elif browser_param == 'chrome':
			self.driver = webdriver.Chrome()
		else:
			print "OOPS. BROWSER PARAMETER NOT RECOGNIZED"
		self.driver.implicitly_wait(5)

	def tearDown(self):
		time.sleep(5)
		self.driver.quit()

	#@unittest.skip('')
	def test_homepage_title(self):
		home = pages.HomePage(self.driver)
		home.openHomePage()
		self.assertEqual(home.getPageTitle(), "Wikipedia")

	#@unittest.skip("")
	def test_article_search1(self):
		home = pages.HomePage(self.driver)
		home.openHomePage()
		home.enterSearchKeywords("Buster Keaton")
		home.submitSearch()

		# Does the resulting page have the correct header & title
		article = pages.ArticlePage(self.driver)
		s = article.getPageTitle()
		self.assertTrue(re.search("^Buster Keaton.*", s), 
			"Page title '{}' does not start with search term".format(s))
		s = article.getCurrentUrl()
		self.assertTrue(re.search(".*Buster_Keaton$", s), 
			"URL '{}'  does not end with search term".format(s))
		self.assertEqual(article.getArticleHeader(), "Buster Keaton")

	#@unittest.skip('')
	def test_article_search2(self):
		main = pages.MainPage(self.driver)
		main.openMainPage()
		main.enterSearchKeywords("Disneyland")
		main.submitSearch()

		# Does the resulting page have the correct header & title
		article = pages.ArticlePage(self.driver)
		s = article.getPageTitle()
		self.assertTrue(re.search("^Disneyland.*", s), 
			"Page title '{}' is unexpected".format(s))
		s = article.getCurrentUrl()
		self.assertTrue(re.search(".*Disneyland$", s), 
			"URL '{}'  is unexpected".format(s))
		self.assertEqual(article.getArticleHeader(), "Disneyland")

	#@unittest.skip('')
	def test_header_autosuggest(self):
		main = pages.MainPage(self.driver)
		main.openMainPage()
		main.enterSearchKeywords("dou")
		titles = []
		for suggestion in main.getSearchSuggestions():
			titles.append(suggestion['title'])
		self.assertIn("Douglas MacArthur", titles)
		self.assertIn("Double bass", titles)
		self.assertNotIn("Dodo", titles)  # appears in suggestions fo 'do'

		time.sleep(1)  # pause before adding more charaters
		main.enterSearchKeywords("glas") # to make 'douglas'
		titles = []
		for suggestion in main.getSearchSuggestions():
			titles.append(suggestion['title'])
		self.assertIn("Douglas MacArthur", titles)
		self.assertNotIn("Double bass", titles)

	#@unittest.skip('')
	def test_homepage_autosuggest(self):
		home = pages.HomePage(self.driver)
		home.openHomePage()
		home.enterSearchKeywords("bust")
		suggestions = home.getSearchSuggestions()
		titles = []
		for suggestion in suggestions:
			titles.append(suggestion['title'])
		self.assertIn("Busta Rhymes", titles)
		self.assertIn("Buster Posey", titles)
		
		time.sleep(1)  # pause before adding more characters
		home.enterSearchKeywords("er")  # to make 'buster'
		suggestions = home.getSearchSuggestions()

		titles = []
		for suggestion in suggestions:
			titles.append(suggestion['title'])
		self.assertIn("Buster Keaton", titles)
		self.assertNotIn("Busta Rhymes", titles)


if __name__ == '__main__':
	if (len(sys.argv) == 2) and (sys.argv[1] in ['firefox', 'ie', 'chrome']):
		global browser_param 
		browser_param = sys.argv[1]
		del sys.argv[1]
		unittest.main(verbosity=2)
	else:
		print "Argument missing or invalid.  Expecting one of 'firefox', 'ie' or 'chrome'"

