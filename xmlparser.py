from config import *

import xml.etree.ElementTree as ET
import utm
import waypointobject
import mission

class importxml(object):
    def __init__(self, filepath, datDatabase):

        self.db = datDatabase
        self.parseXML(filepath)

    def parseXML(self, filepath):
        wpID = 0
        tree = ET.parse(filepath)
        self.root = tree.getroot()

        flightParams = {}
        fancy = None
        for e in self.root.iter('flight_plan'):
            fancy = e.items()
        if fancy is not None:
            flightParams = self.__floatize(dict(fancy))

            utmHome = utm.from_latlon(flightParams['lat0'], flightParams['lon0'])

            flightParams['easting0'] = utmHome[0]
            flightParams['northing0'] = utmHome[1]
            flightParams['utmZoneNumber0'] = utmHome[2]
            flightParams['utmZoneLetter0'] = utmHome[3]

            originWpObj = waypointobject.Waypoint('OrIgIn', '0','utm',flightParams['lat0'], flightParams['lon0'], flightParams['utmZoneNumber0'], True, flightParams['easting0'], flightParams['northing0'], flightParams['alt'])
            self.db.addWaypoint(originWpObj)


            waypoints = []
            for wpt in self.root.iter('waypoint'):
                waypoints.append(self.__floatize(dict(wpt.items())))

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
                    waypoint['alt'] = flightParams['alt']

                if wpTypeXY: # Convert to UTM
                    waypoint['easting'] = flightParams['easting0'] + float(waypoint['x'])
                    waypoint['northing'] = flightParams['northing0'] + float(waypoint['y'])
                    waypoint['zone'] = flightParams['utmZoneNumber0']
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
                self.db.addWaypoint(wpobj)
        else:

            missions = []

            for missionType in ('go', 'path', 'circle', 'segment', 'survey'):
                missions = missions + self.__getListofDictOfXMLtag(missionType)
            index = 1
            for miss in missions: # Add mID's
                miss['mID'] = index
                index = index + 1

            for miss in missions:
                if 'wp' in miss.keys():
                    pass
                elif 'wpts' in miss.keys():
                    miss['wp'] = miss['wpts'].replace(',','').split()
                    #print(miss['wpts'])
                else:
                    raise AttributeError ('Mission ID:' + miss['mID']+ ' does not contain waypoints. ;(')

                if not('radius' in miss.keys()):
                    miss['radius'] = None

                missionObj = mission.Mission(miss['mID'], -1, mission.NavPattern(miss['NavPattern']), miss['wp'], miss['radius'])
                self.db.addMission([(missionObj.name , missionObj)])

            tasks = []
            index2 = 0
            tasks = self.__getListofDictOfXMLtag('task')
            for task in tasks:
                if not('name' in task.keys()):
                    pass
                else:
                    task['mID'] = str(task['mID']).replace(',','').split()
                    task['tID'] = index2
                    index2 = index2 + 1
                    taskObj = mission.task(task['name'], task['mID'])

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
