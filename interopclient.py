import requests
import ast
from time import time


class Connection():

    def __init__(self, baseurl, username, password):
        self.baseurl = baseurl
        self.username = username
        self.password = password
        self.loginsucess = False
        self.s = requests.Session()
        self.lasttele = 0
        data = {"username":self.username, "password":self.password}
        loginurl = "/api/login"
        try:
            self.login = self.s.post(self.baseurl+loginurl, data=data)
            self.loginsucess = True
            pass
        except Exception as e:
            print("Failed to login to interop server")
            pass


    def getobstacleinfo(self):
        ob = self.s.get(self.baseurl+"/api/obstacles")
        objects = ast.literal_eval(ob.text)
        return objects

    def updatetelemetry(self, tele):
        tl = self.s.post(self.baseurl+"/api/telemetry", tele )
        return tl.status_code
