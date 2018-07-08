import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
	driver = webdriver.Chrome(executable_path='/selenium_browser_drivers/chromedriver')
	#driver =  webdriver.Firefox(executable_path='selenium_browser_drivers/geckodriver')
	driver.wait = WebDriverWait(driver, 5)
	return driver

# from Marina Mele site - http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
def lookupMM(driver, query):
	driver.get("https://wikipedia.org")
	try:
		box_locator = (By.ID, "searchInput")
		box = driver.wait.until(EC.presence_of_element_located(box_locator))
		button_locator = (By.CLASS_NAME, "pure-button")
		button = driver.wait.until(EC.presence_of_element_located(button_locator))
		box.send_keys(query)
		button.click()
	except TimeoutException:
		print('EXCEPTION: Box or button not found on page')

def lookup(driver, query):
	driver.get("https://wikipedia.org")
	try:
		driver.find_element_by_id("searchInput").send_keys(query)
		driver.find_element_by_class_name('pure-button').click()
	except TimeoutException:
		print('EXCEPTION: Box or button not found on page')

if __name__ == "__main__":
	driver = init_driver()
	lookup(driver, "Buster Keaton")
	time.sleep(5)
	driver.quit()


