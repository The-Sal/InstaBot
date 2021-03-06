"""
Sample Data Set
'''
1) 0.86
2) 1
3) 2.8
4) 4.75
'''
"""
import json
import random
import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# X_Path of insta to locate elements to be clicked
Struct = {
    "LoginButton1": "/html/body/div[1]/section/main/article/div/div/div/div[3]/button[1]",
    "user_name": "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input",
    "pw": "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input",
    "loginfinal": "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]",
    "savelogin": "/html/body/div[1]/section/main/div/div/section/div/button",
    "dm": "/html/body/div[1]/section/nav[1]/div/div/header/div/div[2]/a/svg",
    "profile": "/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[5]/a/div",
    "like": "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button",
    "follow_click": "/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div/div/span/span[1]/button",
    "dm_input": "/html/body/div[1]/section/div[2]/div/div[1]/div/div[2]/input",
    "dm_top_click": "/html/body/div[1]/section/div[2]/div/div[2]/div[1]/div",
    "dm_next": "/html/body/div[1]/section/div[1]/header/div/div[2]",
    "dm_text_field": "/html/body/div[1]/section/div[2]/div/div/div[2]/div/div/div/textarea",
    "dm_send_message": "/html/body/div[1]/section/div[2]/div/div/div[2]/div/div/div[2]/button",
    "suggestions_follow" : "'html/body/div[1]/section/main/div/div[2]/div/div/div[{}]/div[2]/div[1]/div/a'"
}

Extraction = {
    "flwrs" : "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a",
    "flwing" : "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span",
    "Tag_profile_pic": "/html/body/div[1]/section/main/div/div/article/div[3]/div[1]/div/div[1]/div/a",
    "rando_from_tag_followers": "/html/body/div[1]/section/main/div/ul/li[2]/a/span"
}


Urls = {
    "main" : "https://instagram.com/",
    "activity" : "https://www.instagram.com/accounts/activity/",
    "search_tag" : "https://www.instagram.com/explore/tags/", # <- insert tag
    "discover_friends" : "https://www.instagram.com/explore/people/suggested/"
}





def check_for_ban(dvr):
    import os
    while True:
        time.sleep(0.5)
        if str(dvr.current_url).__contains__("challenge"):
            print("INFO: ACCOUNT LOCKED")
            print("EXITING")
            os._exit(0)

def snor():
    sleep_time = random.randint(0, 10)  # Keep it sus free yk
    time.sleep(sleep_time)

