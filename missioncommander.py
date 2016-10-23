#from gi.repository import Gtk
from time import clock, sleep, time
import signal
import ivylinker
import maths
import threading

class main:
    def __init__( self ):
        self.shutdown = False
        self.interoprunning = False
        self.initIVY()
        self.initINTEROP()
        #signal.signal(signal.SIGINT, self.ctrlcshutdown)

    def ctrlcshutdown(self, signum, fram):
        self.shutdown = True


    def initIVY( self):
        print("Initializing ivylink")
        self.newmissionstatus = False
        self.lastmissionmsg = None
        self.lastgps = None
        self.lastattitude = None
        self.lastestimator = None
        self.telinfoavailable = False
        self.ivylink = ivylinker.CommandSender(verbose=True, callback = self.msg_handler)
        self.lastmissionmessagetime = clock()
        self.interopSD = True

    def initINTEROP(self):
        print("Initializing interop")
        self.lastmoveobjecttime = time()-10
        self.laststationojecttime = time()-10
        self.bypassinghashtable = 0
        self.bypassinghashtable1 = 0
        self.lastupdatetelemetry = time()-10
        self.objecttable = {}

    def startINTEROP(self, interopobject):
        if self.interoprunning == False:
            self.interoplink = interopobject
            self.interopSD = False
            self.intTH = threading.Thread(target=self.interophandler, args=[])
            self.intTH.start()

    def interophandler(self):
        self.interoprunning = True
        print("waiting for full telemetry message")
        while self.telinfoavailable==False:
            sleep(.02)
        print("Communicating with Interop Server")
        while self.interopSD == False:
            if self.lastmoveobjecttime + .1 < time():
                self.movinghandler()
                self.lastmoveobjecttime = time()

            if self.laststationojecttime + .1 < time():
                self.stationaryhandler()
                self.laststationojecttime = time()

            if ((self.lastupdatetelemetry + .05) < time()):
                self.telemetryhandler()
                tmp = time()
                #self.update_freq(1/(tmp - self.lastupdatetelemetry))
                self.lastupdatetelemetry = tmp

            sleep(0.05)
        self.interoprunning = False

        print("shutting down interoperability")
        self.objectdeletion()


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
            self.ivylink.add_shape("create",i, ob)
            i= i+1

    def movinghandler(self):
        objects = self.interoplink.getobstacleinfo()
        moving = objects.get("moving_obstacles")
        i = 20

        for ob in moving:
            self.objecttable[i] = ob
            self.ivylink.add_shape("create",i, ob)
            i= i+1

    def objectdeletion(self):
        for k in self.objecttable.keys():
            self.ivylink.add_shape("delete",k, self.objecttable[k])
        sleep(0.1)


    def telemetryhandler(self):
        lat, lon = maths.utm_to_DD((self.lastgps.fieldvalues[1]), ( self.lastgps.fieldvalues[2] ), self.lastgps.fieldvalues[9])
        alt = self.lastestimator.fieldvalues[0]
        course = float(self.lastattitude.fieldvalues[1]) * 180 / 3.14 + 90
        tele = {'latitude':float(lat), 'longitude':float(lon), 'altitude_msl':float(alt), 'uas_heading':course}
        self.interoplink.updatetelemetry(tele)


if __name__ == "__main__":
    main()
