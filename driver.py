from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
# options.add_argument('headless')

browser = webdriver.Chrome(chrome_options=options)
browser.get("http://www.python.org")
print(browser)

browser.close()
