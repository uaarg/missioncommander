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
from xmlparser import *
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
            current_flight_plan: ???
            ivy_sender: An ivylinker.IvySender object to which a
            message handler can be bound.
        """
        self.logger = logger
        self.foundXML = False
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
        This is a dumb way to find out what MissionsAndTasks file we should use. But its easy to do.
        '''
        print(self.db.waypoints['OrIgIn'].get_latlon())

        if (float(self.db.waypoints['OrIgIn'].get_latlon()['lat'])>49.0): #AKA the origin is in Canada
            return 'Bremner'
        else:
            return ''

    def initiSync(self):
        from synchronizer import BagOfSynchronizing
        self.sync = BagOfSynchronizing()
        self.sync.startThread()

    def ivyMsgHandler(self, ac_id, msg):
        if self.foundXML:
            if (msg.name == "WALDO_MSG"):
                self.db.updateTelemetry(msg)

            if (msg.name == "WP_MOVED"):
                self.db.updateWaypoint(msg)

            if (msg.name == "MISSION_STATUS"):
                self.db.updateAirMissionStatus(msg)
        else:
            if (msg.name == "ALIVE"):
                filepath = findMD5(msg.md5sum, self.logger)
                if filepath != None:
                    print(filepath)
                    self.loadXMLs(filepath, ac_id)
                    self.foundXML = True
                    self.ivy_sender.AC_ID = ac_id
                    self.ivy_sender.sendMessage(self.db.flightBlocks.getFlightBlock("Mission").gen_change_block_msg())

if __name__ == '__main__':
    log.init()
    argDict = argParser()
    logger = logging.getLogger(__name__)

    serverIsUp = True
    try:
        interop = AsyncClient(argDict['url'], argDict['username'], argDict['password'])
    except Exception as e:
        logging.critical('Interop failed to initialize due to: \n'+str(e)+'.\nOperation of Interop threads are supressed.\n')
        serverIsUp = False

    ivy_sender = ivylinker.IvySender(verbose=True)
    mc = MissionCommander(ivy_sender, logger)
    ui = UI(mc.db, ivy_sender.sendMessage)

    # Allow Ctrl+C to kill the program with no cleanup
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if serverIsUp:
        missionInfo = MissionInformation(interop, ivy_sender.sendMessage)
        missionInfo.getMissionInformation()
        missionInfo.sendIvyOffAxisShape()
        missionInfo.sendIvyEmergentTarget(5,mc.db)

        telem_thread = TelemetryThread(interop, mc.db.airplane)
        obstacle_thread = ObstacleThread(interop, ivy_sender.sendMessage)

        telem_thread.start()
        obstacle_thread.start()

    ui.run() # Finishes when UI window is closed
    print('Shutting down...')

    if serverIsUp:
        obstacle_thread.stop()
        telem_thread.stop()

    ivy_sender.shutdown()

    if serverIsUp:
        obstacle_thread.join()
        telem_thread.join()
