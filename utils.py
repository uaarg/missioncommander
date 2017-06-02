class fancyList(list):
    '''
    Fancy list object that is fancy
    '''
    def __init__(self):
        super().__init__()

    def add(self, wp):
        self.append(wp)
    
    def prepend(self, wp):
        self.insert(0, wp)

    def addToIndex(self, wp, ind):
        while (len(self) <= ind):
            self.append(None)
        self[ind] = wp

    def replace(self, wp, index):
        try:
            self[index] = wp
            return True
        except:
            print("The WP Index is out of Range!! Use add or addToIndex")
            return False
    
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
            print("The WP Index is out of Range!! Use add or addToIndex")
            return None

    def getLength(self):
        return len(self)
