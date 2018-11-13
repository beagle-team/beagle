import re 

class WackoPickoXssReflected:

    """
    /**/*.php 2

    /index.php 2

    /pictures/search.php 1
    """

    current_page = "/index.php"

    focus = "" # Focused element

    payload = ""

    base = 10

    # Useful fields
    fields = {
        "search": "",
    }
    
    _get = {
        "search": "",
    }

    def reset(self):
        self.focus = ""
        self.payload = ""
        self.base = 10
        self.switch_page("/index.php")

    def best_base(self, page):
        if page == "/pictures/search.php":
            self.base = 1
        else:
            if self.base > 1:
                self.base = 2


    def switch_page(self, page):
        self._get = self.fields
        self.fields = {
                "search": "",
        }
        self.focus = ""
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
        # if self.current_page == '/pictures/search.php':
            # return

        # Click on WackoPicko.com
        # if (y < 40):
            # self.switch_page("/index.php")

        """
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
        """

        if (80 <= y < 140):
            if (0 <= x < 150):
                pass
            elif (100 <= x < 200):
                # print("[-] -------------------------------------------- Focused!") 
                self.focus = "search"
            elif (200 <= x < 250):
                self.payload = self.fields['search']
                # print("[-] -------------------------------------------- Submitted!") 
                self.switch_page("/pictures/search.php")
                # self.fields['search'] = self._get['search']

    def type(self, string):
        if self.focus == "search":
            # print("[-] -------------------------------------------- Typing...") 
            self.fields['search'] = string
