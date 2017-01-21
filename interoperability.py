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
from database import AirplaneTelemetry
from obstacle import Obstacle

class MissionInformation():
    """
    Class for obtaining information about a mission from the interoperability server, then sending it over the Ivy bus.
    Args:
        interopclient: An interoperability client object to handle sending data to the interoperability server.
    """
    def __init__(self, interopclient, ivysender):
        self.interopclient = interopclient
        self.ivysender = ivysender
        self.mission_info = {}

    def getMissionInformation(self):
        """
        Gets mission information from the interoperability server.
        """
        try:
            self.mission_info = interopclient.get_missions()
        except InteropError as error:
            print(error.message)
        
    def sendIvyEmergentTarget(self, ac_id, emergent_waypoint_id, altitude):
        """
        Sends updated information about the location of the emergent target.
        This is dependent on there being an existing waypoint in the flight plan that can be used for the emergent target task.
        Args:
            ac_id: The aircraft ID, an integer.
            emergent_waypoint_id: The id of the waypoint associated with the emergent target, an integer.
            altitude: The desired MSL altitude for the emergent target waypoint, in metres.
        """
        msg = PprzMessage("ground", "SHAPE")
        msg['wp_id'] = emergent_waypoint_id
        msg['ac_id'] = ac_id
        msg['lat'] = int(
            self.mission_info["emergent_last_known_pos"]["latitude"] * 1e7
        )
        msg['lon'] = int(
            self.mission_info["emergent_last_known_pos"]["longitude"] * 1e7
        )
        msg['alt'] = int(altitude * 1e3)

        self.ivysender(msg)

class TelemetryThread(Thread):
    """
    Thread to send telemetry information.
    """
    def __init__(self, interopclient, plane):
        super(TelemetryThread, self).__init__()
        self.plane = plane
        self.interopclient = interopclient

    def run(self):
        while True:
            self.plane.teleAvail.wait()
            try:
                t = self.plane.getTelemetry()
                if t:
                    telem = Telemetry(t['latitude'], t['longitude'], t['altitude_msl'], t['uas_heading'])
                    r = self.interopclient.post_telemetry(telem).result()

            except InteropError as error:
                print(error)

    def getDataSendFrequency():
        """
        Returns the rate, in Hz, that the interoperability server
        is being updated with telemetry at.
        """

class ObstacleThread(Thread):
    """
    Thread to query for obstacle information,
    update the program's internal store of obstacles,
    and send obstacle information over the Ivy bus.
    """

    @staticmethod
    def _sendIvyShapeMessage(obstacle_id, obstacle, ivysender):
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
        msg['latarr'] = [int(obstacle.lat * 10000000.)] * 2
        msg['lonarr'] = [int(obstacle.lon * 10000000.)] * 2
        msg['radius'] = obstacle.geom_data['radius']
        if obstacle.shape == 'cylinder':
            msg['text'] = "%.2fm" % (obstacle.geom_data['height'])
        if obstacle.shape == 'sphere':
            msg['text'] = "%.2fm" % (obstacle.geom_data['altitude'])

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

    def run(self):
        while True:
            try:
                async_future = self.interopclient.get_obstacles()
                stationary, moving = async_future.result()
                ob_list = []
                for interop_ob in stationary + moving:
                    ob_list.append(Obstacle(interop_ob))
                self.obstacles = ob_list

                obstacle_id = 0
                for obstacle in self.obstacles:
                    sendIvyShapeMessage(obstacle_id, obstacle, self.ivysender)
                    obstacle_id += 1

            except InteropError as error:
                print(error.message)
            
            sleep(self.sleepDuration)

    

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
