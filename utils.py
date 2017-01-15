import ivylinker

sendIvyMSG = ivylinker.sendIvyMSG

class fancyList(object):
    '''
    Fancy list object that is fancy
    '''
    def __init__(self):
        self.lst = list()

    def add(self, wp):
        self.lst.append(wp)

    def addToIndex(self, wp):
        ind = wp.index
        while (len(self.lst) <= ind):
            self.lst.append(None)
        self.lst[ind] = wp

    def replace(self, wp):
        try:
            self.lst[wp.index] = wp
            return True
        except:
            print("The WP Index is out of Range!! Use add or addToIndex")
            return False



    def getFromIndex(self, ind):
        try:
            return self.lst[ind]
        except:
            print("The WP Index is out of Range!! Use add or addToIndex")
            return None



