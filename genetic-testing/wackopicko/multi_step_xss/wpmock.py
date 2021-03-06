import re


class WackoPickoXssBehindFlash:

    """
    /**/*..php 3
    
    /index.php 3
    
    /pictures/recent.php 2

    /pictures/view.php 1

    /comments/preview_comments.php 1
    """

    current_page = "/index.php"

    focus = "" # Focused element

    payload = ""

    base = 10

    # Useful fields
    fields = {
        "search": "",
        "picname": "",
        "comment": "",
    }
    
    _get = {
        "search": "",
        "picname": "",
        "comment": "",
    }

    def best_base(self, page):
        if page == "/pictures/view.php":
            self.base = 1
        elif page == "/comments/preview_comment.php":
            if self.base > 1:
                self.base = 2
        elif page == "/pictures/recent.php":
            if self.base > 1:
                self.base = 2
        elif page == "/index.php":
            if self.base > 2:
                self.base = 3
        else:
            if self.base > 2:
                self.base = 3


    def switch_page(self, page):
        self._get = self.fields
        self.fields = {
                "search": "",
                "picname": "",
                "comment": "",
        }
        self.best_base(page)
        self.current_page = page


    def perform(self, action):

        cat = action[0]

        if cat == "click":
            self.click(action[1][0], action[1][1])

        elif cat == "type":
            self.type(action[1])

        else:
            pass

    def click(self, x, y):
        self.focus = ""

        # Click on WackoPicko.com
        if (y < 40):
            self.switch_page("/index.php")

        # Click on Header (any page)
        elif (40 <= y < 80):
            # Click on home
            if (0 <= x < 50):
                self.switch_page("/users/home.php")
            elif (50 <= x < 100):
                self.switch_page("/pictures/upload.php")
            elif (100 <= x < 150):
                self.switch_page("/pictures/recent.php")
            elif (150 <= x < 200):
                self.switch_page("/guestbook.php")
            elif (200 <= x < 250):
                self.switch_page("/users/login.php")
            else:
                pass
        elif (80 <= y < 120):
            if (0 <= x < 150):
                pass
            elif (150 <= x < 200):
                self.focus = "searchfield"
            elif (200 <= x < 250):
                self.switch_page("/pictures/search.php")
                self.fields['search'] = self._get['search']

        if self.current_page == "/index.php":
            # Click on Page Content
            if (150 <= y < 151):
                if (0 <= x < 150):
                    self.switch_page("/users/register.php")

            elif (151 <= y < 152):
                if (0 <= x < 150):
                    self.switch_page("/users/sample.php")
            elif (152 <= y < 153):
                if (0 <= x < 150):
                    self.switch_page("/calendar.php")
            elif (153 <= y < 154):
                if (0 <= x < 50):
                    self.switch_page("/error.php")

            # Click on submit button
            elif (200 <= y < 250):
                if (50 <= x < 100):
                    if self.fields['picname'] != "":
                        self.switch_page("/piccheck.php")

        if self.current_page == "/pictures/recent.php":
            # Click on Page Content
            if (120 <= y < 250):
                if (0 <= x < 250):
                    self.switch_page("/pictures/view.php")

        if self.current_page == "/pictures/view.php":
            # Click on Page Content
            if (150 <= y < 220):
                if (0 <= x < 250):
                    self.focus = "comment"
            if (150 <= y < 220):
                if (30 <= x < 150):
                    self.switch_page("/comments/preview_comment.php")
        if self.current_page == "/pictures/view.php":
            if (120 <= y < 250):
                if (50 <= x < 150):
                    self.payload = self._get['comment']
                    self.switch_page("/pictures/view.php")

    def type(self, string):
        if self.focus == "comment":
            self.fields['comment'] = string
