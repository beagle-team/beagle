import re


class WackoPickoSqlStored:

    """
    /**/*.php 4

    /index.php 4
    
    /users/login.php 3

    /users/register.php 3

    /users/home.php 2

    /users/similar.php 1

    """

    current_page = "/index.php"
    closest_page = "/index.php"

    focus = "" # Focused element


    base = 10

    # Useful fields
    fields = {
        "username": "",
        "firstname": "",
        "lastname": "",
        "password": "",
        "passconfirm": "",
    }

    payload = fields
    session = fields

    _get = fields

    def best_base(self, page):
        if page == "/users/similar.php":
            self.base = 1
            self.closest_page = page
        elif page == "/users/home.php":
            if self.base > 1:
                self.base = 2
                self.closest_page = page
        elif page == "/users/register.php":
            if self.base > 2:
                self.base = 3
                self.closest_page = page
        elif page == "/users/login.php":
            if self.base > 2:
                self.base = 3
                self.closest_page = page
        elif page == "/index.php":
            if self.base > 3:
                self.base = 4
                self.closest_page = page
        else:
            if self.base > 3:
                self.base = 4
                self.closest_page = page
        # print(self.current_page)


    def switch_page(self, page):
        self._get = self.fields
        self.fields = {
            "username": "",
            "firstname": "",
            "lastname": "",
            "password": "",
            "passconfirm": "",
        }
        self.best_base(page)
        self.current_page = page

    def valid_fields(self):
        valid = (self.fields['username'] != '' and
               self.fields['firstname'] != '' and
               self.fields['lastname'] != '' and
               self.fields['password'] != '' and
               self.fields['password'] == self.fields['passconfirm'])
        return valid


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
                self.switch_page("/users/login.php")
            elif (50 <= x < 100):
                self.switch_page("/users/login.php")
            elif (240 <= x < 250):
                self.switch_page("/users/login.php")
            else:
                pass
        
        if self.current_page == "/users/login.php":
            if (120 <= y < 200):
                if (30 <= x < 150):
                    self.switch_page('/users/register.php')

        if self.current_page == "/users/register.php":
            if (30 <= x < 180):
                # Username
                if (100 <= y < 130):
                    self.focus = "username"
                    # print("[-] --------------------- Focus on {}".format(self.focus))
                # First name
                if (130 <= y < 160):
                    self.focus = "firstname"
                    # print("[-] --------------------- Focus on {}".format(self.focus))
                # Last name
                if (160 <= y < 190): 
                    self.focus = "lastname"
                    # print("[-] --------------------- Focus on {}".format(self.focus))
                # Password
                if (190 <= y < 210):
                    self.focus = "password"
                    # print("[-] --------------------- Focus on {}".format(self.focus))
                # Password confirm
                if (210 <= y < 230):
                    self.focus = "passconfirm"
                    # print("[-] --------------------- Focus on {}".format(self.focus))
                # Submit
                if (230 <= y < 260):
                    # print("[-] --------------------- SUBMIT")
                    self.logged = True
                    self.payload = self.fields
                    self.session = self.fields
                    self.switch_page('/users/home')

        if self.current_page == "/users/home.php":
            if (30 <= x < 180):
                if (100 <= y <= 130):
                    self.switch_page('/users/similar.php')
            
        if self.current_page == "/users/similar.php":
            self.payload = self.session

    def type(self, string):
        if self.focus != "":
            self.fields[self.focus] = string
            # print("[-] --------------------- Write on {}".format(self.focus))
