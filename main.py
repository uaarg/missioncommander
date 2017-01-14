import sys, getopt
from ivylinker import IvySender
from database import bagOfHolding

def argparser(argv):
    url = "http://localhost:8000"
    username = "testuser"
    password = "testpass"
    try:
        opts, args = getopt.getopt(argv,"hl:u:p:",["url=","username=","password="])
    except getopt.GetoptError:
        print 'main.py -l <url> -u <username> -p <password>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -l <url> -u <username> -p <password>'
            sys.exit()
        elif opt in ("-l", "--url"):
            url = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
    return password, username, url


class MissionCommander(object):
    def __init__(self):
        self.db = bagOfHolding()
        self.ivy = IvySender(verbose=True, callback = self.ivyCallBack)

    def ivyMsgHandler(self, msg):
        if (msg.name == "WALDO"):
            self.db.updateTelemetry(msg)

if __name__ == '__main__':
    password, username, url = argparser(sys.argv[1:])
