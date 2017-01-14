#!/usr/bin/env python
from config import *

class IvySender(ivyint):
    def __init__(self, verbose=False, callback = None):
        self.verbose = verbose
        self.callback = callback
        self._interface = IvyMessagesInterface("Mission Commander", start_ivy=False)
        self._interface.subscribe(self.message_recv)
        self._interface.start()

    def message_recv(self, ac_id, msg):
        if (self.verbose and self.callback != None):
            self.callback(ac_id, msg)

    def shutdown(self):
        if DEBUG:
            print("Shutting down ivy interface...")
        self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def send_msg(self, msg):
        self._interface.send(msg)