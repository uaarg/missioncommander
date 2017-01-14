

class airplaneTelemetry():
    def __init__(self, position = (0,0), alt_msl = 0, speed = -1 ):
        self.position = position
        self.altitude = alt_msl
        self.speed = speed

    def newPosition(newPos):
        if (self.position != newPos):
            self.position = newPos
            # UPDATE INTEROP SERVER
        else:
