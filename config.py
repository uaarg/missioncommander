import sys
from os import path, getenv
import math


#PPRZ_SRC = getenv("PPRZ_SRC")
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../paparazzi')))

if PPRZ_SRC == None:
    print("Paparzzi_SRC variable is not set. Considering setting it in your bash.rc file. See the README")
    PPRZ_SRC = getenv(path.normpath(path.join(path.dirname(path.abspath(__file__)), '~/paparazzi/')))

sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python")

from pprzlink.ivy  import IvyMessagesInterface
from pprzlink.message import PprzMessage

ivyint = IvyMessagesInterface
pprzmsg = PprzMessage

#Startup Arguement Defaults
#urlDefault = "http://10.42.0.1:8000" #SEBASTIAN's server over the network
#urlDefault = "http://10.42.0.1:8000" #localhosted server over network
#urlDefault = "http://localhost:8000" # localhosted server
urlDefault = "http://10.10.130.10:80"
usernameDefault = "alberta"
#usernameDefault = "testuser"
#passwordDefault = "testpass"
passwordDefault = "2771408451"

PI = math.pi
feetInOneMeter = 3.2808399
UTM_NORTHERN_HEMISPHERE = True
DEBUG = False
TELEM_DEBUG = False
WP_DEBUG = False # Paparazzi needs to be running
