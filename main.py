#!/usr/bin/env python
# -*- coding: utf-8 -*-

# size.py

import wx
import wx_gui
import missioncommander
import sys, getopt

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




if __name__ == '__main__':
    password, username, url = argparser(sys.argv[1:])
    app = wx.App()
    gui = wx_gui.MyFrame( None, title='Size', size=(600, 400))
    gui.load_data(passw=password, usern=username, url=url)
    mc = missioncommander.main()
    gui.bindmc(mc)
    gui.connect_to_interop()
    app.MainLoop()
