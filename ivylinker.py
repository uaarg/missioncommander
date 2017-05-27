from config import *

class IvySender(ivyint):
    def __init__(self, verbose=False, callback = None):
        self.AC_ID = None
        self.verbose = verbose
        self.callback = callback
        self._interface = IvyMessagesInterface("Mission Commander", start_ivy=False)
        self._interface.subscribe(self.message_recv)
        self._interface.start()

    def bindMessageHandler(self, cb):
        self.callback = cb

    def message_recv(self, ac_id, msg):
        if (self.verbose and self.callback != None):
            self.callback(ac_id, msg)

    def shutdown(self):
        if DEBUG:
            print("Shutting down ivy interface...")
        self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def sendMessage(self, msg):
        if msg.msg_class == 'telemetry':
            msg['ac_id'] = self.AC_ID
            print(self.AC_ID)
        self._interface.send(msg)
