import sys
#import time
import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import pages

class WikipediaCommon(unittest.TestCase):
	def setUp(self):
		if browser == 'firefox':
			self.driver = webdriver.Firefox(executable_path='/selenium_browser_drivers/geckodriver')
		elif browser == 'ie':
			self.driver = webdriver.Ie()
		elif browser == 'chrome':
			self.driver = webdriver.Chrome(executable_path='/selenium_browser_drivers/chromedriver')
		elif browser == 'safari':
			self.driver = webdriver.Safari()
			self.driver.set_window_position(20,20)
			self.driver.set_window_size(1200,800)
		else:
			print('Browser parameter not recognized')
		# The implicit wait should not be necessary, generally
		#self.driver.implicitly_wait(5)

	def tearDown(self):
		self.driver.quit()

class TestHomePage(WikipediaCommon):
	#@unittest.skip('')
	def test_homepage_title(self):
		home = pages.HomePage(self.driver)
		home.open_home_page()
		self.assertEqual(home.get_page_title(), "Wikipedia")

	#@unittest.skip('')
	# Safari doesn't display a tab unless multiple tabs are open.
	def test_homepage_article_search(self):
		home = pages.HomePage(self.driver)
		home.open_home_page()
		home.enter_search_term("Buster Keaton")
		home.submit_search()

		# check the resulting page has the correct header & title
		article = pages.ArticlePage(self.driver)
		s = article.get_page_title()
		self.assertTrue(re.search("^Buster Keaton.*", s), 
			"Page title '{0}' does not start with search term".format(s))
		s = article.get_current_url()
		self.assertTrue(re.search(".*Buster_Keaton$", s), 
			"URL '{0}'  does not end with search term".format(s))
		self.assertEqual(article.get_article_header(), "Buster Keaton")

	#@unittest.skip('')
	def test_homepage_autosuggest(self):
		home = pages.HomePage(self.driver)
		home.open_home_page()
		home.enter_search_term("bust")
		suggestions = home.get_search_suggestions()
		titles = [suggestion['title'] for suggestion in suggestions]
		error_msg = "'{}' not found in titles {}"

		search_str = "Busta Rhymes"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertTrue(len(matching), error_msg.format(search_str, titles))
		
		search_str = "Buster Posey"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertTrue(len(matching), error_msg.format(search_str, titles))

		home.enter_search_term("er")  # complete 'buster'
		suggestions = home.get_search_suggestions()
		titles = [suggestion['title'] for suggestion in suggestions]

		search_str = "Buster Keaton"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertTrue(len(matching), error_msg.format(search_str, titles))

		# should no longer be in list
		search_str = "Busta Rhymes"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertFalse(len(matching), error_msg.format(search_str, titles))
		
	# navigate to a language's main page and some basic checks
	#   language_code: 2 character in link to language main page (ex: de)
	#   language_name: beginning of text on language link (ex: Deutsch)
	#   title_text: expected title on resulting language page
	#   body_text: expected text in page body
	# 
	#@unittest.skip('')
	def language_main_page_test(self, 
		language_code, language_name, title_text, body_text):
		home = pages.HomePage(self.driver)
		home.open_home_page()
		lang_link = home.find_element_language_link(language_code)

		self.assertIn(language_name,lang_link.text)

		home.click_link(lang_link)

		main = pages.MainPage(self.driver)
		self.assertEqual(title_text, home.get_page_title())
		self.assertIn(body_text, home.get_body_text())

	#@unittest.skip('')
	def test_homepage_english_link(self):
		self.language_main_page_test(
			language_code='en',
			language_name='English',
			title_text="Wikipedia, the free encyclopedia",
			body_text="the free encyclopedia that anyone can edit")

	#@unittest.skip('')
	def test_homepage_french_link(self):
		self.language_main_page_test(
			language_code='fr',
			language_name='Français',
			title_text="Wikipédia, l'encyclopédie libre",
			body_text="L'encyclopédie libre que chacun peut améliorer")

	#@unittest.skip('')
	def test_homepage_german_link(self):
		self.language_main_page_test(
			language_code='de',
			language_name='Deutsch',
			title_text="Wikipedia – Die freie Enzyklopädie",
			body_text="Wikipedia ist ein Projekt zum Aufbau einer Enzyklopädie aus freien Inhalten")

	#@unittest.skip('')
	def test_homepage_spanish_link(self):
		# literal for body text
		if browser == 'safari':
			b_text ="la\xa0enciclopedia\xa0de\xa0contenido\xa0libre\xa0que\xa0todos\xa0pueden\xa0editar"
		else:
			b_text ="la enciclopedia de contenido libre que todos pueden editar"

		self.language_main_page_test(
			language_code='es',
			language_name='Español',
			title_text="Wikipedia, la enciclopedia libre",
			body_text=b_text)


