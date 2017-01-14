from utils import *
from config import *
import config
import maths

class bagOfHolding(object):

    def __init__(self):
        self.airplane = AirplaneTelemetry()
        self.waypoints = fancyList()
        self.missions = fancyList()
        self.tasks = fancyList()

    def updateTelemetry(self, msg):
        self.airplane.updateFromWaldo(msg)

    def addWaypoint(self, wp):
        self.waypoints.add(wp)

    def updateWaypoint(self, wp):
        self.waypoints.update(wp)

    def getWaypoint(self, index):
        return self.waypoints.get(index)



class AirplaneTelemetry(object):
    '''
    Stores the airplane's position, altitude and current heading.
    This is meant to be updated from the Ivybus and updating the Interop Server
    when any value is updated.
    We need to submit at a minimum of 1 Hz to the server to recieve points
    '''

    def __init__(self):
        self.position = (0, 0) # Tuple of lat-lon
        self.altitude = 0
        self.heading = 0
        self.positionFlag = False
        self.altitudeFlag = False
        self.headingFlag = False

    def updateFromWaldo(self, msg):
        self.position = maths.utm_to_DD((msg.fieldvalues[4]), (msg.fieldvalues[5] ), msg.fieldvalues[6])
        self.altitude = msg.fieldvalues[10]
        self.heading = float(msg.fieldvalues[1]) * 180 / PI + 90
        if TELEM_DEBUG:
            print(self.position)

    # Updates each variable
    def newPosition(self, newPos):
        if (self.position != newPos):
            self.position = newPos
            self.positionFlag = True
            return True
        else:
            return False

    def newAltitude(self, newAlt):
        if (self.altitude != newAlt):
            self.altitude = newAlt
            self.altitudeFlag = True
            return True
        else:
            return False

    def newHeading(self, newHead):
        if (self.heading != newHead):
            self.heading = newHead
            self.headingFlag = True
            return True
        else:
            return False

    # Interop server code will call this when new data is recieved
    def getTelemetry(self):
        if (self.positionFlag or self.altitudeFlag or self.headingFlag):
            self.positionFlag = self.altitudeFlag = self.headingFlag = False
            tele = {
                'latitude':self.position[0],
                'longitude':float(self.position[1]),
                'altitude_msl':float(self.altitude),
                'uas_heading':float(self.heading)
            }
            return tele
        else:
            return False
