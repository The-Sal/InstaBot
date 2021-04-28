"""
How does it work???

Enter a tag then searches posts based on tag then tages USERS who posted with tag and follows said user
hoping for a follow4follow chain to occur. To help it work faster only follow people who have less than a threshhold of
followers
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# X_Path of insta to locate elements to be clicked
Struct = {
    "LoginButton1" : "/html/body/div[1]/section/main/article/div/div/div/div[3]/button[1]",
    "user_name" : "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input",
    "pw" : "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input",
    "loginfinal" : "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]",
    "savelogin": "/html/body/div[1]/section/main/div/div/section/div/button",
    "dm" : "/html/body/div[1]/section/nav[1]/div/div/header/div/div[2]/a/svg",
    "profile" : "/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[5]/a/div"
}

Extraction = {
    "flwrs" : "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a",
    "flwing" : "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a"
}

class follow:
    def __init__(self, username, password):
        self.UserName = username
        self.pw = password

    def LaunchWithLogin(self):

        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"

        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)

        options = Options()
        options.headless = False
        # Download FireFox & Download GECKODriver and Insert It's path here V
        driver = webdriver.Firefox(options=options, executable_path='/users/sal/downloads/geckodriver', firefox_profile=profile)
        dvr = driver
        dvr.set_window_size(360, 640)
        dvr.get("https://www.instagram.com/")

        self.InstaDriver = dvr

        dvr.delete_all_cookies()
        try:
            cookie_file = open('cookies_yum.json', 'r')
            JsCookieFile = json.load(cookie_file)
            ListOfCookies = list(JsCookieFile["cookies"])
            for l in ListOfCookies: # if you inject saved cookies u don't have to re-login
                dvr.add_cookie(l)

            dvr.refresh()

            dvr.get("https://www.instagram.com/accounts/activity/")
            time.sleep(3)

            if str(dvr.current_url).__contains__("login"): # if cookies failed url will contain login
                print("Cookies Failed")
                raise Exception

        except Exception as e:
            print(e)
            dvr.refresh()
            print("Using PW ERROR WITH COOKIES")
            while True:
                try:
                    dvr.find_element_by_xpath(Struct["LoginButton1"]).click()
                    break
                except:
                    pass

            while True:
                try:
                    dvr.find_element_by_xpath(Struct["user_name"]).send_keys(self.UserName)
                    dvr.find_element_by_xpath(Struct["pw"]).send_keys(self.pw)
                    dvr.find_element_by_xpath(Struct["loginfinal"]).click()
                    break
                except Exception as e:
                    print(e)
                    pass

            time.sleep(4)
            while True:
                try:
                    dvr.find_element_by_xpath(Struct["savelogin"]).click()
                    break
                except:
                    pass

            cookie_file = open('cookies_yum.json', 'w+')
            cookies = dvr.get_cookies()

            cfg = {
                "cookies" : cookies
            }
            json.dump(cfg, cookie_file, indent=4)
            cookie_file.truncate()

            dvr.close()
            dvr.stop_client()
            pass


