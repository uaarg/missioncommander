import xml.etree.ElementTree as ET

class xmlreader:
    def __init__(self):
        self.waypoints = []
        self.commands = []
        self.stagedlist = []


    def openfile(self,  filepath, callback=None):
        tree = ET.parse(filepath)
        root = tree.getroot()


        for waypoint in root.iter('waypoint'):
            self.waypoints.append(waypoint.attrib)


        i = 0
        for command in root.iter('command'):
            self.commandmsg = ""
            print command.keys()
            for element in command.keys():
                print element
                if (element != "id" and element != "name"):
                    self.commandmsg = self.commandmsg + element + "=" + command.get(element) + " "

            self.commands.append(command.attrib)
            self.commands[i]['msg'] = self.commandmsg
            i = i+1
        print self.commands


        for staged in root.iter('staged'):
            self.stagedlist.append(staged.attrib)



        if callback != None :
            callback(self.commands)
