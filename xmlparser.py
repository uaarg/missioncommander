import xml.etree.ElementTree as ET
import utm
from datetime import datetime

from config import *
import waypointobject
import mission


class importxml(object):
    def __init__(self, filepath, datDatabase):

        self.db = datDatabase
        self.parseXML(filepath)
        self.flightParams = {}
        self.root = None

    def parseXML(self, filepath):
        '''
        Parses the XML file at 'filepath' to add its waypoints,
        missions and tasks to a 'Bag of Holding'
        '''

        wpID = 0
        waypoints = []
        missions = []
        tasks = []

        tree = ET.parse(filepath)
        self.root = tree.getroot()


        fancy = None
        for e in self.root.iter('flight_plan'):
            fancy = e.items()

        if fancy is not None: # Checking if this file has flight parameters
            self.flightParams = self.__floatize(dict(fancy))

            utmHome = utm.from_latlon(self.flightParams['lat0'], self.flightParams['lon0'])

            self.flightParams['easting0'] = utmHome[0]
            self.flightParams['northing0'] = utmHome[1]
            self.flightParams['utmZoneNumber0'] = utmHome[2]
            self.flightParams['utmZoneLetter0'] = utmHome[3]

            originWpObj = waypointobject.Waypoint('OrIgIn', '0','utm',self.flightParams['lat0'], self.flightParams['lon0'], self.flightParams['utmZoneNumber0'], True, self.flightParams['easting0'], self.flightParams['northing0'], self.flightParams['alt'])
            self.db.addWaypoint([(originWpObj.name, originWpObj)])



            for wpt in self.root.iter('waypoint'):
                waypoints.append(self.__floatize(dict(wpt.items())))

        if waypoints is not None: # Checking if waypoits are present in this file

            for waypoint in waypoints:
                wpTypeXY = False
                wpTypeUTM = False
                wpTypeLatLon = False
                defaultAlt = True

                for key in waypoint:

                    if key is ('x' or 'y'):
                        wpTypeXY = True
                    if key is ('lat' or 'lon'):
                        wpTypeLatLon = True
                    if key is 'alt':
                        defaultAlt = False

                wpID = wpID + 1
                waypoint['wpID'] = int(wpID)
                if defaultAlt:
                    waypoint['alt'] = self.flightParams['alt']

                if wpTypeXY: # Convert to UTM
                    waypoint['easting'] = self.flightParams['easting0'] + float(waypoint['x'])
                    waypoint['northing'] = self.flightParams['northing0'] + float(waypoint['y'])
                    waypoint['zone'] = self.flightParams['utmZoneNumber0']
                    wpTypeXY = False
                    wpTypeUTM = True

                for requiredKey in ('lat', 'lon', 'zone', 'northHemi', 'easting', 'northing', 'alt'):
                    if not(requiredKey in waypoint):
                        waypoint[requiredKey] = 0

                waypoint['northHemi'] = True
                if wpTypeUTM:
                    waypoint['wpType'] = 'utm'
                else:
                    waypoint['wpType'] = 'latlon'

                wpobj = waypointobject.Waypoint(waypoint['name'], waypoint['wpID'], waypoint['wpType'], waypoint['lat'],waypoint['lon'],waypoint['zone'],waypoint['northHemi'],waypoint['easting'],waypoint['northing'],waypoint['alt'])
                self.db.addWaypoint([(wpobj.name, wpobj)])

        for missionType in ('go', 'path', 'circle', 'segment', 'survey'):
            missions = missions + self.__getListofDictOfXMLtag(missionType)

        if missions is not None:

            index = 1
            for miss in missions: # Add mID's
                miss['mID'] = index
                index = index + 1

            for miss in missions:
                if 'wp' in miss.keys():
                    miss['wp'] = miss['wp'].split()
                elif 'wpts' in miss.keys():
                    miss['wp'] = miss['wpts'].replace(',','').split()
                else:
                    raise AttributeError ('Mission ID:' + miss['mID']+ ' does not contain waypoints. ;(')

                if not('radius' in miss.keys()):
                    miss['radius'] = None

                missionObj = mission.Mission(miss['mID'], -1, mission.NavPattern(miss['NavPattern']), miss['wp'], miss['radius'])
                self.db.addMission([(missionObj.name , missionObj)])

        index2 = 0
        tasks = self.__getListofDictOfXMLtag('task')

        if tasks is not None:
            for task in tasks:
                if not('name' in task.keys()):
                    pass
                else:
                    task['mID'] = str(task['mID']).replace(',','').split()
                    task['tID'] = index2
                    index2 = index2 + 1
                    taskObj = mission.task(task['name'], task['mID'])
                    self.db.addTask(taskObj)

    def __floatize(self, dictionaryWithBadStrings):
        '''
        Makes dictionary entries floats if it can.
        '''
        goodDictionary = {}
        for key in dictionaryWithBadStrings:
            try:
                goodDictionary[key]= float(dictionaryWithBadStrings[key])
            except:
                goodDictionary[key] = dictionaryWithBadStrings[key]
        return goodDictionary

    def __getListofDictOfXMLtag(self, msg):
        '''
        Added this so I didnt have to write it 5 times.
        gets missions by mission type (circle, go, path ect.) and only imports
        ones with a mission id ['mID']
        '''
        detList = []
        for testMission in self.root.iter(msg):
            testMission = self.__floatize(dict(testMission.items()))
            if not(msg is "tasks"):
                testMission['NavPattern'] = msg
            detList.append(testMission)
        return detList

