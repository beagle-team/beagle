import re


class WackoPickoXssReflected:

    """
    /index.php 4

    /users/login.php 3

    /users/register.php 2

    /passcheck.php 1
    """

    current_page = "/index.php"

    focus = "" # Focused element

    payload = ""

    base = 10

    # Useful fields
    fields = {
        "search": "",
        "picname": "",
        "password": "",
    }
    
    _get = {
        "search": "",
        "picname": "",
        "password": "",

    }

    def best_base(self, page):
        if page == "/passcheck.php":
            self.base = 1
        elif page == "/users/register.php":
            if self.base > 1:
                self.base = 2
        elif page == "/users/login.php":
            if self.base > 2:
                self.base = 3
        else:
            if self.base > 3:
                self.base = 4


    def switch_page(self, page):
        self._get = self.fields
        self.fields = {
                "search": "",
                "picname": "",
                "password": "",
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

        elif (80 <= y < 200):
            if (0 <= x < 150):
                pass
            elif (150 <= x < 200):
                self.focus = "searchfield"
            # Click on submit
            elif (200 <= x < 250):
                if self.fields['search'] != "":
                    self.switch_page("/pictures/search.php")
                    self.fields['search'] = self._get['search']

        if self.current_page == "/users/login.php":
            # Click on Page Content
            if (200 <= y < 230):
                if (100 <= x < 150):
                    self.switch_page("/users/register.php")
                elif (30 <= x < 90):
                    self.switch_page("/users/login.php")

            # Click on filename field
            elif (154 <= y < 200):
                if (50 <= x < 100):
                    self.focus = "filefield"

        if self.current_page == "/users/register.php":
            # Click on Page Content
            if (150 <= y < 170):
                if (30 <= x < 150):
                    self.switch_page("/passcheck.php")

            # Click on filename field
            elif (154 <= y < 200):
                if (50 <= x < 100):
                    self.focus = "filefield"

        if self.current_page == "/passcheck.php":
            # Password field
            if (120 <= y < 170):
                if (0 <= x < 180):
                    self.focus = "password"

            # Submit
            elif (190 <= y < 220):
                if (50 <= x < 150):
                    if self.fields['password'] != "":
                        self.payload = self.fields['password']
                        self.switch_page("/passcheck.php")


    def type(self, string):
        if self.focus == "password":
            self.fields['password'] = string
