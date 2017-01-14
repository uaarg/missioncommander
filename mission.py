from enum import Enum

class InsertMode(Enum):
    Append = 1
    Prepend = 2
    ReplaceCurrent = 3
    ReplaceAll = 4

class NavPattern(Enum):
    MISSION_GOTO_WP = 1
    MISSION_GOTO_WP_LLA = 2
    MISSION_CIRCLE = 3
    MISSION_CIRCLE_LLA = 4
    MISSION_SEGMENT = 5
    MISSION_SEGMENT_LLA = 6
    MISSION_PATH = 7
    MISSION_PATH_LLA = 8
    MISSION_SURVEY = 9
    MISSION_SURVEY_LLA = 10

class Mission:
    """class to define missions applying to 1 or more waypoints"""
    
    def __init__(self, name, index, duration, nav_pattern, waypoints, radius=None):
        assert isinstance(nav_pattern, NavPattern)
        assert nav_pattern != NavPattern.MISSION_CIRCLE and nav_pattern != NavPattern.MISSION_CIRCLE_LLA or radius is not None
        
        self.name = name
        self.index = index
        self.duration = duration
        self._nav_pattern = nav_pattern
        self.waypoints = waypoints
        self.radius = radius
        
    def get_nav_pattern(self):
        return self._nav_pattern
    
    def set_nav_pattern(self, nav_pattern):
        assert isinstance(nav_pattern, NavPattern)
        self._nav_pattern = nav_pattern;
    
    nav_pattern = property(get_nav_pattern, set_nav_pattern)
    
    def gen_mission_msg(self, ac_id, insert_mode = InsertMode.Append):
        msg = pprzmsg("datalink", self._nav_pattern.name)

        msg['ac_id'] = ac_id
        msg['insert'] = insert_mode
        msg['duration'] = self.duration

        if self._nav_pattern == NavPattern.MISSION_GOTO_WP_LLA:
            assert len(self.waypoints) == 1
            waypoint = self.waypoints[0].get_latlon;
            msg['wp_lat'] = waypoint['lat']
            msg['wp_lon'] = waypoint['lon']
            msg['wp_alt'] = waypoint['alt']

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE_LLA:
            assert len(self.waypoints) == 1
            waypoint = self.waypoints[0].get_latlon;

            msg['center_lat'] = waypoint['lat']
            msg['center_lon'] = waypoint['lon']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius
            
        elif msg_id == 'MISSION_SEGMENT_LLA':
            assert len(self.waypoints) == 2
            waypoint1 = self.waypoints[0].get_latlon
            waypoint2 = self.waypoints[1].get_latlon
            msg['segment_lat_1'] = waypoint1['lat']
            msg['segment_lon_1'] = waypoint1['lon']
            msg['segment_lat_2'] = waypoint2['lat']
            msg['segment_lon_2'] = waypoint2['lon']

        #elif msg_id == 'MISSION_PATH_LLA':
        #    msg['point_lat_1'] = msgs.get('point_lat_1')
        #    msg['point_lon_1'] = msgs.get('point_lon_1')
        #    msg['point_lat_2'] = msgs.get('point_lat_2')
        #    msg['point_lon_2'] = msgs.get('point_lon_2')
        #    msg['point_lat_3'] = msgs.get('point_lat_3')
        #    msg['point_lon_3'] = msgs.get('point_lon_3')
        #    msg['point_lat_4'] = msgs.get('point_lat_4')
        #    msg['point_lon_4'] = msgs.get('point_lon_4')
        #    msg['point_lat_5'] = msgs.get('point_lat_5')
        #    msg['point_lon_5'] = msgs.get('point_lon_5')
        #    msg['path_alt'] = msgs.get('path_alt')
        #    msg['nb'] = msgs.get('nb')

        #elif msg_id == 'MISSION_SURVEY_LLA':
        #    msg['survey_lat_1'] = msgs.get('survey_lat_1')
        #    msg['survey_lon_1'] = msgs.get('survey_lon_1')
        #    msg['survey_lat_2'] = msgs.get('survey_lat_2')
        #    msg['survey_lon_2'] = msgs.get('survey_lon_2')
        #    msg['survey_alt'] = msgs.get('survey_alt')
        
        return msg
    
a = Mission("name", 1, -1, NavPattern.MISSION_GOTO_WP, [1, 2])

a.nav_pattern = NavPattern.MISSION_GOTO_WP_LLA
print(a.nav_pattern)
