from utils import *
from config import *
import config
import time
import threading


class BagOfSynchronizing(object):

    def __init__(self, db):
        self.db = db
        self.threadShutdown = True
        self.th = threading.Thread(target=self.runner, args=[])
        self.changedMissionQueue = fancyList()
        self.changedMissionEvent = threading.Event()
        self.changedMissionEvent.clear()

    def startThread(self):
        if (self.threadShutdown):
            self.threadShutdown = False
            self.th.start()
        else:
            print("First stop the Sync Thread before starting a new one")

    def stopThread(self):
        self.threadShutdown = True

    def runner(self):
        while not(self.threadShutdown) :
            self.changedMissionEvent.wait()
            print("include code to fix this")
            self.changedMissionEvent.clear()
            print("Sync Thread is running")


    def updatedMission(self, mission):
        ''' Call this function is a waypoint has bee updated.
        If mission is in airMissionStatusMSG then the runner Thread will update'''
        self.changedMissionQueue.append(mission)
        self.changedMissionEvent.set()