class TestMainPage(WikipediaCommon):
	#@unittest.skip('')
	def test_mainpage_article_search(self):
		main = pages.MainPage(self.driver)
		main.open_article_by_search("Disneyland")

		# check the resulting page has the correct header & title
		article = pages.ArticlePage(self.driver)
		s = article.get_page_title()
		self.assertTrue(re.search("^Disneyland.*", s), 
			"Page title '{}' is unexpected".format(s))
		s = article.get_current_url()
		self.assertTrue(re.search(".*Disneyland$", s), 
			"URL '{}'  is unexpected".format(s))
		self.assertEqual(article.get_article_header(), "Disneyland")

	#@unittest.skip('')
	@unittest.skipIf((len(sys.argv) > 1) and (sys.argv[1] == 'safari'), 'main page search does not return autosuggest on Safari')
	def test_mainpage_autosuggest(self):
		main = pages.MainPage(self.driver)
		main.open_main_page()
		main.enter_header_search_term("dou")
		titles = []
		for suggestion in main.get_header_search_suggestions():
			titles.append(suggestion['title'])
		self.assertIn("Douglas MacArthur", titles)
		self.assertIn("Double bass", titles)
		self.assertNotIn("Dodo", titles)  # appears in suggestions for 'do'

		main.enter_header_search_term("glas") # complete 'douglas'
		titles = []
		for suggestion in main.get_header_search_suggestions():
			titles.append(suggestion['title'])
		self.assertIn("Douglas MacArthur", titles)
		self.assertNotIn("Double bass", titles)

class TestArticlePage(WikipediaCommon):

	# Template for testing info box contents
	# Parameters:
	#   search_term: search text to open an article. 
	#     assumes search does not open a disambiguration page
	#   expected_value: list of (label, value) tuples where 
	#     label is a string contained in the left side of a row in info box
	#     value is a string contained in value on the right side.
	#       if value is None then label is not expected in info box
	def infobox_test(self, search_term, expected_values):
		main = pages.MainPage(self.driver)
		main.open_article_by_search(search_term)

		article = pages.ArticlePage(self.driver)
		info = article.get_infobox_contents()
		for (label, expected_value) in expected_values:
			found_value = article.get_value_from_infobox_contents(info, label)
			if expected_value == None:
				self.assertEqual(None, found_value)
			else:
				self.assertIn(expected_value, found_value)

	#@unittest.skip('')
	def test_infobox_for_country(self):
		expected_values = [
			('Currency', "Sol"), ('Capital', "Lima"),
			('Directed', None), ('Starring', None),
			('atomic weight', None), ('Phase at STP', None),
			('Born', None), ('Relatives', None)]
		self.infobox_test("Peru", expected_values)

	#@unittest.skip('')
	def test_infobox_for_chemistry(self):
		expected_values = [
			('atomic weight', "15.999"), ('Phase at STP', "gas"),
			('Directed', None), ('Starring', None),
			('Born', None), ('Relatives', None), 
			('Currency', None), ('Capital', None)]
		self.infobox_test("Oxygen", expected_values)

	#@unittest.skip('')
	def test_infobox_for_person(self):
		expected_values = [
			('Born', '1889'), ('Relatives', 'Chaplin'),
			('Directed', None), ('Starring', None),
			('atomic weight', None), ('Phase at STP', None),
			('Currency', None), ('Capital', None)]
		self.infobox_test("Charlie Chaplin", expected_values)

	#@unittest.skip('')
	def test_infobox_for_movie(self):
		expected_values = [
			('Directed', 'Alfred Hitchcock'), ('Starring', 'Cary Grant'),
			('Born', None), ('Relatives', None), 
			('atomic weight', None), ('Phase at STP', None),
			('Currency', None), ('Capital', None)]
		self.infobox_test("north by northwest", expected_values)

	def test_compare_toc_to_headlines(self):
		main = pages.MainPage(self.driver)
		main.open_article_by_search("Douglas Adams")

		article = pages.ArticlePage(self.driver)
		toc = article.get_toc_items_text()
		headlines = article.get_headlines_text()
		self.assertEqual(toc, headlines)


if __name__ == '__main__':
	if (len(sys.argv) == 2) and (sys.argv[1] in ['firefox', 'ie', 'chrome', 'safari']):
		global browser 
		browser = sys.argv[1]
		del sys.argv[1]
		unittest.main(verbosity=2)
	else:
		print("Argument missing or invalid.  Expecting one of 'firefox', 'ie' or 'chrome'")

