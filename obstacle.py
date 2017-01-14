class Obstacle:
    """
    An obstacle to be avoided by the UAV.

    Attributes:
        moving: If true, the obstacle is moving. Otherwise, it is stationary.
        shape: The shape of the obstacle. This can be one of the following values:
            * 'cylinder'
            * 'sphere' 
        geom_data: A dictionary containing geometric information about
        the obstacle. The contents of the dictionary will vary depending
        on the value of the shape attribute.
            * radius: The radius of the object in metres.
            * height: The height of the object in metres.
            * altitude: The MSL altitude of the object in metres.
        lat: The latitude of the obstacle centre in decimal degrees.
        lon: The longitude of the obstacle centre in decimal degrees.
    """

    def _populateGeomData(shape):
        """
        Given a shape, returns a dictionary of the appropriate geometric
        data for the shape.
        """
        if shape == 'cylinder':
            geom_data = {'radius': None, 'height': None}
        if shape == 'sphere':
            geom_data = {'radius': None, 'altitude', None}

        return geom_data

    def _feetToM(length):
        return length * 0.3048

    def __init__(self, moving, shape, lat, lon):
        """
        Obstacle constructor from properties.
        """
        self.moving = moving
        self.lat = lat
        self.lon = lon
        self.shape = shape
        self.geom_data = _populateGeomData(self.shape)

    def __init__(self, obstacle):
        """
        Obstacle constructor from an instance of one of the obstacle
        types from the interoperability client library.

        Args:
            obstacle: An instance of interop_types.StationaryObstacle 
            or interop_types.MovingObstacle.
        """
        self.lat = obstacle.latitude
        self.lon = obstacle.longitude

        if type(obstacle) == 'StationaryObstacle':
            self.moving = False
            self.shape = 'cylinder'
            self.geom_data = _populateGeomData(self.shape)
            self.geom_data['radius'] = _feetToM(obstacle.cylinder_radius)
            self.geom_data['height'] = _feetToM(obstacle.cylinder_height)

        if type(obstacle) == 'MovingObstacle':
            self.moving = True
            self.shape = 'sphere'
            self.geom_data = _populateGeomData(self.shape)
            self.geom_data['radius'] = _feetToM(obstacle.sphere_radius)
            self.geom_data['altitude'] = _feetToM(obstacle.altitude_msl)