import utm

class Waypoint(object):
    """
    This object may take either latlon or UTM format as input; however, it stores them in UTM.
    """

    def __init__(self, name, wpID, point_type, lat=None, lon=None, zone=None, northern=True, east=None, north=None, alt=None, missions=[]):

        """
        ARGUMENTS
        name: the name of the waypoint
        point_type: the type of the waypoint. Valid values are "latlon" or "utm".

        KEYWORDS
        lat: the latitude. Mandatory if point_type is "latlon".
        lon: the longitude. Mandatory if point_type is "latlon".
        zone: the UTM zone number. Mandatory if point_type is "utm".
        northern: whether the waypoint is in the north or south. Defaults to true. Mandatory if point_type is "utm".
        east: east measurement of UTM coordinate. Mandatory if point_type is "utm".
        north: north measurement of UTM coordinate. Mandatory if point_type is "utm".
        alt: altitude. Optional.
        """
        if point_type == 'latlon':
            if not (lat and lon):
                raise AttributeError("Waypoint initialization failed: latitide and/or longitude not given")
            else:
                (self.east, self.north, self.zone, placeholder) = utm.from_latlon(lat, lon)
        elif point_type == 'utm':
            if not (zone and east and north):
                raise AttributeError("Waypoint initialization failed: one or more UTM parameters not given")
            else:
                self.zone = zone
                self.east = east
                self.north = north
        else:
            raise AttributeError("Waypoint initialization failed: invalid waypoint type given")
        self.alt = alt
        self.name = name
        try:
            self.wpID = wpID
        except:
            raise AttributeError(" Waypoint" + self.name + " requires a waypoint ID")
        self.northern = northern

        self.missions = missions


    def update_latlon(self, lat, lon, name=None, alt=None):
        """
        Used to update the waypoint using latitude and longitude.
        """
        (self.east, self.north, self.zone, placeholder) = utm.from_latlon(lat, lon)
        if alt:
            self.alt = alt
        if name:
            self.name = name


    def update_utm(self, east, north, zone, northern=True, alt=None, name=None):
        """
        Used to update the waypoint using UTM coordinates.
        """
        self.east = east
        self.north = north
        self.zone = zone
        self.northern = northern
        if alt:
            self.alt = alt
        if name:
            self.name = name

        self.flagMissions()


    def get_latlon(self):
        """
        Returns a dictionary containing waypoint data in latlon format.
        """
        result = {}
        result['name'] = self.name
        result['alt'] = self.alt
        (result['lat'], result['lon']) = utm.to_latlon(self.east, self.north, self.zone, northern=self.northern)
        return result


    def get_utm(self):
        """
        Returns a dictionary containing waypoint data in UTM format.
        """
        result = {}
        result['name'] = self.name
        result['alt'] = self.alt
        result['zone'] = self.zone
        result['northern'] = self.northern
        result['east'] = self.east
        result['north'] = self.north
        return result

    def gen_move_waypoint_msg(self, ac_id):
        """
        Returns an Ivy bus message for moving the waypoint.
        """
        msg = pprzmsg("datalink", "MOVE_WP")
        msg['wp_id'] = self.wpID
        msg['ac_id'] = ac_id
        latlon = self.get_latlon()
        msg['lat'] = latlon['lat']
        msg['lon'] = latlon['lon']
        msg['alt'] = latlon['alt']
        return msg

    def addMission(self, mission):
        missions.append(mission)

    def removeMission(self, mission):
        missions.remove(mission)

    def flagMissions(self):
        for m in self.missions:
            m.flagForUpdate()
