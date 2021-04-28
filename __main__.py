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
'''
from Backend import follow
import os
prog = follow(username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))
prog.LaunchWithLogin()