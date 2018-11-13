import re


class SeleniumDriverMock:
    """
    Pages:
    + signup.php
    + confirm.php
    + welcome.php
    """
    current_page = "signup.php"

    focus_on_username_field = False

    username_value = ""
    username_session = ""

    def perform(self, action):

        cat = action[0]

        if cat == "click":
            self.click(action[1][0], action[1][1])

        elif cat == "type":
            self.type(action[1])

        else:
            pass

    def click(self, x, y):
        if self.current_page == "signup.php":
            # Click on Field
            if (8 <= x <= 162) and (8 <= y <= 29):
                self.focus_on_username_field = True

            # Click on Submit button
            elif (166 <= x <= 224) and (8 <= y <= 29):
                self.focus_on_username_field = False
                if len(self.username_value) > 6 and re.search(r"\d", self.username_value) is not None:
                    self.username_session = self.username_value.replace('\'', '')
                    self.current_page = "confirm.php"

                self.username_value = ""
            # Click on Blank page
            else:
                self.focus_on_username_field = False

        elif self.current_page == "confirm.php":
            # Click on Confirm
            if (8 <= x <= 102) and (8 <= y <= 25):
                self.current_page = "welcome.php"
            # Click on Back
            elif (8 <= x <= 88) and (26 <= y <= 43):
                self.current_page = "signup.php"
            else:
                pass

    def type(self, string):
        if self.current_page == "signup.php":
            if self.focus_on_username_field:
                self.username_value += string
