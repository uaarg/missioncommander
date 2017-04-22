import sys
from os import path, getenv
import math

PPRZ_SRC = getenv("PPRZ_SRC")
if PPRZ_SRC == None:
    print("Paparzzi_SRC variable is not set. Considering setting it in your bash.rc file. See the README")
    PPRZ_SRC = path.abspath(path.join(__file__ ,"../../../../"))


from pprzlink.ivy  import IvyMessagesInterface
from pprzlink.message import PprzMessage

ivyint = IvyMessagesInterface
pprzmsg = PprzMessage

#Startup Arguement Defaults
urlDefault = "http://localhost:8000"
usernameDefault = "testuser"
passwordDefault = "testpass"
AC_ID = 5

PI = math.pi
UTM_NORTHERN_HEMISPHERE = True

DEBUG = False
TELEM_DEBUG = False
WP_DEBUG = False # Paparazzi needs to be running
