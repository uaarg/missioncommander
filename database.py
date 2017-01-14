from utils import *
# from config import *

class bagOfHolding(object):

    def __init__(self):
        self.airplane = airplaneTelemetry()
        self.waypoints = fancyList()
        self.missions = fancyList()
        self.tasks = fancyList()

    def addWaypoint(self, wp):
        self.waypoints.add(wp)

    def updateWaypoint(self, wp):
        self.waypoints.update(wp)
    
    def getWaypoint(self, index):
        return self.waypoints.get(index)



class AirplaneTelemetry(object):
    '''
    Fancy mission list object that is fancy
    '''

    def __init__(self):
        self.position = (0, 0) # Tuple of lat-lon
        self.altitude = 0
        self.heading = 0
        self.positionFlag = False
        self.altitudeFlag = False
        self.headingFlag = False

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
