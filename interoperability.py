"""
Queries interoperability server for relevant information,
then passes that information to the rest of the program.
"""
from threading import Thread
from time import sleep

from interop.client import AsyncClient
from interop.exceptions import InteropError
from interop.interop_types import Telemetry
from interop.interop_types import StationaryObstacle, MovingObstacle

from pprzlink.message import PprzMessage
from database import AirplaneTelemetry, Waypoint
from obstacle import Obstacle
from config import *

import logging
logger = logging.getLogger(__name__)


class MissionInformation():
    """
    Class for obtaining information about a mission from the interoperability server, then sending it over the Ivy bus.
    Args:
        interopclient: An interoperability client object to handle sending data to the interoperability server.
    """
    def __init__(self, interopclient, ivysender):
        self.interopclient = interopclient
        self.ivysender = ivysender

    def getMissionInformation(self):
        """
        Gets mission information from the interoperability server.
        """
        try:
            missions = self.interopclient.get_missions().result()
            logger.info(
                "Received mission information from interop server: %s", missions
            )
            # Interop Server may have more than one
            activeMissions = []
            for mission in missions:
                if mission.active:
                    activeMissions.append(mission)
            if len(activeMissions) is 1:
                self.mission_info = activeMissions[0]
            else:
                logger.critical('Found ' + str(len(activeMissions)) + ' active on the Interop Server. Which one should we use?')
                self.mission_info = None
        except InteropError as error:
            logger.error(error.message)

            self.mission_info = None

    def sendIvyEmergentTarget(self, ac_id, db):
        """
        Sends updated information about the location of the emergent target.
        This is dependent on there being an existing waypoint in the flight plan that can be used for the emergent target task.
        Args:
            ac_id: The aircraft ID, an integer.
            emergent_waypoint_id: The id of the waypoint associated with the emergent target, an integer.
        """
        if db.waypoints['LKN'] is not None:
            if self.mission_info.emergent_last_known_pos is not None:
                LKNwpt = db.waypoints['LKN']
                LKNwpt.update_latlon(self.mission_info.emergent_last_known_pos.latitude, self.mission_info.emergent_last_known_pos.longitude)
                msg = LKNwpt.gen_move_waypoint_msg(ac_id)

                self.ivysender(msg)
                logger.info('Moved the LKN waypoint to Lat:'+str(self.mission_info.emergent_last_known_pos.latitude)+' Lon:'+str(self.mission_info.emergent_last_known_pos.longitude))
            else:
                logger.critical('LKN waypoint not found on Interop server.')
        else:
            logger.critical('LKN waypoint not found in list of Waypoints. Lask Known Location from Interop Server is '+ str(self.mission_info.emergent_last_known_pos.latitude) + ' ' + str(self.mission_info.emergent_last_known_pos.longitude))

    def sendIvyOffAxisShape(self):
        """
        Sends a message displaying the shape information for the off-axis target.
        """
        if self.mission_info.off_axis_target_pos is not None:
            logger.info('Off Axis Target is at' +str(self.mission_info.off_axis_target_pos))
            msg = PprzMessage("ground", "SHAPE")
            msg['id'] = 99
            msg['linecolor'] = 'white'
            msg['fillcolor'] = 'blue'
            msg['opacity'] = 2
            msg['shape'] = 0
            msg['status'] = 0
            msg['latarr'] = [int(
                self.mission_info.off_axis_target_pos.latitude * 1e7
            )] * 2
            msg['lonarr'] = [int(
                self.mission_info.off_axis_target_pos.longitude * 1e7
            )] * 2
            msg['radius'] = 10
            msg['text'] = 'OAX'

            self.ivysender(msg)
        else:
            logger.critical('Interop server does not have an OAX target.')

    def sendIvyGroupOfWaypoints(self,ac_id,db,group):
        '''
        Sends a group of waypoint moves over the Ivy bus as according to the interop-
        provided posistions. Currently supports the 'Operational Area', 'Search Area'
        and 'Waypoint Navigation'
        '''

        wptPrefix = None
        interopWaypointGroup = None
        newAltitude = None
        GCSwaypoints = []

        if group == 'OpArea':
            wptPrefix = '_oparea'
            hasAlt = False
            interopWaypointGroup = self.mission_info.fly_zones[0].boundary_pts
        elif group == 'SearchArea':
            wptPrefix = '_searchArea'
            hasAlt = False
            interopWaypointGroup = self.mission_info.search_grid_points
        elif group == 'WptNav':
            wptPrefix = 'wp'
            hasAlt = True
            interopWaypointGroup = self.mission_info.mission_waypoints
        else:
            raise AttributeError('Incorrect group called with moveGroupOfWaypoints')


        for wptName in db.waypoints.keys():
            if wptName[0:len(wptPrefix)] == wptPrefix:
                GCSwaypoints.append(wptName)
        assert type(GCSwaypoints) is list

        if len(GCSwaypoints) < len(interopWaypointGroup):
            logger.critical('Interop Server has more '+group+' area points then the GCS. Moving the first ' +str(len(GCSwaypoints))+ ' waypoints into position')
        for index in range(0,len(GCSwaypoints)):
            InteropIndex = index
            while InteropIndex >= len(interopWaypointGroup):
                InteropIndex = InteropIndex - len(interopWaypointGroup)

            if hasAlt: # remember height info on the server is in ft msl
                newAltitude = interopWaypointGroup[InteropIndex].altitude_msl/feetInOneMeter
            else:
                newAltitude = None

            db.waypoints[wptPrefix + str(index +1 )].update_latlon(interopWaypointGroup[InteropIndex].latitude, interopWaypointGroup[InteropIndex].longitude, None, newAltitude)
            msg = db.waypoints[wptPrefix + str(index +1)].gen_move_waypoint_msg(ac_id)
            self.ivysender(msg)
            logger.info('Moved ' +wptPrefix+str(index+1)+ ' to the Interop server position for it.')



