import xml.etree.ElementTree as ET
import utm
import waypointobject

class importxml(object):
    def __init__(self, filepath, datDatabase):
        # Add things if we need em
        self.db = datDatabase
        self.parseXML(filepath)

    def parseXML(self, filepath):
        wpID = 0
        tree = ET.parse(filepath)
        root = tree.getroot()

        flightParams = {}

        for e in root.iter('flight_plan'): # Only works on last msg with 'flight_plan'
            fancy = e.items()
        flightParams = self.floatize(dict(fancy))
        #print (flightParams)
        #print ('Home is at Lat:' + flightParams['lat0'] + 'deg Lon:' + flightParams['lon0'] + 'deg')

        utmHome = utm.from_latlon(flightParams['lat0'], flightParams['lon0'])
        #print(utmHome)
        flightParams['easting0'] = utmHome[0]
        flightParams['northing0'] = utmHome[1]
        flightParams['utmZoneNumber0'] = utmHome[2]
        flightParams['utmZoneLetter0'] = utmHome[3]
        #print(flightParams)
        originWpObj = waypointobject.Waypoint('OrIgIn', '0','utm',flightParams['lat0'], flightParams['lon0'], flightParams['utmZoneNumber0'], True, flightParams['easting0'], flightParams['northing0'], flightParams['alt'])
        self.db.addWaypoint(originWpObj)
        
        # Get waypoints from XML
        waypoints = []
        for wpt in root.iter('waypoint'):
            waypoints.append(self.floatize(dict(wpt.items())))

        #print(waypoints)

        for waypoint in waypoints:
            wpTypeXY = False
            wpTypeUTM = False
            wpTypeLatLon = False
            defaultAlt = True
            #waypoint = dict(waypoint)
            for key in waypoint:
                # Check wut keys we got
                if key is ('x' or 'y'):
                    wpTypeXY = True
                if key is ('lat' or 'lon'):
                    wpTypeLatLon = True
                if key is 'alt':
                    defaultAlt = False
            #print(dir(waypoint))
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

            #put all the required keys in
            for requiredKey in ('lat', 'lon', 'zone', 'northHemi', 'easting', 'northing', 'alt'):
                if not(requiredKey in waypoint):
                    waypoint[requiredKey] = 0

            waypoint['northHemi'] = True
            if wpTypeUTM:
                waypoint['wpType'] = 'utm'
            else:
                waypoint['wpType'] = 'latlon'

            #print(type(waypoint['lat']))
            wpobj = waypointobject.Waypoint(waypoint['name'], waypoint['wpID'], waypoint['wpType'], waypoint['lat'],waypoint['lon'],waypoint['zone'],waypoint['northHemi'],waypoint['easting'],waypoint['northing'],waypoint['alt'])
            self.db.addWaypoint(wpobj)

    def floatize(self, dictionaryWithBadStrings):
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
