#!/usr/bin/python3

import sys, getopt
import log, logging
import os
import argparse
import signal
import threading


from config import *
import ivylinker
from ui import UI
from database import importxml
from md5checker import findMD5

from interop.client import AsyncClient
from interoperability import MissionInformation, TelemetryThread, ObstacleThread


def argParser():
    '''
    Uses argparse to read arguements passed on startup. To pass a custom
    arguement on startup simply add the flag and then the arguement, as per below

    python3 ./main.py -l thisURL
    python3 ./main.py -l thisURL --flightPlan webster

    TO ADD ANOTHER ARGUEMENT:
    1) Add default value on config.py and on defaultArgs
    2) Add input arguement line
    (parser.add_argument('-shortFlag', '--longFlag', help='delimited list input', type=str))
    NOTE: args[longFlag] = newArguement
    3) Access arg in main function by argDict['longflag']
    '''

    defaultArgs = {'url': urlDefault, 'username':usernameDefault,
        'password': passwordDefault}

    parser = argparse.ArgumentParser()
    # Input arguements
    parser.add_argument('-l', '--url', help='delimited list input', type=str)
    parser.add_argument('-u', '--username', help='delimited list input', type=str)
    parser.add_argument('-p', '--password', help='delimited list input', type=str)
    # vars parses the namespace into a dictionary so we can iterate over the names
    args = vars(parser.parse_args())

    for key in args.keys():
        if args[key] is None:
            args[key] = defaultArgs[key]

    return args

class MissionCommander():
    def __init__(self, ivy_sender, logger):
        """
        Initializes a MissionCommander object.
        Args:
            ivy_sender: An ivylinker.IvySender object to which a
            message handler can be bound.
        """
        self.logger = logger
        self.foundXML = False
        self.ac_id = None
        self.loadedXML = threading.Event()
        self.loadedXML.clear()

        from database import BagOfHolding
        self.db = BagOfHolding()
        self.ivy_sender = ivy_sender
        self.ivy_sender.bindMessageHandler(self.ivyMsgHandler)

        self.loadedXML.wait()

    def loadXMLs(self, filepath, ac_id):
        importxml.bindDBandFilepath(os.path.join(*[filepath, 'flight_plan.xml']), self.db, ac_id)
        importxml.parseXML()
        prefixMandT = self.determineFlightPlan()
        importxml.bindDBandFilepath(os.path.join('MissAndTsk', prefixMandT + 'MissionsAndTasks.xml'), self.db, ac_id)
        importxml.parseXML()
        self.loadedXML.set()

    def determineFlightPlan(self):
        '''
        This is a dumb way to find out what MissionsAndTasks file we should use, but it works
        '''

        homePosition = self.db.waypoints['OrIgIn'].get_latlon()
        if ((str(homePosition['lat'])[0:6] == '53.638') and (str(homePosition['lon'])[0:8] == '-113.286')):
            return 'Bremner'
        if ((str(homePosition['lat'])[0:6] == '38.144') and (str(homePosition['lon'])[0:7] == '-76.427')):
            return 'Webster'
        else:
            logger.critical('Did not find MissionsAndTasks file - should make one presently')
            return ''

    def initiSync(self):
        from synchronizer import BagOfSynchronizing
        self.sync = BagOfSynchronizing()
        self.sync.startThread()

    def ivyMsgHandler(self, ac_id, msg):

        if self.foundXML:
            if (msg.name == "WP_MOVED"):
                self.db.updateWaypoint(msg)

            if (msg.name == "MISSION_STATUS"):
                self.db.updateAirMissionStatus(msg)

            if (msg.name == "NAVIGATION"):
                self.db.updateCurrentFlightBlock(msg.cur_block)

        else:
            if (msg.name == "ALIVE"):
                filepath = findMD5(msg.md5sum, self.logger)
                if filepath != None:
                    self.loadXMLs(filepath, ac_id)
                    self.foundXML = True
                    self.ivy_sender.AC_ID = ac_id
                    self.ac_id = ac_id

if __name__ == '__main__':
    log.init()
    argDict = argParser()
    logger = logging.getLogger(__name__)

    ivy_sender = ivylinker.IvySender(verbose=True)
    
    # run interIvy as submprocess!!
    mc = MissionCommander(ivy_sender, logger)
    ui = UI(mc.db, ivy_sender.sendMessage, mc.ac_id)

    # Allow Ctrl+C to kill the program with no cleanup
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    ui.run() # Finishes when UI window is closed
    print('Shutting down...')

    ivy_sender.shutdown()
