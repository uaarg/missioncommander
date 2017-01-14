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
    
    def __init__(self, name, index, duration, nav_pattern, waypoints):
        assert isinstance(nav_pattern, NavPattern)
        
        self.name = name
        self.index = index
        self.duration = duration
        self._nav_pattern = nav_pattern
        self.waypoints = waypoints
        
    def get_nav_pattern(self):
        return self._nav_pattern
    
    def set_nav_pattern(self, nav_pattern):
        assert isinstance(nav_pattern, NavPattern)
        self._nav_pattern = nav_pattern;
    
    nav_pattern = property(get_nav_pattern, set_nav_pattern)
    
a = Mission("name", 1, -1, NavPattern.MISSION_GOTO_WP, [1, 2])

a.nav_pattern = NavPattern.MISSION_GOTO_WP_LLA
print(a.nav_pattern)
