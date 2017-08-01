#!/usr/bin/python3

import log, logging
import argparse
import signal
import threading
import os

from config import *
import ivylinker

from md5checker import findMD5
from database import importxml
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

class interIvy():

    def __init__(self, ivySender, logger, TelemetryThread):
        '''
        Instilizes an interIvy object
        '''
        self.TelemetryThread = TelemetryThread
        self.logger = logger
        self.ac_id = None
        self.loadedXML = threading.Event()
        self.loadedXML.clear()

        from database import BagOfHolding
        self.db = BagOfHolding()
        self.ivy_sender = ivySender
        self.ivy_sender.bindMessageHandler(self.ivyMsgHandler)

        self.foundAC_ID = False

        self.loadedXML.wait()


    def loadXMLs(self, filepath, ac_id):
        importxml.bindDBandFilepath(os.path.join(*[filepath, 'flight_plan.xml']), self.db, ac_id)
        importxml.parseXML()
        self.loadedXML.set()

    def ivyMsgHandler(self, ac_id, msg):
        if self.foundAC_ID:
            if (msg.name == "WALDO_MSG"):
                self.TelemetryThread.updateTelemetry(msg)

        else:
            if (msg.name == "ALIVE"):
                filepath = findMD5(msg.md5sum, self.logger)
                if filepath != None:
                    self.loadXMLs(filepath, ac_id)
                    self.foundAC_ID = True
                    self.ivy_sender.AC_ID = ac_id
                    self.ac_id = ac_id

def mainInterop():
    '''
    Function kept as a placeholder to call the interops functions from MC. __main__
    will also call this to initialize InterIvy.
    '''
    log.init()
    argDict = argParser()
    logger = logging.getLogger(__name__)
    serverIsUp = True
    try:
        interop = AsyncClient(argDict['url'], argDict['username'], argDict['password'],  timeout = 1000)
    except Exception as e:
        logging.critical('Failed to connect to interop server due to: \n'+str(e)+'.\nOperation of Interop threads are supressed.\n')
        serverIsUp = False

    ivy_sender = ivylinker.IvySender(verbose=True)

    telem_thread = TelemetryThread(interop)
    telem_thread.start()

    II = interIvy(ivy_sender, logger, telem_thread)

    # Allow Ctrl+C to kill the program with no cleanup
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if serverIsUp:
        missionInfo = MissionInformation(interop, ivy_sender.sendMessage)
        missionInfo.getMissionInformation()
        try:
            missionInfo.sendIvyOffAxisShape()
            missionInfo.sendIvyEmergentTarget(II.ac_id,II.db)
            missionInfo.sendIvyGroupOfWaypoints(II.ac_id,II.db, 'OpArea')
            missionInfo.sendIvyGroupOfWaypoints(II.ac_id,II.db, 'SearchArea')
            missionInfo.sendIvyGroupOfWaypoints(II.ac_id,II.db, 'WptNav')
            obstacle_thread = ObstacleThread(interop, ivy_sender.sendMessage)
            obstacle_thread.start()
        except Exception as e:
            logging.critical('Failed to plot interop details (OAX, LKN, OpArea, SearchArea, WptNav and Obstacles) because of \n' + str(e))

    while True:
        pass

    if serverIsUp:
        telem_thread.stop()
        if not(missionInfo.mission_info is None):
            obstacle_thread.stop()

    ivy_sender.shutdown()

    if serverIsUp:
        telem_thread.join()
        if not(missionInfo.mission_info is None):
            obstacle_thread.join()


if __name__ == '__main__':
    mainInterop()
