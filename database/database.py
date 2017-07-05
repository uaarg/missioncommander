from utils import *
from config import *
from .flightblock import FlightBlockList
from .waypointobject import Waypoint
import config

import logging

from collections import OrderedDict
from PyQt5.QtCore import QObject, pyqtSignal

logg = logging.getLogger(__name__)

class BagOfHolding(object):

    def __init__(self):
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

    def updateAirMissionStatus(self, msg):
        self.remianingMissionTime = msg.fieldvalues[0]
        if(msg.fieldvalues[1].split(",")[0] != 0):
            mission_array = msg.fieldvalues[1].split(",")
            mission_list = fancyList()

            task_array = msg.fieldvalues[2].split(",")

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
