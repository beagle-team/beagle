from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('disable-xss-auditor')
options.add_argument('window-size=1000,1000')

host = 'http://localhost:5000'
target = 'xss.php'
payload = 'someone'

browser = webdriver.Chrome(chrome_options=options)

browser.get(host)

actions = ActionChains(browser)

# CLICK 60, 60
actions.move_by_offset(60, 60)
actions.click()
actions.move_by_offset(-60, -60)

# CLICK 80, 20
actions.move_by_offset(80, 20)
actions.click()
actions.move_by_offset(-80, -20)

# TYPE 'Andrea'
actions.send_keys(payload)

# CLICK 200, 20
actions.move_by_offset(200, 20)
actions.click()
actions.move_by_offset(-200, -20)

actions.perform()

