import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SelExc

class BasePage(object):

	import wait_for

	search_input = (By.ID, 'searchInput')
	submit_search_button = (By.CSS_SELECTOR, '#searchButton')
	search_input_suggestions = (By.CSS_SELECTOR, '.suggestions-results > a')

	def __init__(self, driver):
		self.driver = driver

	def get_page_title(self):
		return self.driver.title

	def get_current_url(self):
		return self.driver.current_url	

	def get_body_text(self):
		return self.driver.find_element(By.TAG_NAME, 'body').text

	# get rows from a table and return as a dictionary
	#   keys are text from th element
	#   values are text from td element
	#   missing th or td element is assigned None for the key or value 
	def table_to_list_of_tuples(self, table_element):
		vals = []
		row_elements = table_element.find_elements(By.TAG_NAME, "tr")
		for row in row_elements:
			try:
				h = row.find_element(By.TAG_NAME, "th").text.strip()
			except SelExc.NoSuchElementException:
				h = None

			try:
				d = row.find_element(By.TAG_NAME, "td").text.strip()
			except SelExc.NoSuchElementException:
				d = None
			
			##print("Key:", h, "; Value:", d)
			vals.append((h, d))

		return vals

	# return a value from a table
	# parameters:
	#   table_element: web object expected to contain table rows elements (tr)
	#   header_text: text to find in a row header (th). 
	# returns: 
	#     table data (td) text if a matching row header if found
	#     None if a matching row header is not found
	def get_value_in_table(self, table_element, header_text):
		row_elements = table_element.find_elements(By.TAG_NAME, "tr")
		for row in row_elements:
			try:
				h = row.find_element(By.TAG_NAME, "th").text.strip()
			except SelExc.NoSuchElementException:
				h = ''

			if header_text in h:
				try:
					d = row.find_element(By.TAG_NAME, "td").text.strip()
				except SelExc.NoSuchElementException:
					d = None
				return d

		return None  # header text was not found
	# Click on a link
	#   parameter: link_obj is a selenium object which can be clicked on.
	#     assumes link opens another page
	@wait_for.new_url_and_title
	def click_link(self, link_obj):
		link_obj.click()

	def enter_header_search_term(self, search_string):
		before_list = self.get_header_search_suggestions()
		before_time = time.time()
		self.driver.find_element(
			*BasePage.search_input).send_keys(search_string)
		# wait for autosuggest list to update
		while True:
			after_list = self.get_header_search_suggestions()
			after_time = time.time()
			if (before_list != after_list) or ((after_time-before_time) > 1):
				break

	@wait_for.new_url_and_title
	def submit_header_search(self):
		self.driver.find_element(*BasePage.submit_search_button).send_keys(Keys.RETURN)

	# get the list of suggestions from the header search field
	#   Returns: list of suggestions represented as a dictionary with items
	#     'title' contain text of suggestion and 'link' containing href.
	#
	#   Note: method does not attempt to wait for list to "settle" although
	#     it does recover from selenium Stale Element exception
	def get_header_search_suggestions(self):
		while True:
			try:
				suggestions = [ 
					{'title': element.text, 
					 'link' : element.get_attribute('href') }
					for element in self.driver.find_elements(
						*BasePage.search_input_suggestions)
				]
				break
			except SelExc.StaleElementReferenceException:
				pass

		return suggestions

class HomePage(BasePage):

	import wait_for

	homePageUrl = "https://wikipedia.org"
	
	search_input = (By.ID, 'searchInput')
	submit_search_button = (By.XPATH, "//button[@type='submit']")
	search_input_suggestions = (By.CSS_SELECTOR, '#typeahead-suggestions a')

	def open_home_page(self):
		self.driver.get(self.homePageUrl)

	def enter_search_term(self, search_str):
		max_wait = 2 # maximum time to wait for search suggestions to change
		before_list = self.get_search_suggestions()
		before_time = time.time()		
		self.driver.find_element(*HomePage.search_input).send_keys(search_str)
		# wait for sooner of: the autosuggestion list to change, or 1 second
		while True:
			after_list = self.get_search_suggestions()
			after_time = time.time()
			if (after_list != before_list) or ((after_time-before_time) > max_wait):
				break

	@wait_for.new_url_and_title
	def submit_search(self):
		self.driver.find_element(*HomePage.submit_search_button).click()

	# get the suggestions from the search input
	# returns a list of suggestions represented by dictionaries containing
	#   'title' of the suggestion
	#   'summary' with any additional text
	#   'link' containing the href in the suggestion
	def get_search_suggestions(self):
		suggestions = []
		while True:
			try:
				for element in self.driver.find_elements(
						*HomePage.search_input_suggestions):
					text = element.text.split("\n")
					suggestion = {
						'title'  : text[0],
						'summary': text[1] if len(text) == 2 else '',
						'link'   : element.get_attribute('href')}
					suggestions.append(suggestion)
				break
			except SelExc.StaleElementReferenceException:
				pass
		return suggestions

	def find_element_language_link(self, language_code):
		css = "a[href='//{}.wikipedia.org/']".format(language_code)
		return self.driver.find_element(By.CSS_SELECTOR, css)

	# Click a specified language link
	#   parameter language_code: 2 letter language code in link 
	#     for lanaguage's main page
	@wait_for.new_url_and_title
	def click_language_link(self, language_code):
		self.find_element_language_link(language_code).click()


class ArticlePage(BasePage):

	article_header = (By.ID, 'firstHeading')
	infobox = (By.CSS_SELECTOR, 'table.infobox')

	def get_article_header(self):
		return self.driver.find_element(*ArticlePage.article_header).text

	def get_infobox_text(self):
		return self.driver.find_element(*ArticlePage.infobox).text

	# parse the contents of the infobox
	# returns: list of two-item tuples containing text from th and td elements
	def get_infobox_contents(self):
		i = self.driver.find_element(*ArticlePage.infobox)
		return self.table_to_list_of_tuples(i)

	def get_value_from_infobox(self, header_text):
		i = self.driver.find_element(*ArticlePage.infobox)
		return self.get_value_in_table(i, header_text)

	# return a value from a list of tuples
	# parameters:
	#   infobox_contents: list of two-item tuples, presumably from an infobox 
	#   header_text: text to find the first item of each tuple (i.e. table header) 
	# returns: 
	#     second item from the tuple containing the matching header text
	#     None if a matching value is not found
	def get_value_from_infobox_contents(self, infobox_contents, header_text):
		for item in infobox_contents:
			if item[0] != None and header_text in item[0]:
				return item[1]
		return None

class MainPage(BasePage):

	main_page_url = "https://en.wikipedia.org/wiki/Main_Page"
	top_banner = (By.ID, 'mp-topbanner')

	def open_main_page(self):
		self.driver.get(self.main_page_url)

