import logging
logger = logging.getLogger(__name__)

class fancyList(list):
    '''
    Fancy list object that is fancy
    '''
    def __init__(self):
        super().__init__()
        '''
        if len(wp) is 1:
            try:
                self[index] = wp
                return True
            except:
                print("The WP Index is out of Range!! Use add or addToIndex")
                return False
        '''
    def add(self, wp):
        self.append(wp)

    def prepend(self, wp):
        self.insert(0, wp)

    def addToIndex(self, wp, ind):
        while (len(self) <= ind):
            self.append(None)
        self[ind] = wp

    def replace(self, wp, index):
        '''
        Inserts a list into the fancyList at the index specified.
        Note the old entry at self[index] is removed.
        '''
        for i in range(0,(len(wp) + index)):
            if i < index: # Not reached replace
                pass
            elif i == index: # Replace time
                if type(wp) is type([]):
                    self[index] = wp[0]
                else:
                    self[index] = wp
            else: # i > index
                self.insert(i, wp[i-index])

    def replaceAll(self, wps):

        if type(wps).__name__ == 'fancyList':
            self.clear()
            for e in wps:
                self.append(e)
        else:
            raise NameError('Cannot fancify something that is not fancy')

    def getFromIndex(self, ind):
        try:
            return self[ind]
        except:
            print("The Index is out of Range!! Use add or addToIndex")
            return None

    def getLength(self):
        return len(self)
