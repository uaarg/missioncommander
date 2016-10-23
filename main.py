#!/usr/bin/python
# -*- coding: utf-8 -*-

# size.py

import wx
import wx_gui
import missioncommander

if __name__ == '__main__':
    app = wx.App()
    gui = wx_gui.MyFrame(None, title='Size', size=(600, 400))
    mc = missioncommander.main()
    gui.bindmc(mc)
    gui.connect_to_interop()
    app.MainLoop()