class Insta_Bot:
    def __init__(self, username, password):
        self.UserName = username
        self.pw = password

    def LwL(self, x_path, type, text_to_send=None, alt=None):
        '''
        0 = click
        1 = text
        2 = sendkeys
        '''
        OverrideCount = 500
        dvr = self.InstaDriver
        while OverrideCount > 0:
            try:
                if type == 0:
                    text = dvr.find_element_by_xpath(x_path).click()
                    break

                if type == 1:
                    try:
                        text = dvr.find_element_by_xpath(x_path).text
                        return text
                    except:
                        text = dvr.find_element_by_xpath(alt).text
                        return text

                if type == 2:
                    dvr.find_element_by_xpath(x_path).send_keys(text_to_send)
                    break

                break
            except Exception as e:
                if str(e).__contains__("element"):
                    pass
                else:
                    print(e)
                pass

        if not OverrideCount > 0:
            print("INFO: Too many attempts on {}".format(x_path))
            raise Exception("Too many attempts")

    def LaunchWithLogin(self, skipcheckup=False, headless=False):

        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"

        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)

        options = Options()
        options.headless = headless
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

            if skipcheckup:
                dvr.get("https://www.instagram.com/accounts/activity/")
                time.sleep(3)

                if str(dvr.current_url).__contains__("login"):  # if cookies failed url will contain login
                    print("INFO: Cookies Failed")
                    import sys
                    sys.exit(1)

            dvr.get("https://instagram.com")

        except Exception as e:
            dvr.refresh()
            print("INFO: Using Pw ERROR WITH COOKIES")
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
                    print("INFO: Exception Occured ->",e)
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

        followers = self.LwL(x_path=Extraction["flwrs"], type=1)
        following = self.LwL(x_path=Extraction["flwing"], type=1)

        dvr.set_window_size(360, 640)



        Thread(target=check_for_ban, args=[dvr], daemon=True).start()

        self.followers = followers
        self.following = following

        print("INFO: Username {}".format(self.UserName))
        print("INFO: Followers {}".format(self.followers).replace("followers", ""))
        print("INFO: Following {}".format(self.following))



        #dvr.quit()

    def do_like_with_tags(self, tags:list, max_likes, follow_user=None, max_followers=None):

        try:
            dvr = self.InstaDriver
        except:
            raise Exception("Driver not initialised")



        for tag in tags:
            Url = Urls["search_tag"] + tag
            dvr.get(Url)
            ActualPosts = []

            print("INFO: Searching for tag {}".format(tag))

            allLinks = dvr.find_elements_by_tag_name("a")

            for link in allLinks:
                l = link.get_attribute("href")
                if str(l).__contains__("/p/"):
                    ActualPosts.append(l)


            Liked = []
            Followed = []
            for post in ActualPosts:
                if max_likes <= 0:
                    break
                max_likes = max_likes - 1
                print(post)
                snor()
                dvr.get(post)

                Tries = 10000
                NoReturn = False
                while Tries > 0:
                    if NoReturn:
                        break
                    snor()
                    dvr.execute_script("window.scrollTo(28, 527)")
                    snor()
                    self.LwL(x_path=Struct["like"], type=0)

                    if follow_user:
                        snor()
                        print("INFO: Checking user eligibility")
                        self.LwL(x_path=Extraction["Tag_profile_pic"], type=0)
                        Followers = self.LwL(x_path=Extraction["rando_from_tag_followers"], type=1)
                        print("INFO: Raw Data {}".format(Followers))

                        Followers = Followers.replace(",", "")

                        if str(Followers).lower().__contains__("k"):
                            Followers = Followers.lower().replace("k", "")
                            Followers = Followers.split(".")
                            Followers = Followers[0]
                            nom_followers = int(Followers)
                            nom_followers = nom_followers * 1000
                        else:
                            nom_followers = int(Followers)

                        print("INFO: Target Has {}".format(nom_followers))
                        if nom_followers <= max_followers:
                            Followed.append(dvr.current_url)
                            print("INFO: Target Acquired")
                            break
                    break
                else:
                    print("INFO: Max Tries EXCEEDED")
                    continue

                Liked.append(post)

            self.liked_posts = Liked
            self.followed_people = Followed


    def unlike_all_posts(self):
        dvr = self.InstaDriver
        for post in self.liked_posts:
            dvr.get(post)
            Tries = 1000
            while Tries > 0:
                snor()

                try:
                    dvr.execute_script("window.scrollTo(28, 527)")
                    self.LwL(x_path=Struct["like"], type=0)
                    break
                except:
                    pass
            else:
                print("INFO: Max Tries EXCEEDED")
                continue

        self.liked_posts.clear()

    def save_progress(self):
        SVD = open('progress_made.json', 'w+')
        SavedArray = self.liked_posts
        Followed = self.followed_people
        cfg = {
            "Liked": SavedArray,
            "Followed" : Followed
        }
        json.dump(cfg, SVD, indent=4)
        SVD.truncate()

    def scroll_feed(self, times):
        driver = self.InstaDriver
        driver.get(Urls["main"])
        print("INFO: Scrolling {}".format(times))
        for _ in range(times):
            time.sleep(1)
            screen_height = driver.execute_script("return window.screen.height;")
            i = 1

            C = 0

            while True:
                driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                C = C + 1
                if C >= 10:
                    break

                time.sleep(1)
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                if (screen_height) * i > scroll_height:
                    break

    def safe_mode(self, type:int, Tags=None, AmountOfLikes=None, follow=None, max_followerss=None):
        print("INFO: Using SAFE MODE")
        if type == 0:
            for tag in Tags:
                self.do_like_with_tags([tag], AmountOfLikes, follow_user=follow, max_followers=max_followerss)
                rn = random.randint(0, 3)
                self.scroll_feed(rn)

                continue

        if type == 1:
            pass

    def direct_message(self, message, recipient):
        dvr = self.InstaDriver
        dvr.get('https://www.instagram.com/direct/new/')
        self.LwL(x_path=Struct["dm_input"], type=2, text_to_send=recipient)
        time.sleep(3)
        self.LwL(x_path=Struct["dm_top_click"], type=0)
        time.sleep(2)
        self.LwL(x_path=Struct["dm_next"], type=0)
        # time.sleep(1)
        self.LwL(x_path=Struct["dm_text_field"], type=2, text_to_send=message)
        # time.sleep(2)
        print("INFO: Sending message to {}".format(recipient))
        self.LwL(x_path=Struct["dm_send_message"], type=0)


    def undo_progress(self):
        dvr = self.InstaDriver
        prog_file = open('progress_made.json', 'r')
        JsProgFile = json.load(prog_file)
        Flwrs = list(JsProgFile["Followed"])
        Liked = list(JsProgFile["Liked"])

        in_ = random.randint(0,1)

        self.liked_posts = Liked
        self.unlike_all_posts()
        # Uncompleted work in progress


    def slurp_links(self, keytag=None):
        Actual = []
        dvr = self.InstaDriver
        allLinks = dvr.find_elements_by_tag_name("a")

        for link in allLinks:
            l = link.get_attribute("href")
            if not keytag == None:
                if str(l).__contains__(keytag):
                    Actual.append(l)
            else:
                Actual.append(l)


    def chain_follow_suggestions(self, max_follow:int = None):
        dvr = self.InstaDriver



        # Look for pattern
        # /html/body/div[1]/section/main/div/div[2]/div/div/div[1]/div[3]/button | /html/body/div[1]/section/main/div/div[2]/div/div/div[1]/div[2]/div[1]/div/a
        # /html/body/div[1]/section/main/div/div[2]/div/div/div[2]/div[3]/button | /html/body/div[1]/section/main/div/div[2]/div/div/div[2]/div[2]/div[1]/div/a
        # /html/body/div[1]/section/main/div/div[2]/div/div/div[1]/div[2]/div[1]/div/a

        max_follow = max_follow + 1

        FollowUsers = []
        for x in range(max_follow):

            dvr.set_window_size(360, 640)
            dvr.get(Urls["discover_friends"])
            User_html_id = x + 1


            Temp_html_for_user = f"/html/body/div[1]/section/main/div/div[2]/div/div/div[{User_html_id}]/div[2]/div[1]/div/a"
            snor()
            self.LwL(x_path=Temp_html_for_user, type=0)
            print("INFO: Checking user eligibility")

            dvr.set_window_size(1280, 734)

            followers = self.LwL(x_path="/html/body/div[1]/section/main/div/header/section/ul/li[2]/span",
                                 alt='/html/body/div[1]/section/main/div/header/section/ul/li[2]/a',
                                 type=1)

            following = self.LwL(x_path="/html/body/div[1]/section/main/div/header/section/ul/li[3]/span",
                                 alt='/html/body/div[1]/section/main/div/header/section/ul/li[3]/a',
                                 type=1)


            print("INFO: Raw Data {} / {}".format(followers, following))

            following = str(following).replace('following', '')
            followers = str(followers).replace('followers', '')
            following = str(following).replace(',', '')
            followers = str(followers).replace(',', '')

            # Math Time---

            flwrs_int = float(followers)
            flwing_int = float(following)
            ratio = flwrs_int / flwing_int

            print('INFO: Follow Ratio -> {}'.format(ratio))

            r = round(ratio, 1)

            if r <= 1:
                FollowUsers.append(dvr.current_url)

            continue

        print(FollowUsers)



