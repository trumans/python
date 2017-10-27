import time
from selenium import webdriver
driver = webdriver.Firefox()
driver.get("http://www.busterkeaton.com")
time.sleep(5)
driver.quit()
