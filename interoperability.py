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

def main():
    print("lol")

if __name__ == "__main__":
    main()