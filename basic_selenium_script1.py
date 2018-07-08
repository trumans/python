import time
from selenium import webdriver
#driver = webdriver.Chrome(executable_path='/selenium_browser_drivers/chromedriver')
driver = webdriver.Firefox(executable_path='/selenium_browser_drivers/geckodriver')
driver.get("http://www.busterkeaton.com")
time.sleep(5)
driver.quit()
