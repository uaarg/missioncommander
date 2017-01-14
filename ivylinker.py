#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path, getenv

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python/")

from pprzlink.ivy  import IvyMessagesInterface
from pprzlink.message   import PprzMessage

maxTargets = 20 # /2 is the max number of eiether moving or stationary targets we can handle. SAME AS missioncommander.py's global var


class CommandSender(IvyMessagesInterface):
    def __init__(self, verbose=False, callback = None):
        self.verbose = verbose
        self.callback = callback
        self._interface = IvyMessagesInterface("Mission Commander", start_ivy=False)
        self._interface.subscribe(self.message_recv)
        self._interface.start()
        self.tooManyTargets = 0

    def message_recv(self, ac_id, msg):
        if (self.verbose and self.callback != None):
            self.callback(ac_id, msg)

    def shutdown(self):
        print("Shutting down ivy interface...")
        self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def add_mission_command_dict(self, ac_id, insert, msg_id, msgs):

        msg = PprzMessage("datalink", msg_id)

        msg['ac_id'] = ac_id
        msg['insert'] = insert
        msg['duration'] = msgs.get('duration')

        if msg_id == 'MISSION_GOTO_WP_LLA':
            msg['wp_lat'] = msgs.get('wp_lat')
            msg['wp_lon'] = msgs.get('wp_lon')
            msg['wp_alt'] = msgs.get('wp_alt')

        elif msg_id == 'MISSION_CIRCLE_LLA':
            msg['center_lat'] = msgs.get('center_lat')
            msg['center_lon'] = msgs.get('center_lon')
            msg['center_alt'] = msgs.get('center_alt')
            msg['radius'] = msgs.get('radius')

        elif msg_id == 'MISSION_SEGMENT_LLA':
            msg['segment_lat_1'] = msgs.get('segment_lat_1')
            msg['segment_lon_1'] = msgs.get('segment_lon_1')
            msg['segment_lat_2'] = msgs.get('segment_lat_2')
            msg['segment_lon_2'] = msgs.get('segment_lon_2')

        elif msg_id == 'MISSION_PATH_LLA':
            msg['point_lat_1'] = msgs.get('point_lat_1')
            msg['point_lon_1'] = msgs.get('point_lon_1')
            msg['point_lat_2'] = msgs.get('point_lat_2')
            msg['point_lon_2'] = msgs.get('point_lon_2')
            msg['point_lat_3'] = msgs.get('point_lat_3')
            msg['point_lon_3'] = msgs.get('point_lon_3')
            msg['point_lat_4'] = msgs.get('point_lat_4')
            msg['point_lon_4'] = msgs.get('point_lon_4')
            msg['point_lat_5'] = msgs.get('point_lat_5')
            msg['point_lon_5'] = msgs.get('point_lon_5')
            msg['path_alt'] = msgs.get('path_alt')
            msg['nb'] = msgs.get('nb')

        elif msg_id == 'MISSION_SURVEY_LLA':
            msg['survey_lat_1'] = msgs.get('survey_lat_1')
            msg['survey_lon_1'] = msgs.get('survey_lon_1')
            msg['survey_lat_2'] = msgs.get('survey_lat_2')
            msg['survey_lon_2'] = msgs.get('survey_lon_2')
            msg['survey_alt'] = msgs.get('survey_alt')


#        print("Sending message: %s" % msg)
        self._interface.send(msg)

    def add_shape(self, status, obstacle_id, obmsg):
        msg = PprzMessage("ground", "SHAPE")
        msg['id'] = int(obstacle_id)

        if obstacle_id >= (maxTargets/2 -1 ):
            msg['fillcolor'] = "blue"
            msg['linecolor'] = "blue"
            msg['opacity'] = 2
        elif obstacle_id >= (maxTargets -1):
            msg['fillcolor'] = "red"
            msg['linecolor'] = "red"
            msg['opacity'] = 1
        elif obstacle_id >= (3*maxTargets/2 -1):
            msg['fillcolor'] = "orange"
            msg['linecolor'] = "orange"
            msg['opacity'] = 2
        elif obstacle_id >= (2*maxTargets -1):
            msg['fillcolor'] = "red"
            msg['linecolor'] = "red"
            msg['opacity'] = 1
        else:
            if (self.tooManyTargets< maxTargets):
                print("TOO MANY OBSTACLES, things are failing")
                self.tooManyTargets = self.tooManyTargets +1

        msg['status'] = 0 if status=="create" else 1
        msg['shape'] = 0
        msg['latarr'] = [int(obmsg.get("latitude")*10000000.),int(obmsg.get("latitude")*10000000.)]
        msg['lonarr'] = [int(obmsg.get("longitude")*10000000.),int(obmsg.get("longitude")*10000000.)]
        msg['radius'] = int(obmsg.get("sphere_radius") if "sphere_radius" in obmsg else obmsg.get("cylinder_radius"))
        msg['text'] = "NULL"

        self._interface.send(msg)


# add_mission_command(msg_id = "MISSION_GOTO_WP_LLA", ac_id=5, insert = "0", wp_lat=434624607, wp_lon=12723454, wp_alt=700, duration =60)
