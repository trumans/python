import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class BasePage(object):

	search_input = (By.ID, 'searchInput')
	submit_search = (By.CSS_SELECTOR, '.searchButton')
	search_input_suggestions = (By.CSS_SELECTOR, '.suggestions-results > a')

	def __init__(self, driver):
		self.driver = driver

	def getPageTitle(self):
		return self.driver.title

	def getCurrentUrl(self):
		return self.driver.current_url	

	def enterSearchKeywords(self, search_string):
		self.driver.find_element(
			*BasePage.search_input).send_keys(search_string)

	def submitSearch(self):
		self.driver.find_element(*BasePage.submit_search).click()

	def getSearchSuggestions(self):
		time.sleep(.2)  # allow suggestion list to update
		##elements = 
		suggestions = []
		for element in self.driver.find_elements(
				*BasePage.search_input_suggestions):
			suggestion = {}
			suggestion['title'] = element.text
			suggestion['link'] = element.get_attribute('href')
			suggestions.append(suggestion)
		return suggestions

class HomePage(BasePage):

	homePageUrl = "https://wikipedia.org"
	
	search_input = (By.ID, 'searchInput')
	submit_search = (By.XPATH, "//button[@type='submit']")
	search_input_suggestions = (By.CSS_SELECTOR, '#typeahead-suggestions a')
	
	def openHomePage(self):
		self.driver.get(self.homePageUrl)

	def enterSearchKeywords(self, search_str):
		self.driver.find_element(*HomePage.search_input).send_keys(search_str)

	def submitSearch(self):
		self.driver.find_element(*HomePage.submit_search).click()

	def getSearchSuggestions(self):
		time.sleep(.2)  # allow suggestion list to update
		##elements = 
		suggestions = []
		for element in self.driver.find_elements(
				*HomePage.search_input_suggestions):
			suggestion = {}
			text = element.text.split("\n")
			suggestion['title'] = text[0]
			suggestion['summary'] = text[1] if len(text) == 2 else ''
			suggestion['link'] = element.get_attribute('href')
			suggestions.append(suggestion)
		return suggestions

class ArticlePage(BasePage):

	article_header = (By.ID, 'firstHeading')

	def getArticleHeader(self):
		return self.driver.find_element(*ArticlePage.article_header).text

class MainPage(BasePage):

	mainPageUrl = "https://en.wikipedia.org/wiki/Main_Page"

	def openMainPage(self):
		self.driver.get(self.mainPageUrl)
