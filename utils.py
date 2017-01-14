import ivylinker

sendMSG = ivylinker.sendMSG

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

    def update(self, wp):
        self.lst[wp.index] = wp

    def get(self, wp):
        return self.lst[wp.index]

        