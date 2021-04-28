"""
How does it work???

Enter a tag then searches posts based on tag then tages USERS who posted with tag and follows said user
hoping for a follow4follow chain to occur. To help it work faster only Insta_Bot people who have less than a threshhold of
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
    "profile" : "/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[5]/a/div",
    "like" : "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
}

Extraction = {
    "flwrs" : "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a",
    "flwing" : "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span"
}


Urls = {
    "main" : "https://instagram.com/",
    "activity" : "https://www.instagram.com/accounts/activity/",
    "search_tag" : "https://www.instagram.com/explore/tags/" # <- insert tag
}

def LwL(dvr, x_path, type):
    text = "None"
    OverrideCount = 500
    while OverrideCount > 0:
        try:
            if type == 0:
                text = dvr.find_element_by_xpath(x_path).click()
                break

            if type == 1:
                text = dvr.find_element_by_xpath(x_path).text
                break

            break
        except Exception as e:
            print(e)
            pass

    if not OverrideCount > 0:
        print("INFO: Too many attempts on {}".format(x_path))
        raise Exception("Too many attempts")

    return text

class Insta_Bot:
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

            dvr.get("https://instagram.com")

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

            pass

        prfurl = "https://www.instagram.com/" + self.UserName

        dvr.get(url=prfurl)

        dvr.set_window_size(1280, 734)

        followers = LwL(dvr=dvr, x_path=Extraction["flwrs"], type=1)
        following = LwL(dvr=dvr, x_path=Extraction["flwing"], type=1)

        dvr.set_window_size(360, 640)

        self.followers = followers
        self.following = following

        print("INFO: Username {}".format(self.UserName))
        print("INFO: Followers {}".format(self.followers).replace("followers", ""))
        print("INFO: Following {}".format(self.following))

        self.InstaDriver = dvr

        #dvr.quit()

    def do_like_with_tags(self, tags:list, max_likes):

        try:
            dvr = self.InstaDriver
        except:
            raise Exception("Driver not initialised")


        #
        #/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[2]/a/div/div[2]
        #/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[3]/a/div/div[2]


        for tag in tags:
            Url = Urls["search_tag"] + tag
            dvr.get(Url)
            ActualPosts = []

            allLinks = dvr.find_elements_by_tag_name("a")

            for link in allLinks:
                l = link.get_attribute("href")
                if str(l).__contains__("/p/"):
                    ActualPosts.append(l)


            Liked = []
            for post in ActualPosts:
                if max_likes <= 0:
                    break
                max_likes = max_likes - 1
                print(post)
                dvr.get(post)

                Tries = 10000
                while Tries > 0:
                    try:
                        dvr.execute_script("window.scrollTo(28, 527)")
                        LwL(dvr=dvr, x_path=Struct["like"], type=0)
                        break
                    except:
                        pass
                else:
                    print("INFO: Max Tries EXCEEDED")
                    continue

                Liked.append(post)

            self.liked_posts = Liked




    def unlike_all_posts(self):
        dvr = self.InstaDriver
        for post in self.liked_posts:
            dvr.get(post)
            Tries = 1000
            while Tries > 0:
                try:
                    dvr.execute_script("window.scrollTo(28, 527)")
                    LwL(dvr=dvr, x_path=Struct["like"], type=0)
                    break
                except:
                    pass
            else:
                print("INFO: Max Tries EXCEEDED")
                continue

        self.liked_posts.clear()

    def save_all_liked(self):
        SVD = open('progress_liked', 'w+')
        SavedArray = self.liked_posts
        cfg = {
            "cookies": SavedArray
        }
        json.dump(cfg, SVD, indent=4)
        SVD.truncate()
