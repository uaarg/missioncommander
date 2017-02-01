from enum import Enum
from waypointobject import Waypoint
from config import *

class InsertMode(Enum):
    Append = 1
    Prepend = 2
    ReplaceCurrent = 3
    ReplaceAll = 4

class NavPattern(Enum):
    MISSION_GOTO_WP = 'go'
    MISSION_GOTO_WP_LLA = 'go_lla'
    MISSION_CIRCLE = 'circle'
    MISSION_CIRCLE_LLA = 'circle_lla'
    MISSION_SEGMENT = 'segment'
    MISSION_SEGMENT_LLA = 'segment_lla'
    MISSION_PATH = 'path'
    MISSION_PATH_LLA = 'path_lla'
    MISSION_SURVEY = 'survey'
    MISSION_SURVEY_LLA = 'survey_lla'


class Mission(object):
    """class to define missions applying to 1 or more waypoints"""

    def genName(self):
        '''
        Generate useable name for mission if one is not pre-made.
        Uses waypoints involved and the nav_pattern.
        '''

        nameStr = ''

        if (self.nav_pattern.name is 'MISSION_GOTO_WP'):
            nameStr = nameStr + 'Go to waypoint '
        elif (self.nav_pattern.name is 'MISSION_CIRCLE'):
            nameStr = nameStr + 'Circle waypoint '
        elif (self.nav_pattern.name is 'MISSION_PATH'):
            nameStr = nameStr + 'Make a path from '
        elif (self.nav_pattern.name is 'MISSION_SEGMENT'):
            nameStr = nameStr + 'Make a path between '
        elif (self.nav_pattern.name is 'MISSION_SURVEY'):
            nameStr = nameStr + 'Survey from waypoint '

        oneWaypoit = True

        if type(self.waypoints) is str: # if we only have 1 waypoint to deal with
            nameStr = nameStr + self.waypoints
        else:
            for wp in self.waypoints:
                if not(oneWaypoit):
                    nameStr = nameStr + ' to ' + wp
                else:
                    nameStr = nameStr + wp
                    oneWaypoit = False

        return nameStr


    def __init__(self, index, duration, nav_pattern, waypoints, radius = None, name = None):
        assert isinstance(nav_pattern, NavPattern)
        assert nav_pattern != NavPattern.MISSION_CIRCLE and nav_pattern != NavPattern.MISSION_CIRCLE_LLA or radius is not None


        self.index = index
        self.duration = duration
        self._nav_pattern = nav_pattern
        self.waypoints = waypoints
        self.radius = radius
        self.wpUpdated = False

        if name is None:
            self.name = self.genName()
        else:
            self.name = name

    def get_nav_pattern(self):
        return self._nav_pattern

    def set_nav_pattern(self, nav_pattern, radius = None):
        assert isinstance(nav_pattern, NavPattern)
        self._nav_pattern = nav_pattern

    #Causes mission.nav_pattern to call setter or getter
    nav_pattern = property(get_nav_pattern, set_nav_pattern)

    def gen_mission_msg(self, ac_id, wpList, insert_mode = InsertMode.Append):



        assert isinstance(insert_mode, InsertMode)
        msg = pprzmsg("datalink", self._nav_pattern.name)

        msg['ac_id'] = ac_id
        msg['insert'] = insert_mode.name
        msg['duration'] = self.duration
        msg['index'] = self.index

        if self._nav_pattern == NavPattern.MISSION_GOTO_WP:
            assert len(self.waypoints) == 1
            waypoint = wpList[self.waypoints[0]].get_utm()
            msg['wp_east'] = waypoint['east']
            msg['wp_north'] = waypoint['north']
            msg['wp_alt'] = waypoint['alt']

        elif self._nav_pattern == NavPattern.MISSION_GOTO_WP_LLA:
            assert len(self.waypoints) == 1
            waypoint = wpList[self.waypoints[0]].get_latlon()
            msg['wp_lat'] = waypoint['lat']
            msg['wp_lon'] = waypoint['lon']
            msg['wp_alt'] = waypoint['alt']

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE:
            assert len(self.waypoints) == 1
            if not self.radius:
                raise AttributeError("Circle requires radius")
            waypoint = wpList[self.waypoints[0]].get_utm()

            msg['center_east'] = waypoint['east']
            msg['center_north'] = waypoint['north']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE_LLA:
            assert len(self.waypoints) == 1
            if not self.radius:
                raise AttributeError("Circle requires radius")
            waypoint = wpList[self.waypoints[0]].get_latlon()

            msg['center_lat'] = waypoint['lat']
            msg['center_lon'] = waypoint['lon']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius

        elif self._nav_pattern == NavPattern.MISSION_SEGMENT:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[self.waypoints[0]].get_utm()
            waypoint2 = wpList[self.waypoints[1]].get_utm()
            msg['segment_east_1'] = waypoint1['east']
            msg['segment_north_1'] = waypoint1['north']
            msg['segment_east_2'] = waypoint2['east']
            msg['segment_north_2'] = waypoint2['north']

        elif self._nav_pattern == NavPattern.MISSION_SEGMENT_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[self.waypoints[0]].get_latlon()
            waypoint2 = wpList[self.waypoints[1]].get_latlon()
            msg['segment_lat_1'] = waypoint1['lat']
            msg['segment_lon_1'] = waypoint1['lon']
            msg['segment_lat_2'] = waypoint2['lat']
            msg['segment_lon_2'] = waypoint2['lon']

        elif self._nav_pattern == NavPattern.MISSION_PATH:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0, waypoints_num):
                waypoint = wpList[self.waypoints[i]].get_utm()
                msg['point_east_' + str(i + 1)] = waypoint['east']
                msg['point_north_' + str(i + 1)] = waypoint['north']
            msg['path_alt'] = wpList[self.waypoints[0]].get_utm()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_PATH_LLA:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0,waypoints_num):
                waypoint = wpList[self.waypoints[i]].get_latlon()
                msg['point_lat_' + str(i + 1)] = waypoint['lat']
                msg['point_lon_' + str(i + 1)] = waypoint['lon']
            msg['path_alt'] = wpList[self.waypoints[0]].get_utm()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_SURVEY:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[self.waypoints[0]].get_utm()
            waypoint2 = wpList[self.waypoints[1]].get_utm()
            msg['survey_east_1'] = waypoint1['east']
            msg['survey_north_1'] = waypoint1['north']
            msg['survey_east_2'] = waypoint2['east']
            msg['survey_north_2'] = waypoint2['north']
            msg['survey_alt'] = waypoint1['alt']

        elif self._nav_pattern == NavPattern.MISSION_SURVEY_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[self.waypoints[0]].get_latlon()
            waypoint2 = wpList[self.waypoints[1]].get_latlon()
            msg['survey_lat_1'] = waypoint1['lat']
            msg['survey_lon_1'] = waypoint1['lon']
            msg['survey_lat_2'] = waypoint2['lat']
            msg['survey_lon_2'] = waypoint2['lon']
            msg['survey_alt'] = waypoint1['alt']

        return msg

    def flagForUpdate(self):
        self.wpUpdated = True

class task(object):
    '''
    Collection of missions used to complete mission objectives
    (eg. surveying a search area, completing autonamous waypoint navigation)
    '''

    def __init__(self, name, missions):
        self.name = name
        self.missions = missions
