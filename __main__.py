'''
To set username and pw

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