import xml.etree.ElementTree as ET
import utm
from datetime import datetime

from config import *
import waypointobject
import mission

class importXML(object):
    def __init__(self):
        '''
        CALL bindDBandFilepath BEFORE USING
        '''
        self.do = 'Nothing'

    def bindDBandFilepath(self, fP, datDatabase):
        self.filepath = fP
        self.db = datDatabase

    def parseXML(self):
        '''
        Parses the XML file at 'filepath' to add its waypoints,
        missions and tasks to a 'Bag of Holding'
        '''

        if (self.filepath or self.db) is None:
            raise AttributeError('Tried to export without binding database and filepath. :| ')

        wpID = 0
        waypoints = []
        missions = []
        tasks = []

        tree = ET.parse(self.filepath)
        self.root = tree.getroot()


        fancy = None
        for e in self.root.iter('flight_plan'):
            fancy = e.items()

        if fancy is not None: # Checking if this file has flight parameters
            self.flightParams = self.__floatize(dict(fancy))

            utmHome = utm.from_latlon(self.flightParams['lat0'], self.flightParams['lon0'])

            self.flightParams['easting0'] = float(utmHome[0])
            self.flightParams['northing0'] = float(utmHome[1])
            self.flightParams['utmZoneNumber0'] = utmHome[2]
            self.flightParams['utmZoneLetter0'] = utmHome[3]

            waypointobject.Waypoint.flightParams = self.flightParams
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
                    if 'alt' in str(key):
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

            for miss in missions:
                if 'mID' in miss.keys(): # Only use it if it already has a mission ID
                    if 'wp' in miss.keys():
                        miss['wp'] = miss['wp'].split()
                    elif 'wpts' in miss.keys():
                        miss['wp'] = miss['wpts'].replace(',','').split()
                    else:
                        raise AttributeError ('Mission ID:' + miss['mID']+ ' does not contain waypoints. ;(')

                    if not('radius' in miss.keys()):
                        miss['radius'] = None

                    missionObj = mission.Mission(int(miss['mID']), -1, mission.NavPattern(miss['NavPattern'] +'_lla'), miss['wp'], miss['radius'])
                    self.db.addMission([(missionObj.name , missionObj)])

        taskIndex= -1
        tasks = self.__getListofDictOfXMLtag('task')

        if tasks is not None:
            for task in tasks:
                taskIndex = taskIndex + 1
                if not('name' in task.keys()):
                    pass
                else:
                    task['mID'] = str(task['mID']).replace(',','').split()
                    task['tID'] = taskIndex
                    taskObj = mission.task(task['tID'], task['name'], task['mID'])
                    self.db.addTask([(task['name'],taskObj)])

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

    def __init__(self):
        '''
        CALL bindDBandFilepath BEFORE USING
        '''
        self.do = 'Nothing'

    def bindDBandFilepath(self, fP, datDatabase):
        self.filepath = fP
        self.db = datDatabase

    def writeXML(self):
        '''
        Writes the current Waypoints, Missions and Tasks to an xml file
        at the designated filepath.
        NOTE the file made here cannot be used by paparazzi, users must
        paste the flight plan parameters and waypoints to the flight plan
        used by paparazzi.
        '''
        if (self.filepath or self.db) is None:
            raise AttributeError('Tried to export without binding database and filepath. :| ')

        gParentElement = ET.Element('MissionCommanderFlightStuff')

        waypoints = ET.SubElement(gParentElement, 'waypoints')
        for waypoint in self.db.waypoints.values():
            wpt = ET.SubElement(waypoints, 'waypoint')
            wpt.set('name', waypoint.name)
            wpt.set('lat', str(waypoint.get_latlon()['lat']))
            wpt.set('lon', str(waypoint.get_latlon()['lon']))
            if waypoint.alt is not None:
                wpt.set('alt', str(waypoint.alt))
            else:
                pass

        missions = ET.SubElement(gParentElement, 'missions')
        for missObj in self.db.allMissions.values():
            miss = ET.SubElement(missions, str(missObj._nav_pattern.value))
            miss.set('mID', str(missObj.index))

            waypts = self.listToStringList(missObj.waypoints)
            if ',' in waypts:
                miss.set('wpts', waypts)
            else:
                miss.set('wp', waypts)

            if missObj._nav_pattern.value is 'circle':
                miss.set('radius', str(missObj.radius))

        tasks = ET.SubElement(gParentElement, 'tasks')

        for taskObj in self.db.tasks.values():
            tsk = ET.SubElement(tasks, 'task')
            tsk.set('name', str(taskObj.name))
            allMiss = self.listToStringList(taskObj.missions)
            tsk.set('mID', allMiss)

        self.indent(gParentElement)

        outgoingTree = ET.ElementTree(gParentElement)
        fileName = self.filepath + str(datetime.now()) + '_WptsMissTsks.xml'
        outgoingTree.write(fileName, xml_declaration = True, encoding='utf-8', method="xml")

    def listToStringList(self, thingToConvert):
        '''
        Converts a list of waypoints (or mission ID's) to a single string to be put into an xml.
        '''
        if type(thingToConvert) is str:
            return thingToConvert
        else:
            string = ''
            for thing in thingToConvert:
                string = string + thing + ', '
            string = string[:(len(string)-2)] # Remove last ', '
            return string

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

global importxml
importxml = importXML()

global exportxml
exportxml = exportToXML()
