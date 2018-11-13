import re


class WackoPickoMock:

    """
    /index.php

    /users/home.php
    /guestbook.php
    /pictures/search.php
    /pictures/upload.php
    /pictures/recent.php
    /users/login.php
    /users/logout.php

    /admin/index.php
    /tos.php

    /submitname.php
    /passcheck.php
    /users/similar.php
    /users/view.php
    /users/register.php
    /pictures/view.php
    /pictures/purchased.php
    /comments/preview_comment.php
    /users/sample.php
    /cart/action.php
    /cart/review.php
    /cart/confirm.php
    """

    current_page = "/index.php"

    focus = "" # Focused element
    
    # Useful fields


    def perform(self, action):

        cat = action[0]

        if cat == "click":
            self.click(action[1][0], action[1][1])

        elif cat == "type":
            self.type(action[1])

        else:
            pass

    def click(self, x, y):
        if self.current_page == "signup":
            # Click on Field
            if (64 <= x <= 192) and (224 <= y <= 240):
                self.focus_on_username_field = True

            # Click on Submit button
            elif (96 <= x <= 178) and (32 <= y <= 64):
                self.focus_on_username_field = False
                if len(self.username_value) > 6 and re.search(r"\d", self.username_value) is not None:
                    self.username_session = self.username_value.replace('\'', '')
                    self.current_page = "confirm"

                self.username_value = ""
            # Click on Blank page
            else:
                self.focus_on_username_field = False

        elif self.current_page == "confirm":
            # Click on Confirm
            if (96 <= x <= 178) and (32 <= y <= 64):
                self.current_page = "welcome"
            # Click on Back
            elif (96 <= x <= 178) and (128 <= y <= 160):
                self.current_page = "signup"
            else:
                pass
        else:
            pass

    def type(self, string):
        if self.current_page == "signup":
            if self.focus_on_username_field:
                self.username_value += string