class TelemetryThread(Thread):
    """
    Thread to send telemetry information.
    """
    def __init__(self, interopclient, plane):
        super(TelemetryThread, self).__init__()
        self.plane = plane
        self.interopclient = interopclient
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.plane.teleAvail.wait()
            try:
                t = self.plane.getTelemetry()
                if t:
                    telem = Telemetry(t['latitude'], t['longitude'], t['altitude_msl'], t['uas_heading'])
                    r = self.interopclient.post_telemetry(telem).result()

            except InteropError as error:
                logger.error(error.message)

    def getDataSendFrequency():
        """
        Returns the rate, in Hz, that the interoperability server
        is being updated with telemetry at.
        """

    def stop(self):
        self.plane.teleAvail.set()
        self.running = False

class ObstacleThread(Thread):
    """
    Thread to query for obstacle information,
    update the program's internal store of obstacles,
    and send obstacle information over the Ivy bus.
    """

    @staticmethod
    def sendIvyShapeMessage(obstacle_id, obstacle, ivysender):
        """
        Send a shape message over the Ivy bus for a given obstacle.

        Args:
            obstacle_id: The ID of the obstacle.
            obstacle: An Obstacle object.
            ivysender: A callback to a function used to send Ivy messages, given a message dictionary.
        """
        msg = PprzMessage("ground", "SHAPE")
        msg['id'] = obstacle_id
        msg['linecolor'] = "white"
        msg['fillcolor'] = "red" if obstacle.moving else "orange"
        msg['opacity'] = 1
        msg['shape'] = 0
        msg['status'] = 0
        msg['latarr'] = [int(obstacle.lat * 1e7)] * 2
        msg['lonarr'] = [int(obstacle.lon * 1e7)] * 2
        msg['radius'] = obstacle.geom_data['radius']
        if obstacle.shape == 'cylinder':
            msg['text'] = "%.2fm" % (obstacle.geom_data['height'] - Waypoint.flightParams['ground_alt'])
        if obstacle.shape == 'sphere':
            msg['text'] = "%.2fm" % (obstacle.geom_data['altitude'] - Waypoint.flightParams['ground_alt'])

        ivysender(msg)

    def __init__(self, interopclient, ivysender, update_frequency=2):
        """
        Constructor for an ObstacleThread.

        Args:
            interopclient: An interoperability client object to handle sending data to the interoperability server.
            ivysender: A callback to a function used to send Ivy messages, given a message dictionary.
            updatefrequency: The frequency, in Hz, at which this thread should send obstacle messages over the Ivy bus.
        """
        super(ObstacleThread, self).__init__()
        self.interopclient = interopclient
        self.ivysender = ivysender
        self.obstacles = []
        self.sleepDuration = 1.0 / update_frequency
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                async_future = self.interopclient.get_obstacles()
                stationary, moving = async_future.result()
                logger.info('Stationary Obstacles '+str(stationary))
                logger.info('Moving Obstacles '+str(moving))
                ob_list = []
                for interop_ob in stationary + moving:
                    ob_list.append(Obstacle(interop_ob))
                self.obstacles = ob_list
                obstacle_id = 1
                for obstacle in self.obstacles:

                    self.sendIvyShapeMessage(
                        obstacle_id, obstacle, self.ivysender
                    )

                    obstacle_id += 1

            except InteropError as error:
                logger.error(error.message)

            sleep(self.sleepDuration)

    def stop(self):
        self.running = False



def main():
    config = {
        'url': "http://127.0.0.1:8000",
        'username': 'testuser',
        'password': 'testpass'
    }
    plane = AirplaneTelemetry()
    plane.positionFlag = plane.altitudeFlag = plane.headingFlag = True
    plane.newPosition((57.0, -128.0))
    plane.newAltitude(45.0)
    plane.newHeading(180.0)
    interop = AsyncClient(config['url'], config['username'], config['password'])
    telem = TelemetryThread(interop, plane)

    telem.start()
    telem.join()

if __name__ == "__main__":
    main()
