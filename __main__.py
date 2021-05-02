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
    from dotenv import load_dotenv  # Optional Package to load .env file

    load_dotenv()
except:
    pass

from Backend import Insta_Bot
import os

if __name__ == '__main__':
    prog = Insta_Bot(username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))
    prog.LaunchWithLogin(headless=True)
    prog.chain_follow_suggestions(max_follow=5)
    # prog.undo_progress()
    # prog.direct_message(recipient="", message="how's you're day?")
    # prog.safe_mode(Tags=["uae"], type=0, AmountOfLikes=10, follow=True, max_followerss=300)
    # prog.save_progress()
