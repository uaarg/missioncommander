

class airplaneTelemetry(object):
    '''
    Stores the airplane's position, altitude and current heading.
    This is meant to be updated from the Ivybus and updating the Interop Server
    when any value is updated.
    We need to submit at a minimum of 1 Hz to the server to recieve points
    '''

    def __init__(self, position = (0,0), alt_msl = 0, heading = 0 ):
        # Can construct without any telemetry data
        self.position = position # Tuple of lat-lon
        self.altitude = alt_msl
        self.heading = heading
        self.positionFlag = False
        self.altitideFlag = False
        self.headingFlag = False

    # Updates each variable
    def newPosition(self, newPos):
        if (self.position != newPos):
            self.position = newPos
            self.positionFlag = True
            return True
        else:
            return False

    def newAltitude(self, newAlt):
        if (self.altitude != newAlt):
            self.altitude = newAlt
            self.altitideFlag = True
            return True
        else:
            return False

    def newheading(self, newHead):
        if (self.heading != newHead):
            self.heading = newHead
            self.headingFlag = True
            return True
        else:
            return False

    # Interop server code will call this when new data is recieved
    def sendTelemetry(self):
        if (self.positionFlag | self.altitideFlag | self.headingFlag):
            self.positionFlag = self.altitideFlag = self.headingFlag = False
            tele = {'latitude':float(position(0)), 'longitude':float(position(1)), 'altitude_msl':float(altitude), 'uas_heading':float(heading0}
            return tele
        else:
            return False
