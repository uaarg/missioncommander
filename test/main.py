#!/usr/bin/python3

import sys, getopt
import logging
import os
from time import sleep

from ivylinker import *

def gen_mission_msg():
    msg = pprzmsg("datalink", "MISSION_GOTO_WP")

    msg['ac_id'] = 5
    msg['insert'] = 1

    msg['duration'] = -1
    msg['index'] = 23
    msg['task'] = 28
    msg['insert_index'] = 1
    msg['wp_east'] = 0
    msg['wp_north'] = 0
    msg['wp_alt'] = 100
    print(msg)
    return msg



def ivyMsgHandler(ac_id, msg):
    if (msg.name == "WALDO_MSG"):
        self.db.updateTelemetry(msg)

    if (msg.name == "WP_MOVED"):
        self.db.updateWaypoint(msg)

    if (msg.name == "MISSION_STATUS"):
        self.db.updateAirMissionStatus(msg)

print("hello")
sleep(1)
sendIvyMSG(gen_mission_msg())

print("hello")
shutdownIvyBus()
#bindIvyMsgHandler(self.ivyMsgHandler)
