from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('disable-xss-auditor')

host = 'http://localhost:5000/detect_mouse.html'

browser = webdriver.Chrome(chrome_options=options)

browser.get(host)

actions = ActionChains(browser)

for i in range(500):
    actions.move_by_offset(5, 5)
    actions.pause(0.1)
    actions.click()

actions.perform()
