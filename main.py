#!/usr/bin/python3

import sys, getopt
import log, logging
import os
import argparse


from xmlparser import *
from config import *
from ivylinker import *
from ui import UiThread

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
        'password': passwordDefault, 'flightPlan': currentFlightPlanDefault }

    parser = argparse.ArgumentParser()
    # Input arguements
    parser.add_argument('-l', '--url', help='delimited list input', type=str)
    parser.add_argument('-u', '--username', help='delimited list input', type=str)
    parser.add_argument('-p', '--password', help='delimited list input', type=str)
    parser.add_argument('-x', '--flightPlan', help='delimited list input', type=str)
    # vars parses the namespace into a dictionary so we can iterate over the names
    args = vars(parser.parse_args())

    for key in args.keys():
        if args[key] is None:
            args[key] = defaultArgs[key]

    return args

class MissionCommander(object):
    def __init__(self, currentFlightPlan):
        self.initDatabase()
        importxml.bindDBandFilepath(os.path.join(*[PPRZ_SRC, 'conf/flight_plans/UAARG', currentFlightPlan]), self.db)
        importxml.parseXML()
        importxml.bindDBandFilepath('MissionsAndTasks.xml', self.db)
        importxml.parseXML()
        bindIvyMsgHandler(self.ivyMsgHandler)

    def initDatabase(self):
        from database import BagOfHolding
        self.db = BagOfHolding()

    def initiSync(self):
        from synchronizer import BagOfSynchronizing
        self.sync = BagOfSynchronizing()
        self.sync.startThread()

    def ivyMsgHandler(self, ac_id, msg):
        if (msg.name == "WALDO_MSG"):
            self.db.updateTelemetry(msg)

        if (msg.name == "WP_MOVED"):
            self.db.updateWaypoint(msg)

        if (msg.name == "MISSION_STATUS"):
            self.db.updateAirMissionStatus(msg)

if __name__ == '__main__':
    log.init()
    argDict = argParser()
    serverIsUp = True
    logger = logging.getLogger(__name__)
    interop = None
    try:
        interop = AsyncClient(argDict['url'], argDict['username'], argDict['password'])
    except Exception as e:
        logging.critical('Interop failed to initialize due to: \n'+str(e)+'.\nOperation of Interop threads are supressed.\n')
        serverIsUp = False

    if serverIsUp:
        missionInfo = MissionInformation(interop, sendIvyMSG)
        missionInfo.getMissionInformation()
        missionInfo.sendIvyOffAxisShape()

    mc = MissionCommander(argDict['flightPlan'])

    if serverIsUp:
        telem_thread = TelemetryThread(interop, mc.db.airplane)
        obstacle_thread = ObstacleThread(interop, sendIvyMSG)

    ui_thread = UiThread(mc.db)

    if serverIsUp:
        telem_thread.start()
        obstacle_thread.start()

    ui_thread.start()
    ui_thread.join()

    if serverIsUp:
        obstacle_thread.join()
        telem_thread.join()
