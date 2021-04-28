'''
Setup Instructions:

Download Driver from https://github.com/mozilla/geckodriver/releases
Download FireFox from https://www.mozilla.org/firefox/download/thanks/

Install Packages : selenium

Set PW & UserName:
use the export command on shell
example:
*********************************
export USERNAME=the._.sal
export PASSWORD=SomePWIDFK
*********************************

Run in shell ONLY or enter user name and pw manually
'''

try:
    from dotenv import load_dotenv # Optional Package to load .env file
    load_dotenv()
except:
    pass

from Backend import Insta_Bot
import os
prog = Insta_Bot(username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))
prog.LaunchWithLogin()
prog.do_like_with_tags(["Cars"])