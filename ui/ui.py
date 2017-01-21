# Form implementation generated from reading ui file 'main_ui_template.ui'
# Created by: PyQt5 UI code generator 5.5.1

import sys
from threading import Thread
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets

translate = QtCore.QCoreApplication.translate

# No Operation (noop)
def noop():
    pass

class UiThread(Thread):
    """
    Thread to update graphical user interface.
    """
    def __init__(self, database):
        super(UiThread, self).__init__()
        self.ui = UI(database)
        self.ui.run()

    def run(self):
        while True:
            sleep(0.1)

class UI(QtCore.QObject):
    def __init__(self, database):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow(database)

    def run(self):
        self.mainWindow.show()
        return self.app.exec_()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, database):
        # Initialize Members
        super().__init__()
        self.db = database

        ################################################
        ### START OF QT DESIGNER AUTO-GENERATED CODE ###
        ################################################

        # Define Layout, Font, and Size Policy
        self.showMaximized()
        self.setWindowTitle(translate("mainWindow", "Mission Commander"))
        self.setObjectName("mainWindow")
        self.resize(1377, 1018)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1357, 949))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(16, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.scrollAreaGrid = QtWidgets.QGridLayout()
        self.scrollAreaGrid.setObjectName("scrollAreaGrid")
        self.lowerPane = QtWidgets.QGridLayout()
        self.lowerPane.setObjectName("lowerPane")
        self.RightPlane = QtWidgets.QGridLayout()
        self.RightPlane.setObjectName("RightPlane")
        self.interopFreqDisplay = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.interopFreqDisplay.setFont(font)
        self.interopFreqDisplay.setAutoFillBackground(False)
        self.interopFreqDisplay.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.interopFreqDisplay.setObjectName("interopFreqDisplay")
        self.RightPlane.addWidget(self.interopFreqDisplay, 1, 1, 1, 1)
        self.ivyMessageTSLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ivyMessageTSLabel.setFont(font)
        self.ivyMessageTSLabel.setObjectName("ivyMessageTSLabel")
        self.RightPlane.addWidget(self.ivyMessageTSLabel, 2, 0, 1, 1)
        self.ivyMessageTSDisplay = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ivyMessageTSDisplay.setFont(font)
        self.ivyMessageTSDisplay.setObjectName("ivyMessageTSDisplay")
        self.RightPlane.addWidget(self.ivyMessageTSDisplay, 2, 1, 1, 1)
        self.bottomRightBottomPane = QtWidgets.QGridLayout()
        self.bottomRightBottomPane.setObjectName("bottomRightBottomPane")
        self.RightPlane.addLayout(self.bottomRightBottomPane, 3, 1, 1, 1)
        self.interopFreqDisplay_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.interopFreqDisplay_2.setFont(font)
        self.interopFreqDisplay_2.setObjectName("interopFreqDisplay_2")
        self.RightPlane.addWidget(self.interopFreqDisplay_2, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 131, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.RightPlane.addItem(spacerItem1, 3, 0, 1, 1)
        self.lowerPane.addLayout(self.RightPlane, 0, 4, 1, 1)
        self.leftLowerPane = QtWidgets.QGridLayout()
        self.leftLowerPane.setObjectName("leftLowerPane")
        self.derouteButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.derouteButton.sizePolicy().hasHeightForWidth())
        self.derouteButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        self.derouteButton.setFont(font)
        self.derouteButton.setObjectName("derouteButton")
        self.leftLowerPane.addWidget(self.derouteButton, 0, 0, 1, 3)
        self.sendWaypointButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendWaypointButton.sizePolicy().hasHeightForWidth())
        self.sendWaypointButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        font.setItalic(False)
        self.sendWaypointButton.setFont(font)
        self.sendWaypointButton.setObjectName("sendWaypointButton")
        self.leftLowerPane.addWidget(self.sendWaypointButton, 2, 2, 1, 1)
        self.waypointComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waypointComboBox.sizePolicy().hasHeightForWidth())
        self.waypointComboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        self.waypointComboBox.setFont(font)
        self.waypointComboBox.setObjectName("waypointComboBox")
        self.leftLowerPane.addWidget(self.waypointComboBox, 2, 0, 1, 1)
        self.typeComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeComboBox.sizePolicy().hasHeightForWidth())
        self.typeComboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        font.setItalic(False)
        self.typeComboBox.setFont(font)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.leftLowerPane.addWidget(self.typeComboBox, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 61, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.leftLowerPane.addItem(spacerItem2, 3, 0, 1, 1)
        self.lowerPane.addLayout(self.leftLowerPane, 0, 3, 1, 1)
        self.scrollAreaGrid.addLayout(self.lowerPane, 1, 0, 1, 1)
        self.upperPane = QtWidgets.QGridLayout()
        self.upperPane.setObjectName("upperPane")
        self.unstagedListView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.unstagedListView.setObjectName("unstagedListView")
        self.upperPane.addWidget(self.unstagedListView, 1, 1, 1, 1)
        self.uasWaypointsLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.uasWaypointsLabel.setFont(font)
        self.uasWaypointsLabel.setObjectName("uasWaypointsLabel")
        self.upperPane.addWidget(self.uasWaypointsLabel, 0, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.upperPane.addItem(spacerItem3, 1, 4, 1, 1)
        self.stagedlistView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.stagedlistView.setObjectName("stagedlistView")
        self.upperPane.addWidget(self.stagedlistView, 1, 3, 1, 1)
        self.unstagedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.unstagedLabel.setFont(font)
        self.unstagedLabel.setObjectName("unstagedLabel")
        self.upperPane.addWidget(self.unstagedLabel, 0, 1, 1, 1)
        self.uavListView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.uavListView.setObjectName("uavListView")
        self.upperPane.addWidget(self.uavListView, 1, 5, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(165, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.upperPane.addItem(spacerItem4, 0, 2, 1, 1)
        self.stagedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.stagedLabel.setFont(font)
        self.stagedLabel.setObjectName("stagedLabel")
        self.upperPane.addWidget(self.stagedLabel, 0, 3, 1, 1)
        self.buttonScrollPane = QtWidgets.QGridLayout()
        self.buttonScrollPane.setObjectName("buttonScrollPane")
        self.replaceAllButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        self.replaceAllButton.setFont(font)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.buttonScrollPane.addWidget(self.replaceAllButton, 7, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.buttonScrollPane.addItem(spacerItem5, 2, 1, 1, 1)
        self.prependButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        self.prependButton.setFont(font)
        self.prependButton.setObjectName("prependButton")
        self.buttonScrollPane.addWidget(self.prependButton, 3, 1, 1, 1)
        self.replaceButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        font.setItalic(False)
        self.replaceButton.setFont(font)
        self.replaceButton.setObjectName("replaceButton")
        self.buttonScrollPane.addWidget(self.replaceButton, 5, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.buttonScrollPane.addItem(spacerItem6, 4, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 39, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.buttonScrollPane.addItem(spacerItem7, 0, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.buttonScrollPane.addItem(spacerItem8, 8, 1, 1, 1)
        self.appendButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        self.appendButton.setFont(font)
        self.appendButton.setObjectName("appendButton")
        self.buttonScrollPane.addWidget(self.appendButton, 1, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.buttonScrollPane.addItem(spacerItem9, 6, 1, 1, 1)
        self.upperPane.addLayout(self.buttonScrollPane, 1, 2, 1, 1)
        self.scrollAreaGrid.addLayout(self.upperPane, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.scrollAreaGrid, 0, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(16, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem10, 0, 2, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1377, 26))
        self.menuBar.setAutoFillBackground(False)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuMission = QtWidgets.QMenu(self.menuBar)
        self.menuMission.setObjectName("menuMission")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menuBar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionTask = QtWidgets.QAction(self)
        self.actionTask.setObjectName("actionTask")
        self.actionDocumentation = QtWidgets.QAction(self)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionClose = QtWidgets.QAction(self)
        self.actionClose.setObjectName("actionClose")
        self.actionImport = QtWidgets.QAction(self)
        self.actionImport.setObjectName("actionImport")
        self.actionClose_2 = QtWidgets.QAction(self)
        self.actionClose_2.setObjectName("actionClose_2")
        self.actionClose_Project = QtWidgets.QAction(self)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionExit_Program = QtWidgets.QAction(self)
        self.actionExit_Program.setObjectName("actionExit_Program")
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionClose_2)
        self.menuFile.addAction(self.actionClose_Project)
        self.menuFile.addAction(self.actionExit_Program)
        self.menuMission.addAction(self.actionTask)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuMission.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        # Translate text for all labels
        self.translateUi(self)

        ################################################
        ###  END OF QT DESIGNER AUTO-GENERATED CODE  ###
        ################################################

        # Model for Unstaged Listview
        unstagedListViewModel = QtGui.QStandardItemModel(self.upperPane)
        for mission in self.db.allMissions.lst:
            item = QtGui.QStandardItem(mission.name)
            item.setCheckable(True)
            unstagedListViewModel.appendRow(item)
        self.unstagedListView.setModel(unstagedListViewModel)

        # Button Bindings
        self.appendButton.clicked.connect(lambda: self.appendButtonAction(self))
        self.prependButton.clicked.connect(lambda: self.prependButtonAction(self))

        QtCore.QMetaObject.connectSlotsByName(self)

    # Prepend Button clicked_slot():
    def prependButtonAction(self, mainWindow):
        print('Prepend Button Pressed')
        print('List of Selected Mission')
        model = mainWindow.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))

    # Append Button clicked_slot():
    def appendButtonAction(self, mainWindow):
        print('Append Button Pressed')
        print('List of Selected Mission')
        model = mainWindow.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))

    # Used by Main Window Constructor
    def translateUi(self, mainWindow):
        mainWindow.setWindowTitle(translate("mainWindow", "Mission Commander"))
        self.derouteButton.setText(translate("mainWindow", "Quick Deroute"))
        self.sendWaypointButton.setText(translate("mainWindow", "Send Waypoint"))
        self.typeComboBox.setItemText(0, translate("mainWindow", "Path"))
        self.typeComboBox.setItemText(1, translate("mainWindow", "Circle"))
        self.uasWaypointsLabel.setText(translate("mainWindow", "Last UAS Waypoints"))
        self.unstagedLabel.setText(translate("mainWindow", "Unstaged Waypoints"))
        self.stagedLabel.setText(translate("mainWindow", "Staged Waypoints"))
        self.replaceAllButton.setText(translate("mainWindow", "Replace All"))
        self.prependButton.setText(translate("mainWindow", "Prepend"))
        self.replaceButton.setText(translate("mainWindow", "Replace"))
        self.appendButton.setText(translate("mainWindow", "Append"))
        self.menuFile.setTitle(translate("mainWindow", "File"))
        self.menuMission.setTitle(translate("mainWindow", "Mission"))
        self.menuHelp.setTitle(translate("mainWindow", "Help"))
        self.actionTask.setText(translate("mainWindow", "Task"))
        self.actionDocumentation.setText(translate("mainWindow", "Documentation"))
        self.actionClose.setText(translate("mainWindow", "Open Project"))
        self.actionImport.setText(translate("mainWindow", "Save Project"))
        self.actionClose_2.setText(translate("mainWindow", "Import Project"))
        self.actionClose_Project.setText(translate("mainWindow", "Close Project"))
        self.actionExit_Program.setText(translate("mainWindow", "Exit Program"))

class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == QtCore.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()
