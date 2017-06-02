from utils import *
from config import *
import config
import time
import threading


class BagOfSynchronizing(object):

    def __init__(self, db, gms):
        self.db = db

        self.groundMissionStatus = gms

        self.count = 0
        self.reset = True
        self.localMissionStatus = fancyList()
        self.firstStart = True

    def missionUpdateSent(self):
        self.count = 3

    def newMissionStatusMessage(self, airMissionStatus):
        length = airMissionStatus.getLength()
        self.groundMissionStatus.replaceAll(airMissionStatus)

        if length == 0:
            return

        if self.count != 0:
            self.count = self.count - 1
            return
        
        self.groundMissionStatus.replaceAll(airMissionStatus)


        