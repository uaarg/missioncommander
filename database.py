from utils import *
from config import *
import config
import utm
import threading
import mission
from collections import OrderedDict

class BagOfHolding(object):

    def __init__(self):
        self.airplane = AirplaneTelemetry()
        self.waypoints = OrderedDict()
        self.allMissions = OrderedDict()
        self.tasks = fancyList()
        self.airMissionStatus = fancyList()
        self.remianingMissionTime = 0

    def updateTelemetry(self, msg):
        self.airplane.updateFromWaldo(msg)

    def updateAirMissionStatus(self, msg):
        self.remianingMissionTime = msg.remaining_time
        for e in range(0,len(msg.index_list)):
            self.airMissionStatus.addToIndex(self, (msg.index_list[e],msg.task_array[e]))

    def addWaypoint(self, wpTuple):
        self.waypoints.update(wpTuple)

    def updateWaypoint(self, msg):
        east = msg.fieldvalues[1]
        north = msg.fieldvalues[2]
        alt = msg.fieldvalues[3]
        zone = msg.fieldvalues[4]
        wp = self.waypoints.getFromIndex(int(msg.fieldvalues[0]))
        if wp != None:
            tmpest = str(wp.east)
            wp.update_utm(east, north, zone, northern=True, alt=alt, name=None)

            if (tmpest !=  str(wp.east)) and (WP_DEBUG):
                print(str(msg.fieldvalues[0]))
                print(wp.name)
                print('Updating a Waypoint!')
                print("Easting is :" + tmpest)
                print("Easting is :" + str(wp.east))
                print('------------------------------------------------------')

    def getWaypoint(self, index):
        return self.waypoints.get(index)

    def addMission(self, missionTuple):
        self.allMissions.update(missionTuple)

    def addTask(self, taskObj):
        self.tasks = fancyList()


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
        self.teleAvail = threading.Event()
        self.teleAvail.clear()
        self.positionFlag = False
        self.altitudeFlag = False
        self.headingFlag = False

    def updateFromWaldo(self, msg):
        easting = float(msg.fieldvalues[4]) / 100
        northing = float(msg.fieldvalues[5]) / 100
        zone_num = int(msg.fieldvalues[6])
        self.position = utm.to_latlon(easting, northing, zone_num, northern=UTM_NORTHERN_HEMISPHERE)
        self.altitude = msg.fieldvalues[10]
        self.heading = float(msg.fieldvalues[1]) * 180 / PI + 90
        self.teleAvail.set()
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
        self.teleAvail.clear()
        tele = {
            'latitude':float(self.position[0]),
            'longitude':float(self.position[1]),
            'altitude_msl':float(self.altitude),
            'uas_heading':float(self.heading)
        }
        return tele
