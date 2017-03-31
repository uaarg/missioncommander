from enum import Enum
from waypointobject import Waypoint
from config import *

class InsertMode(Enum):
    Append = 0
    Prepend = 1
    ReplaceCurrent = 2
    ReplaceAll = 3
    ReplaceIndex = 4

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

        if ('MISSION_GOTO_WP'  in self.nav_pattern.name):
            nameStr = nameStr + 'Go to waypoint '
        elif ('MISSION_CIRCLE' in self.nav_pattern.name):
            nameStr = nameStr + 'Circle waypoint '
        elif ('MISSION_PATH'   in self.nav_pattern.name):
            nameStr = nameStr + 'Make a path from '
        elif ('MISSION_SEGMENT'in self.nav_pattern.name):
            nameStr = nameStr + 'Make a path between '
        elif ('MISSION_SURVEY' in self.nav_pattern.name):
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

    def gen_mission_msg(self, ac_id, db, insert_mode = InsertMode.Append, task_id = 0, insert_index = 1):

        assert isinstance(insert_mode, InsertMode)
        msg = pprzmsg("datalink", self._nav_pattern.name)

        msg['ac_id'] = ac_id
        msg['insert'] = insert_mode.value
        msg['duration'] = self.duration #if duration is -1 mission completes
        msg['index'] = int(self.index)
        msg['insert_index'] = insert_index
        msg['task'] = task_id

        wpList = []
        for wpIndex in range(0,len(self.waypoints)):
            wpList.append(db.waypoints[str(self.waypoints[wpIndex])])


        if self._nav_pattern == NavPattern.MISSION_GOTO_WP:
            assert len(self.waypoints) == 1
            waypoint = wpList[0].get_xy()
            msg['wp_east'] = waypoint['x']
            msg['wp_north'] = waypoint['y']
            msg['wp_alt'] = waypoint['alt']

        elif self._nav_pattern == NavPattern.MISSION_GOTO_WP_LLA:
            assert len(self.waypoints) == 1
            waypoint = wpList[0].get_fancyLatLon()
            msg['wp_lat'] = waypoint['lat']
            msg['wp_lon'] = waypoint['lon']
            msg['wp_alt'] = waypoint['alt']

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE:
            assert len(self.waypoints) == 1
            if not self.radius:
                raise AttributeError("Circle requires radius")
            waypoint = wpList[0].get_xy()

            msg['center_east'] = waypoint['x']
            msg['center_north'] = waypoint['y']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius

        elif self._nav_pattern == NavPattern.MISSION_CIRCLE_LLA:
            assert len(self.waypoints) == 1
            if not self.radius:
                raise AttributeError("Circle requires radius")
            waypoint = wpList[0].get_fancyLatLon()

            msg['center_lat'] = waypoint['lat']
            msg['center_lon'] = waypoint['lon']
            msg['center_alt'] = waypoint['alt']
            msg['radius'] = self.radius

        elif self._nav_pattern == NavPattern.MISSION_SEGMENT:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[0].get_xy()
            waypoint2 = wpList[1].get_xy()
            msg['segment_east_1'] = waypoint1['x']
            msg['segment_north_1'] = waypoint1['y']
            msg['segment_east_2'] = waypoint2['x']
            msg['segment_north_2'] = waypoint2['y']

        elif self._nav_pattern == NavPattern.MISSION_SEGMENT_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[0].get_fancyLatLon()
            waypoint2 = wpList[1].get_fancyLatLon()
            msg['segment_lat_1'] = waypoint1['lat']
            msg['segment_lon_1'] = waypoint1['lon']
            msg['segment_lat_2'] = waypoint2['lat']
            msg['segment_lon_2'] = waypoint2['lon']

        elif self._nav_pattern == NavPattern.MISSION_PATH:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0, waypoints_num):
                waypoint = wpList[i].get_xy()
                msg['point_east_' + str(i + 1)] = waypoint['x']
                msg['point_north_' + str(i + 1)] = waypoint['y']
            msg['path_alt'] = wpList[0].get_xy()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_PATH_LLA:
            waypoints_num = len(self.waypoints)
            assert waypoints_num >= 2 and waypoints_num <= 5
            for i in range(0,waypoints_num):
                waypoint = wpList[i].get_fancyLatLon()
                msg['point_lat_' + str(i + 1)] = waypoint['lat']
                msg['point_lon_' + str(i + 1)] = waypoint['lon']

            msg['path_alt'] = wpList[0].get_xy()['alt']
            msg['nb'] = waypoints_num

        elif self._nav_pattern == NavPattern.MISSION_SURVEY:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[0].get_xy()
            waypoint2 = wpList[1].get_xy()
            msg['survey_east_1'] = waypoint1['x']
            msg['survey_north_1'] = waypoint1['y']
            msg['survey_east_2'] = waypoint2['x']
            msg['survey_north_2'] = waypoint2['y']
            msg['survey_alt'] = waypoint1['alt']

        elif self._nav_pattern == NavPattern.MISSION_SURVEY_LLA:
            assert len(self.waypoints) == 2
            waypoint1 = wpList[0].get_fancyLatLon()
            waypoint2 = wpList[1].get_fancyLatLon()
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

    def __init__(self, id, name, missions):
        self.id = id
        self.name = name
        self.missions = missions
