"""
Queries interoperability server for relevant information,
then passes that information to the rest of the program.
"""
from threading import Thread

from interop.client import AsyncClient
from interop.exceptions import InteropError
from interop.interop_types import Telemetry

from database import AirplaneTelemetry

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
            try:
                t = self.plane.getTelemetry()
                if t:
                    telem = Telemetry(t['latitude'], t['longitude'], t['altitude_msl'], t['uas_heading'])
                    r = self.interopclient.post_telemetry(telem)

            except InteropError as error:
                print(error.message)

    def getDataSendFrequency():
        """
        Returns the rate, in Hz, that the interoperability server
        is being updated with telemetry at.
        """

class ObstacleThread(Thread):
    """
    Thread to query for obstacle information
    and update the program's 
    """

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