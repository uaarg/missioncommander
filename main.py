import sys, getopt
from xmlparser import *
from config import *
from ivylinker import *
from ui import UI

from interop.client import AsyncClient
from interoperability import TelemetryThread, ObstacleThread


def argparser(argv):
    url = "http://localhost:8000"
    username = "testuser"
    password = "testpass"
    try:
        opts, args = getopt.getopt(argv,"hl:u:p:",["url=","username=","password="])
    except getopt.GetoptError:
        print('main.py -l <url> -u <username> -p <password>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -l <url> -u <username> -p <password>')
            sys.exit()
        elif opt in ("-l", "--url"):
            url = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
    return password, username, url


class MissionCommander(object):
    def __init__(self):
        self.initDatabase()
        # Todo. Fix XML import
        # importxml('sampleflightplan.xml', self.db)
        # Do XML loading stuff
        bindIvyMsgHandler(self.ivyMsgHandler)
        self.ui = UI()
        self.ui.run()

    def initDatabase(self):
        from database import bagOfHolding
        self.db = bagOfHolding()

    def ivyMsgHandler(self, ac_id, msg):
        if (msg.name == "WALDO_MSG"):
            self.db.updateTelemetry(msg)
        
        if (msg.name == "WP_MOVED"):
            self.db.updateWaypoint(msg)
        


if __name__ == '__main__':
    password, username, url = argparser(sys.argv[1:])
    if INTEROP_ENABLE:
        interop = AsyncClient(url, username, password)
    mc = MissionCommander()

    if INTEROP_ENABLE:
        telem_thread = TelemetryThread(interop, mc.db.airplane)
        obstacle_thread = ObstacleThread(interop, glbivy)
        telem_thread.start()
        obstacle_thread.start()
        obstacle_thread.join()
        telem_thread.join()