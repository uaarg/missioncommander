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
            flightParams = dict(fancy)
        #print (flightParams)
        #print ('Home is at Lat:' + flightParams['lat0'] + 'deg Lon:' + flightParams['lon0'] + 'deg')

        for key in flightParams:
            try:
                flightParams[key]= float(flightParams[key])
            except:
                pass

        utmHome = utm.from_latlon(flightParams['lat0'], flightParams['lon0'])
        #print(utmHome)
        flightParams['easting0'] = utmHome[0]
        flightParams['northing0'] = utmHome[1]
        flightParams['utmZoneNumber0'] = utmHome[2]
        flightParams['utmZoneLetter0'] = utmHome[3]
        #print(flightParams)

        # Get waypoints from XML
        waypoints = []
        for wpt in root.iter('waypoint'):
            waypoints.append(dict(wpt.items()))
        print(waypoints)
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
            waypoint['wpID'] = int(wpID)
            wpID = wpID + 1
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

            wpobj = waypointobject.Waypoint(waypoint['name'], waypoint['wpID'],  waypoint['wpType'], waypoint['lat'],waypoint['lon'],waypoint['zone'],waypoint['northHemi'],waypoint['easting'],waypoint['northing'],waypoint['alt'])
            self.db.addWaypointToIndex(wpobj)
