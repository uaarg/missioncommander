from utils import *
from config import *
from .flightblock import FlightBlockList
from .waypointobject import Waypoint
import config
import utm
import logging
import threading
from collections import OrderedDict
from PyQt5.QtCore import QObject, pyqtSignal



logg = logging.getLogger(__name__)

class BagOfHolding(object):

    def __init__(self):
        self.airplane = AirplaneTelemetry()
        self.waypoints = OrderedDict()
        self.allMissions = OrderedDict()
        self.tasks = OrderedDict()
        self.airMissionStatus = fancyList()
        self.groundMissionStatus = fancyList()
        self.remianingMissionTime = 0
        self.signals = dbSignals()
        self.flightBlocks = FlightBlockList()
        self.currentFlightBlock = None

    def groundMissionStatusUpdated(self):
        pass
        #self.sync.missionUpdateSent()

    def updateTelemetry(self, msg):
        self.airplane.updateFromWaldo(msg)

    def updateAirMissionStatus(self, msg):
        self.remianingMissionTime = msg.fieldvalues[0]
        if(msg.fieldvalues[1].split(",")[0] != 0):
            mission_array = msg.fieldvalues[1].split(",")
            mission_list = fancyList()
#--------------------------------------------------------------------------------[6/9/2018]----------------
            #task_array = msg.fieldvalues[2].split(",")

            # Parse Missions and Task
            for iv_miss_id in mission_array:
                miss = self.findMissionById(iv_miss_id)
                if miss != None :
                    mission_list.append(miss)

            if (len(mission_list)>0)and(len(self.airMissionStatus)>0)and(mission_list[0].name != self.airMissionStatus[0].name):
                self.signals.updateStagedMissionsinUI()

            self.airMissionStatus = mission_list
            self.groundMissionStatus.replaceAll(mission_list)


        self.signals.updateUASinUI()

    def findMissionById(self, idStr):
        for miss in self.allMissions.items():
            if (str(miss[1].index) == idStr):
                return miss[1]
        return None

    def addWaypoint(self, wpTuple):
        self.waypoints.update(wpTuple)

    def updateWaypoint(self, msg):
        east = msg.fieldvalues[1]
        north = msg.fieldvalues[2]
        alt = msg.fieldvalues[3]
        zone = msg.fieldvalues[4]
        wp = list(self.waypoints.items())[int(msg.fieldvalues[0])][1]
        if (wp != None)and((east != wp.east)or(north != wp.north)or(alt != wp.alt)):
            tmpest = str(wp.east)
            if (tmpest !=  str(wp.east)) and (WP_DEBUG):
                print(str(msg.fieldvalues[0]))
                print(wp.name)
                print('Updating a Waypoint!')
                print("New Easting is :" + tmpest)
                print("Old Easting is :" + str(wp.east))
                print('------------------------------------------------------')

            wp.update_utm(east, north, zone, northern=True, alt=alt, name=None)
            #Waypoint has updated, check if it is part of a comitted mission
            for mission in self.groundMissionStatus :
                for committedWaypoint in mission.waypoints:
                    if wp.name == committedWaypoint:
                        self.signals.resendMissions()

    def getWaypoint(self, index):
        return self.waypoints.get(index)

    def addMission(self, missionTuple):
        self.allMissions.update(missionTuple)

    def addTask(self, taskTuple):
        self.tasks.update(taskTuple)

    def updateCurrentFlightBlock(self, currentBlockID):
        '''
        Sends the signal to UI to update to the selected flight block
        '''
        newBlock = self.flightBlocks.getFlightBlockByID(currentBlockID)

        if (newBlock != self.currentFlightBlock):
            self.currentFlightBlock =  newBlock
            self.signals.updateCurrentBlock()


class AirplaneTelemetry(object):
    '''
    Stores the airplane's position, altitude and current heading.
    This is meant to be updated from the Ivybus and updating the Interop Server
    when any value is updated.
    We need to submit at a minimum of 1 Hz to the server to recieve points

    Note the interop server REQUIRES position in Lat/Lon and height in ft msl
    (feet above mean sea level). Conversion is done here and saved in the server's units.
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
        easting = float(msg.fieldvalues[4]) / 100 # cm to m
        northing = float(msg.fieldvalues[5]) / 100 # cm to m
        zone_num = int(msg.fieldvalues[6])
        try:
            self.position = utm.to_latlon(easting, northing, zone_num, northern=UTM_NORTHERN_HEMISPHERE)
        except utm.error.OutOfRangeError:
            logg.warning('Out Of Range Error, GPS is probably disconnected. Defaulting to NULL ISLAND (0,0) \n GPS Easting: ' +str(easting)+ ' Northing: ' + str(northing))
            self.position = ('0', '0') #Plane defaults to NULL ISLAND in the Atlantic Ocean

        self.altitude = str((float(msg.fieldvalues[10]) + Waypoint.flightParams['ground_alt'])*feetInOneMeter)
        if (float(self.altitude) < 0):
            logg.warning('Altitude reported as negative. Flipping Altitude:' + self.altitude + ' to prevent further errors')
            self.altitude = str(-1*float(self.altitude))

        self.heading = float(msg.fieldvalues[1]) * 180 / PI + 90
        self.teleAvail.set()
        if TELEM_DEBUG:
            print(self.position)

    # Updates each variable individually. This isint really used, can we discard?
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
        newHead = self.checkHeading(newHead)
        if (self.heading != newHead):
            self.heading = newHead
            self.headingFlag = True
            return True
        else:
            return False

    def checkHeading(self, value):
        '''
        Ensures heading is a value the interop server accepts.
        '''
        counter = 0
        while (value > 360.0) or (value < 0.0):
            if (value > 360.0):
                value = value - 360.0
            else:
                value = value + 360.0

            counter = counter + 1
            if counter > 1000:
                logger. critical('Breaking infinite loop of heading checker')
                break

        return value

    # Interop server code will call this when new data is recieved
    def getTelemetry(self):
        self.teleAvail.clear()
        self.newHeading(self.heading) # probably a better way to do this, but I want to be sure were sending a valid heading

        tele = {
            'latitude':float(self.position[0]),
            'longitude':float(self.position[1]),
            'altitude_msl':float(self.altitude),
            'uas_heading':float(self.heading)
        }
        return tele

class dbSignals(QObject):
    '''This class is to be used to create QT signal objects which can then be connected to the UI'''
    uas_update = pyqtSignal()
    stagedListUpdate = pyqtSignal()
    resendMissionstoUI = pyqtSignal()
    updateFlightBlock = pyqtSignal()

    def __init__(self):
        # Initialize as a QObject
        QObject.__init__(self)

    def updateUASinUI(self):
        self.uas_update.emit()

    def updateStagedMissionsinUI(self):
        self.stagedListUpdate.emit()

    def resendMissions(self):
        self.resendMissionstoUI.emit()

    def updateCurrentBlock(self):
        self.updateFlightBlock.emit()
