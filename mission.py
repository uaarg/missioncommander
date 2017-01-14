from enum import Enum
from waypointobject import Waypoint
from config import *

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
    
    def __init__(self, name, index, duration, nav_pattern, waypoints, radius = None):
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
    
    def set_nav_pattern(self, nav_pattern, radius = None):
        assert isinstance(nav_pattern, NavPattern)
        print("setting nav pattern")
        self._nav_pattern = nav_pattern
    
    nav_pattern = property(get_nav_pattern, set_nav_pattern)
    
    def gen_mission_msg(self, ac_id, insert_mode = InsertMode.Append):
        assert isinstance(insert_mode, InsertMode)
        msg = pprzmsg("datalink", self._nav_pattern.name)

        msg['ac_id'] = ac_id
        msg['insert'] = insert_mode.name
        msg['duration'] = self.duration
        msg['index'] = self.index
        
        if self._nav_pattern == NavPattern.MISSION_GOTO_WP:
            assert len(self.waypoints) == 1
            waypoint = self.waypoints[0].get_utm()
            msg['wp_east'] = waypoint['east']
            msg['wp_north'] = waypoint['north']
            msg['wp_alt'] = waypoint['alt']

        if self._nav_pattern == NavPattern.MISSION_GOTO_WP_LLA:
            assert len(self.waypoints) == 1
            waypoint = self.waypoints[0].get_latlon()
            msg['wp_lat'] = waypoint['lat']
            msg['wp_lon'] = waypoint['lon']
            msg['wp_alt'] = waypoint['alt']
        
        elif self._nav_pattern == NavPattern.MISSION_CIRCLE:
            assert len(self.waypoints) == 1
            if not self.radius: 
                raise AttributeError("Circle requires radius")
            waypoint = self.waypoints[0].get_utm()

            msg['center_east'] = waypoint['east']
            msg['center_north'] = waypoint['north']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE_LLA:
            assert len(self.waypoints) == 1
            if not self.radius: 
                raise AttributeError("Circle requires radius")
            waypoint = self.waypoints[0].get_latlon()

            msg['center_lat'] = waypoint['lat']
            msg['center_lon'] = waypoint['lon']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius
            
        elif self._nav_pattern == NavPattern.MISSION_SEGMENT:
            assert len(self.waypoints) == 2
            waypoint1 = self.waypoints[0].get_utm()
            waypoint2 = self.waypoints[1].get_utm()
            msg['segment_east_1'] = waypoint1['east']
            msg['segment_north_1'] = waypoint1['north']
            msg['segment_east_2'] = waypoint2['east']
            msg['segment_north_2'] = waypoint2['north']
            
        elif self._nav_pattern == NavPattern.MISSION_SEGMENT_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = self.waypoints[0].get_latlon()
            waypoint2 = self.waypoints[1].get_latlon()
            msg['segment_lat_1'] = waypoint1['lat']
            msg['segment_lon_1'] = waypoint1['lon']
            msg['segment_lat_2'] = waypoint2['lat']
            msg['segment_lon_2'] = waypoint2['lon']

        elif self._nav_pattern == NavPattern.MISSION_PATH:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0, waypoints_num):
                waypoint = self.waypoints[i].get_utm()
                msg['point_east_' + str(i + 1)] = waypoint['east']
                msg['point_north_' + str(i + 1)] = waypoint['north']
            msg['path_alt'] = self.waypoints[0].get_utm()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_PATH_LLA:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0,waypoints_num):
                waypoint = self.waypoints[i].get_latlon()
                msg['point_lat_' + str(i + 1)] = waypoint['lat']
                msg['point_lon_' + str(i + 1)] = waypoint['lon']
            msg['path_alt'] = self.waypoints[0].get_latlon()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_SURVEY:
            assert len(self.waypoints) == 2
            waypoint1 = self.waypoints[0].get_utm()
            waypoint2 = self.waypoints[1].get_utm()
            msg['survey_east_1'] = waypoint1['east']
            msg['survey_north_1'] = waypoint1['north']
            msg['survey_east_2'] = waypoint2['east']
            msg['survey_north_2'] = waypoint2['north']
            msg['survey_alt'] = waypoint1['alt']

        elif self._nav_pattern == NavPattern.MISSION_SURVEY_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = self.waypoints[0].get_latlon()
            waypoint2 = self.waypoints[1].get_latlon()
            msg['survey_lat_1'] = waypoint1['lat']
            msg['survey_lon_1'] = waypoint1['lon']
            msg['survey_lat_2'] = waypoint2['lat']
            msg['survey_lon_2'] = waypoint2['lon']
            msg['survey_alt'] = waypoint1['alt']
        
        return msg
        
