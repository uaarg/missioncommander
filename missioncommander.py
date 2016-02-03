from gi.repository import Gtk
from time import clock, sleep


import threading
import gui
import interopclient
import maths


class main:

    def __init__( self ):
        self.shutdown = False
        self.newmissionstatus = False
        self.initGUI()
        self.initINTEROP()
        if self.interoplink.loginsucess == True:
            self.interopTH = threading.Thread(target = self.interophandler)
            self.interopTH.start()
        self.guihandler()

    def initIVY( self):
        print("Initializing ivylink")
        self.lastmissionmsg = None
        self.lastgps = None
        self.lastattitude = None
        self.lastestimator = None
        self.telinfoavailable = False
        self.ivylink = ivylinker.CommandSender(verbose=True, callback = self.msg_handler)
        self.lastmissionmessagetime = clock()

    def initINTEROP(self):
        print("Initializing interop")
        self.interoplink = interopclient.Connection()
        self.lastmoveobjecttime = clock()-10
        self.laststationojecttime = clock()-10
        self.bypassinghashtable = 0
        self.bypassinghashtable1 = 0
        self.lastupdatetelemetry = clock()-10
        self.objecttable = {}

    def initGUI( self):
        print("Initializing GUI")
        self.win = gui.MissionGUI(shutdowncb = self.shutdownprog)
        self.win.window.show_all()

    def guihandler(self):
        print("Opening GUI")
        while self.shutdown==False:
            if self.newmissionstatus == True:
                self.win.update_uav_queue(self.lastmissionmsg)
                self.newmissionstatus = False
            elif Gtk.events_pending():
                Gtk.main_iteration()
            sleep(0.01)

    def interophandler(self):
        print("Communicating with Interop Server")
        while True:
            if self.lastmoveobjecttime + .01 < clock():
                self.movinghandler()
                self.lastmoveobjecttime = clock()

            if self.laststationojecttime + .1 < clock():
                self.stationaryhandler()
                self.laststationojecttime = clock()

            if self.lastupdatetelemetry + .01 <clock() and self.telinfoavailable :
                self.telemetryhandler()
                self.lastupdatetelemetry = clock()

            if self.shutdown == True:
                print("shutting down interoperability")
                self.objectdeletion()
                return 0
            sleep(0.02)

    def msg_handler(self, acid, msg):
        if (msg.name == "MISSION_STATUS" and (self.lastmissionmessagetime + .1) < (clock())):
            self.lastmissionmsg = msg
            self.newmissionstatus = True
            self.lastmissionmessagetime = clock()

        if (msg.name == "GPS"):
            self.lastgps = msg

        if (msg.name == "ATTITUDE"):
            self.lastattitude = msg

        if (msg.name == "ESTIMATOR"):
            self.lastestimator = msg

        if (self.lastgps != None) and (self.lastattitude != None) and (self.lastestimator != None):
            self.telinfoavailable = True

    def stationaryhandler(self):
        objects = self.interoplink.getobstacleinfo()
        station = objects.get("stationary_obstacles")
        i=1

        for ob in station:
            self.objecttable[i] = ob
            self.ivylink.add_obstacle_dict("create",i, ob)
            i= i+1

    def movinghandler(self):
        objects = self.interoplink.getobstacleinfo()
        moving = objects.get("moving_obstacles")
        i = 20

        for ob in moving:
            self.objecttable[i] = ob
            self.ivylink.add_obstacle_dict("update",i, ob)
            i= i+1

    def objectdeletion(self):
        for k in self.objecttable.keys():
            self.ivylink.add_obstacle_dict("delete",k, self.objecttable[k])
        sleep(0.1)
        self.ivylink.shutdown()


    def telemetryhandler(self):
        lat, lon = maths.utm_to_DD((self.lastgps.fieldvalues[1]), ( self.lastgps.fieldvalues[2] ), self.lastgps.fieldvalues[9])
        alt = self.lastestimator.fieldvalues[0]
        course = float(self.lastattitude.fieldvalues[1]) * 180 / 3.14
        tele = {'latitude':float(lat), 'longitude':float(lon), 'altitude_msl':float(alt), 'uas_heading':course}
        self.interoplink.updatetelemetry(tele)

    def shutdownprog(self):
        self.shutdown = True


if __name__ == "__main__":
    main()
#    try:
#        p = main#
#        p.start()#
#    except KeyboardInterrupt:
#        print 'Interrupted'
#        p.shutdownprog()
#        print("SDFKJSDLFKJSDLKFJ")
#        sys.exit(0)
