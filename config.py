import sys
from os import path, getenv
import math

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
#PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../paparazzi')))
#sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python/")

from pprzlink.ivy  import IvyMessagesInterface
from pprzlink.message import PprzMessage

ivyint = IvyMessagesInterface
pprzmsg = PprzMessage

PI = math.pi
UTM_NORTHERN_HEMISPHERE = True

DEBUG = False
TELEM_DEBUG = False

INTEROP_ENABLE = False