class exportToXML(object):

    def __init__(self, filepath, datDatabase):

        self.db = datDatabase
        self.writeXML(filepath)
        self.flightParams = {}
        self.root = None

    def writeXML(self, filepath):
        '''
        Writes the current Waypoints, Missions and Tasks to an xml file
        at the designated filepath.
        NOTE the file made here cannot be used by paparazzi, users must
        paste the flight plan parameters and waypoints to the flight plan
        used by paparazzi.
        '''

        gParentElement = ET.Element('MissionCommanderFlightStuff')

        waypoints = ET.SubElement(gParentElement, 'waypoints')
        for waypoint in self.db.waypoints.lst:
            wpt = ET.SubElement(waypoints, 'waypoint')
            wpt.set('name', waypoint.name)
            wpt.set('utm_x0', str(waypoint.east))
            wpt.set('utm_y0', str(waypoint.north))
            if waypoint.alt is not None:
                wpt.set('alt', str(waypoint.alt))
            else:
                pass

        missions = ET.SubElement(gParentElement, 'missions')
        for missObj in self.db.allMissions.values():
            miss = ET.SubElement(missions, str(missObj._nav_pattern.value))
            if type(missObj.waypoints) is str:
                miss.set('wp', missObj.waypoints)
            else:
                wptString = ''
                for wpt in missObj.waypoints:
                    wptString = wptString + wpt + ', '
                wptString = wptString[:(len(wptString)-2)] # Remove last ', '
                miss.set('wpts', str(wptString))
            if missObj._nav_pattern is 'circle':
                miss.set('radius', str(missObj.radius))

        tasks = ET.SubElement(gParentElement, 'tasks')
        for task in self.db.tasks.lst:
            tsk = ET.SubElement(tasks, 'task')
            tsk.set('name', str(task.name))
            tsk.set('mID', str(task.missions))

        self.indent(gParentElement)

        outgoingTree = ET.ElementTree(gParentElement)
        fileName = filepath + str(datetime.now()) + '_WptsMissTsks.xml'
        outgoingTree.write(fileName, xml_declaration = True, encoding='utf-8', method="xml")

    def indent(self, elem, level=0):
        '''
        Seb copied and pasted THIS function from https://norwied.wordpress.com/2013/08/27/307/
        Acessed on January 26th, 2017 because its a really badass piece of code.
        Element Tree should totally use it.
        copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
        it basically walks your tree and adds spaces and newlines so the tree is
        printed in a nice way
        '''
        i = '\n' + level*2*' ' # Had to add the *2 here since our xml levles are denoted by 2 spaces
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        for elem in elem:
            self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
