# Form implementation generated from reading ui file 'main_ui_template.ui'
# Created by: PyQt5 UI code generator 5.5.1

import sys, os
from threading import Thread
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from database import  InsertMode, NavPattern, Mission, exportxml
from config import *
from utils import fancyList

translate = QtCore.QCoreApplication.translate

RADIUS_DISABLED_TEXT = "Radius field (Disabled)"

ICON_ABSOLUTE_PATH = os.path.join(PPRZ_SRC, 'sw', 'ext', 'missioncommander', 'data', 'icon')

# No Operation (noop)
def noop():
    pass

class UI(QtCore.QObject):
    def __init__(self, database, send_ivy_message, ac_id):
        """
        Initialize the UI.
        Args:
            database: A database.BagOfHolding object containing information about the aircraft mission.
            send_ivy_message: A callback to a function that, given a string, send that string as a message over an Ivy bus to the aircraft.
        """
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow(database, send_ivy_message, ac_id)

    def run(self):
        self.mainWindow.show()
        return self.app.exec_()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, database, send_ivy_message, ac_id):
        # Initialize Members
        super().__init__()
        self.db = database
        self.ivySender = send_ivy_message
        self.ac_id = ac_id
        ################################################
        ### START OF QT DESIGNER AUTO-GENERATED CODE ###
        ################################################

        # Define Layout, Font, and Size Policy
        self.showMaximized()
        self.setWindowTitle(translate("mainWindow", "Mission Commander"))
        self.setObjectName("mainWindow")
        self.resize(1377, 1018)
        font = QtGui.QFont()
        font.setPointSize(18)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        self.interopFreqDisplay = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.interopFreqDisplay.setSizePolicy(sizePolicy)
        self.interopFreqDisplay.setFont(font)
        self.interopFreqDisplay.setReadOnly(True)
        self.interopFreqDisplay.setObjectName("interopFreqDisplay")
        self.RightPlane.addWidget(self.interopFreqDisplay, 1, 1, 1, 1)
        self.ivyMessageTSLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ivyMessageTSLabel.setFont(font)
        self.ivyMessageTSLabel.setObjectName("ivyMessageTSLabel")
        self.ivyMessageTSLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.RightPlane.addWidget(self.ivyMessageTSLabel, 1, 2, 1, 1)
        self.ivyMessageTSDisplay = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.ivyMessageTSDisplay.setSizePolicy(sizePolicy)
        self.ivyMessageTSDisplay.setFont(font)
        self.ivyMessageTSDisplay.setObjectName("ivyMessageTSDisplay")
        self.ivyMessageTSDisplay.setReadOnly(True)
        self.RightPlane.addWidget(self.ivyMessageTSDisplay, 1, 3, 1, 1)
        self.bottomRightBottomPane = QtWidgets.QGridLayout()
        self.bottomRightBottomPane.setObjectName("bottomRightBottomPane")
        self.RightPlane.addLayout(self.bottomRightBottomPane, 3, 1, 1, 1)
        self.interopFreqLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.interopFreqLabel.setFont(font)
        self.interopFreqLabel.setObjectName("interopFreqLabel")
        self.interopFreqLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.RightPlane.addWidget(self.interopFreqLabel, 1, 0, 1, 1)
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
        self.derouteButton.setFont(font)
        self.derouteButton.setObjectName("derouteButton")
        self.leftLowerPane.addWidget(self.derouteButton, 0, 0, 1, 3)
        self.sendMissionButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendMissionButton.sizePolicy().hasHeightForWidth())
        self.sendMissionButton.setSizePolicy(sizePolicy)
        self.sendMissionButton.setFont(font)
        self.sendMissionButton.setObjectName("sendMissionButton")
        self.leftLowerPane.addWidget(self.sendMissionButton, 2, 2, 1, 1)
        self.createMissionButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.createMissionButton.setSizePolicy(sizePolicy)
        self.createMissionButton.setFont(font)
        self.createMissionButton.setObjectName("createMissionButton")
        self.leftLowerPane.addWidget(self.createMissionButton, 2, 2, 2, 1)
        self.waypointOneComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.waypointTwoComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waypointOneComboBox.sizePolicy().hasHeightForWidth())
        self.waypointOneComboBox.setSizePolicy(sizePolicy)
        self.waypointOneComboBox.setFont(font)
        self.waypointOneComboBox.setObjectName("waypointOneComboBox")
        self.leftLowerPane.addWidget(self.waypointOneComboBox, 2, 0, 1, 1)
        self.waypointTwoComboBox.setSizePolicy(sizePolicy)
        self.waypointTwoComboBox.setFont(font)
        self.waypointTwoComboBox.setObjectName("waypointTwoComboBox")
        self.leftLowerPane.addWidget(self.waypointTwoComboBox, 2, 0, 2, 1)
        self.missionTypeComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.missionTypeComboBox.sizePolicy().hasHeightForWidth())
        self.missionTypeComboBox.setSizePolicy(sizePolicy)
        self.missionTypeComboBox.setFont(font)
        self.missionTypeComboBox.setObjectName("missionTypeComboBox")
        self.leftLowerPane.addWidget(self.missionTypeComboBox, 2, 1, 1, 1)
        self.radiusField = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.radiusField.setSizePolicy(sizePolicy)
        self.radiusField.setFont(font)
        self.radiusField.setReadOnly(True)
        self.radiusField.setText(RADIUS_DISABLED_TEXT)
        self.radiusField.setObjectName("interopFreqDisplay")
        self.leftLowerPane.addWidget(self.radiusField, 2, 1, 2, 1)
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
        self.uasWaypointsLabel.setFont(font)
        self.uasWaypointsLabel.setObjectName("uasWaypointsLabel")
        self.upperPane.addWidget(self.uasWaypointsLabel, 0, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.upperPane.addItem(spacerItem3, 1, 4, 1, 1)
        self.stagedlistView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.stagedlistView.setObjectName("stagedlistView")
        self.upperPane.addWidget(self.stagedlistView, 1, 3, 1, 1)
        self.unstagedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.unstagedLabel.setFont(font)
        self.unstagedLabel.setObjectName("unstagedLabel")
        self.upperPane.addWidget(self.unstagedLabel, 0, 1, 1, 1)
        self.uavListView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.uavListView.setObjectName("uavListView")
        self.upperPane.addWidget(self.uavListView, 1, 5, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(165, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.upperPane.addItem(spacerItem4, 0, 2, 1, 1)
        self.stagedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.stagedLabel.setFont(font)
        self.stagedLabel.setObjectName("stagedLabel")
        self.upperPane.addWidget(self.stagedLabel, 0, 3, 1, 1)
        self.buttonScrollPane = QtWidgets.QGridLayout()
        self.buttonScrollPane.setObjectName("buttonScrollPane")
        self.replaceAllButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.replaceAllButton.setFont(font)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.buttonScrollPane.addWidget(self.replaceAllButton, 7, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.buttonScrollPane.addItem(spacerItem5, 2, 1, 1, 1)
        self.prependButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prependButton.setFont(font)
        self.prependButton.setObjectName("prependButton")
        self.buttonScrollPane.addWidget(self.prependButton, 3, 1, 1, 1)
        self.replaceButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
        self.appendButton.setFont(font)
        self.appendButton.setObjectName("appendButton")
        self.buttonScrollPane.addWidget(self.appendButton, 1, 1, 1, 1)

        self.takeoffBlockToggleButton = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICON_ABSOLUTE_PATH, 'pilot-hat.png')), 'Takeoff', self.scrollAreaWidgetContents)
        self.takeoffBlockToggleButton.setSizePolicy(sizePolicy)
        self.takeoffBlockToggleButton.setFont(font)
        self.takeoffBlockToggleButton.setCheckable(True)
        self.RightPlane.addWidget(self.takeoffBlockToggleButton, 2, 0, 2, 1)
        self.standbyBlockToggleButton = QtWidgets.QPushButton('Standby', self.scrollAreaWidgetContents)
        self.standbyBlockToggleButton.setSizePolicy(sizePolicy)
        self.standbyBlockToggleButton.setFont(font)
        self.standbyBlockToggleButton.setCheckable(True)
        self.standbyBlockToggleButton.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(ICON_ABSOLUTE_PATH, 'planes-circling.png'))))
        self.RightPlane.addWidget(self.standbyBlockToggleButton, 2, 1, 2, 1)
        self.missionBlockToggleButton = QtWidgets.QPushButton('Mission', self.scrollAreaWidgetContents)
        self.missionBlockToggleButton.setSizePolicy(sizePolicy)
        self.missionBlockToggleButton.setFont(font)
        self.missionBlockToggleButton.setCheckable(True)
        self.missionBlockToggleButton.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(ICON_ABSOLUTE_PATH, 'departures.png'))))
        self.RightPlane.addWidget(self.missionBlockToggleButton, 2, 2, 2, 1)
        self.landingBlockToggleButton = QtWidgets.QPushButton('Landing', self.scrollAreaWidgetContents)
        self.landingBlockToggleButton.setSizePolicy(sizePolicy)
        self.landingBlockToggleButton.setFont(font)
        self.landingBlockToggleButton.setCheckable(True)
        self.landingBlockToggleButton.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(ICON_ABSOLUTE_PATH, 'arrivals.png'))))
        self.RightPlane.addWidget(self.landingBlockToggleButton, 2, 3, 2, 1)

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
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionImport = QtWidgets.QAction(self)
        self.actionImport.setObjectName("actionImport")
        self.actionClose_Project = QtWidgets.QAction(self)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionExit_Program = QtWidgets.QAction(self)
        self.actionExit_Program.setObjectName("actionExit_Program")
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionClose_Project)
        self.menuFile.addAction(self.actionExit_Program)
        self.menuMission.addAction(self.actionTask)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuMission.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.insertAction = QtWidgets.QAction("Insert", self)


        # Translate text for all labels
        self.translateUi()

        ################################################
        ###  END OF QT DESIGNER AUTO-GENERATED CODE  ###
        ################################################

        # QWidget Initializations
        self.checkMissionTypeComboBox()

        # Model for Unstaged Listview
        self.updateUnstagedMissionList()

        # Model for staged Listview
        self.updateStagedMissionList()


        self.updateUavListViewList()


        # Waypoint Comboboxes Content
        waypointComboBoxModel = QtGui.QStandardItemModel(self.upperPane)
        for waypoint in self.db.waypoints.items():
            item = QtGui.QStandardItem(waypoint[0])
            waypointComboBoxModel.appendRow(item)
        self.waypointOneComboBox.setModel(waypointComboBoxModel)
        self.waypointTwoComboBox.setModel(waypointComboBoxModel)

        # Mission combobox
        missionComboBoxModel = QtGui.QStandardItemModel(self.upperPane)
        for name, mission in NavPattern.__members__.items():
            if "LLA" not in name:
                item = QtGui.QStandardItem(mission.value.capitalize())
                missionComboBoxModel.appendRow(item)
        self.missionTypeComboBox.setModel(missionComboBoxModel)

        # Button Bindings
        self.appendButton.clicked.connect(lambda: self.appendButtonAction())
        self.prependButton.clicked.connect(lambda: self.prependButtonAction())
        self.replaceButton.clicked.connect(lambda: self.replaceButtonAction())
        self.replaceAllButton.clicked.connect(lambda: self.replaceAllButtonAction())
        self.sendMissionButton.clicked.connect(lambda: self.sendMissionButtonAction())
        self.createMissionButton.clicked.connect(lambda: self.createMissionButtonAction())
        self.derouteButton.clicked.connect(lambda: self.derouteButtonAction())
        self.missionBlockToggleButton.clicked.connect(lambda: self.setActiveFlightBlockAction('Mission'))
        self.takeoffBlockToggleButton.clicked.connect(lambda: self.setActiveFlightBlockAction('Takeoff'))
        self.standbyBlockToggleButton.clicked.connect(lambda: self.setActiveFlightBlockAction('Standby'))
        self.landingBlockToggleButton.clicked.connect(lambda: self.setActiveFlightBlockAction('InitAutoLanding'))

        # Flight Block List (so only the CURRENT flight block is toggled)
        self.flightBlockDict = dict()
        self.flightBlockDict['Takeoff'] = self.takeoffBlockToggleButton
        self.flightBlockDict['Mission'] = self.missionBlockToggleButton
        self.flightBlockDict['Standby'] = self.standbyBlockToggleButton
        self.flightBlockDict['InitAutoLanding'] = self.landingBlockToggleButton
        # Shortcuts
        self.actionExit_Program.setShortcut('Ctrl+Q')
        self.actionSave.setShortcut('Ctrl+S')
        self.appendButton.setShortcut('Ctrl+A')
        self.prependButton.setShortcut('Ctrl+P')

        self.insertAction.setShortcut('Ctrl+I')

        # Signals
        self.missionTypeComboBox.currentIndexChanged.connect(lambda: self.checkMissionTypeComboBox())
        self.db.signals.uas_update.connect(lambda: self.updateUavListViewList())
        self.db.signals.stagedListUpdate.connect(lambda: self.updateStagedMissionList())
        self.db.signals.resendMissionstoUI.connect(lambda: self.resendMissions())
        self.db.signals.updateFlightBlock.connect(lambda: self.setActiveFlightBlockAction())


        # Action Bindings
        self.actionSave.triggered.connect(lambda: self.saveMissionState())
        self.insertAction.triggered.connect(lambda: self.insertMissions())
        QtCore.QMetaObject.connectSlotsByName(self)

    def updateUavListViewList(self):
        uavlistViewModel = QtGui.QStandardItemModel(self.upperPane)
        for airMission in list(self.db.airMissionStatus):
            item = QtGui.QStandardItem(airMission.name)
            item.setEditable(False)
            uavlistViewModel.appendRow(item)
        self.uavListView.setModel(uavlistViewModel)

    def updateStagedMissionList(self):
        stagedlistViewModel = QtGui.QStandardItemModel(self.upperPane)
        for stagedMission in self.db.groundMissionStatus:
            item = QtGui.QStandardItem(stagedMission.name)
            item.setEditable(False)
            stagedlistViewModel.appendRow(item)
        self.stagedlistView.setModel(stagedlistViewModel)

    def updateUnstagedMissionList(self):
        unstagedListViewModel = QtGui.QStandardItemModel(self.upperPane)
        for mission in self.db.allMissions.items():
            item = QtGui.QStandardItem(mission[0])
            item.setCheckable(True)
            item.setEditable(False)
            unstagedListViewModel.appendRow(item)
        for task in self.db.tasks.items():
            self.appendItemToRowCheckable(unstagedListViewModel,task[0])
        self.unstagedListView.setModel(unstagedListViewModel)

    def appendItemToRowCheckable(self, qItemModel, itemName):
        item = QtGui.QStandardItem(itemName)
        item.setCheckable(True)
        item.setEditable(False)
        qItemModel.appendRow(item)

    # Prepend Button clicked_slot():
    def prependButtonAction(self):

        print('Prepend Button Pressed')
        print('List of Selected Mission')
        model = self.unstagedListView.model()

        # Find Checkboxed Items
        for index in reversed(range(model.rowCount())):  #Reverse the list so that when prepend is called individually for each, it is the same order as if the whole list were prepended at once
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                itemName = item.index().data()
                print('Index %s with Mission: %s' % (item.row(), itemName))
                if (itemName in self.db.allMissions):
                    currentMission = self.db.allMissions[itemName]
                    ivyMsg = currentMission.gen_mission_msg(self.ac_id, self.db, InsertMode.Prepend)
                    self.ivySender(ivyMsg)
                    self.db.groundMissionStatus.prepend(currentMission)
                else:
                    currentTask = self.db.tasks[itemName]
                    for missID in reversed(currentTask.missions):
                        #currentMission = self.db.findMissionById(missID)
                        ivyMsg = currentMission.gen_mission_msg(self.ac_id, self.db, InsertMode.Prepend, currentTask.id)
                        self.ivySender(ivyMsg)
                        self.db.groundMissionStatus.prepend(currentMission)

        self.updateStagedMissionList()
        self.updateUnstagedMissionList()



    # Append Button clicked_slot():
    def appendButtonAction(self):
        print('Append Button Pressed')
        print('List of Selected Mission')
        model = self.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                itemName = item.index().data()
                print('Index %s with Mission: %s' % (item.row(), itemName))
                if (itemName in self.db.allMissions):
                    currentMission = self.db.allMissions[itemName]
                    ivyMsg = currentMission.gen_mission_msg(self.ac_id, self.db, InsertMode.Append)
                    if DEBUG:
                        print(ivyMsg)
                        for key in ivyMsg.to_dict().keys():
                            print(key + ' is ' +str(ivyMsg.to_dict()[key]))
                            print(type(ivyMsg.to_dict()[key]))
                    self.ivySender(ivyMsg)
                    self.db.groundMissionStatus.add(currentMission)
                else: #Tasks
                    currentTask = self.db.tasks[itemName]
                    for missID in currentTask.missions:
                        currentMission = self.db.findMissionById(missID)
                        ivyMsg = currentMission.gen_mission_msg(self.ac_id, self.db, InsertMode.Append, currentTask.id)
                        self.ivySender(ivyMsg)
                        self.db.groundMissionStatus.add(currentMission)

        self.updateStagedMissionList()
        self.updateUnstagedMissionList()

    def replaceButtonAction(self):
        print('Replace button Pressed')
        model = self.unstagedListView.model()
        #Find selected row
        print('Replace mission:')
        selectedIndexes = self.stagedlistView.selectedIndexes()
        if len(selectedIndexes) == 1:
            replaceIndex = selectedIndexes[0].row()
            print(selectedIndexes[0].data())
            print(replaceIndex)
        else:
            print('Select one and only one mission')
            return

        insertList = list()

        ## TODO: cannot replace with Tasks

        # Find Checkboxed Items
        print('List of Selected Missions')
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                itemName = item.index().data()
                print('Index %s with Mission: %s' % (item.row(), itemName))
                if itemName in self.db.allMissions:
                    current_mission = self.db.allMissions[itemName]
                    insertList.append(current_mission)
                else:#Tasks
                    currentTask = self.db.tasks[itemName]
                    for missID in currentTask.missions:
                        insertList.append(self.db.findMissionById(missID))
        print('replaceList')
        givenReplaceIndex = replaceIndex
        insertIndex = 0
        shiftingList = list()
        while insertIndex < len(insertList) or len(shiftingList) > 0:
            if insertIndex == 0:
                ivyMsg = insertList[0].gen_mission_msg(self.ac_id,self.db, InsertMode.ReplaceIndex, 0, replaceIndex)
                self.ivySender(ivyMsg)
                replaceIndex += 1
                insertIndex += 1
                continue

            if insertIndex < len(insertList):
                currentMission = insertList[insertIndex]
            else:
                currentMission = shiftingItem = shiftingList.pop(0)

            if replaceIndex < len(self.db.groundMissionStatus):
                ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.ReplaceIndex, 0, replaceIndex)
                shiftingList.append(self.db.groundMissionStatus.getFromIndex(replaceIndex))
                self.ivySender(ivyMsg)
                replaceIndex += 1
                insertIndex += 1
            else:
                ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.Append)
                self.ivySender(ivyMsg)
                replaceIndex += 1
                insertIndex += 1

        self.db.groundMissionStatus.replace(insertList, givenReplaceIndex)
        self.updateStagedMissionList()
        self.updateUnstagedMissionList()

    def replaceAllButtonAction(self):
        print('replace all button pressed')
        print('List of Selected Missions')
        model = self.unstagedListView.model()

        insertList = fancyList()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                itemName = item.index().data()
                print('Index %s with Mission: %s' % (item.row(), itemName))
                if (itemName in self.db.allMissions):
                    currentMission = self.db.allMissions[itemName]
                    ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.Append)
                    if len(insertList) == 0:
                        ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.ReplaceAll)
                    self.ivySender(ivyMsg)
                    insertList.append(currentMission)
                else: #Task
                    currentTask = self.db.tasks[itemName]
                    for missID in currentTask.missions:
                        currentMission = self.db.findMissionById(missID)
                        ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.Append)
                        if len(insertList) == 0:
                            ivyMsg = currentMission.gen_mission_msg(self.ac_id,self.db, InsertMode.ReplaceAll)
                        self.ivySender(ivyMsg)
                        insertList.append(currentMission)

        #self.db.groundMissionStatus.replaceAll(insertList)
        self.updateStagedMissionList()
        self.updateUnstagedMissionList()

    def insertMissions(self):
        '''
        Inserts checked missions just after the selested staged mission.
        '''
        # Find selected mission
        print('Insert action Triggered')
        model = self.unstagedListView.model()
        #Find selected row
        print('Keep mission:')
        selectedIndexes = self.stagedlistView.selectedIndexes()
        if len(selectedIndexes) == 1:
            replaceIndex = selectedIndexes[0].row()
            print(selectedIndexes[0].data())
            print(replaceIndex)
        else:
            print('Select one and only one mission')
            return


        print('List of Selected Missions')
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                itemName = item.index().data()
                print('Index %s with Mission: %s' % (item.row(), itemName))
                if itemName in self.db.allMissions:
                    current_mission = self.db.allMissions[itemName]
                    insertList.append(current_mission)
                else:#Tasks
                    currentTask = self.db.tasks[itemName]
                    for missID in currentTask.missions:
                        insertList.append(self.db.findMissionById(missID))
        print('replaceList')
        insertList = []
    def resendMissions(self):
        '''
        Resends all the missions currently on the plane to update a moved waypoint or changed mission.
        '''

        self.ivySender(self.db.groundMissionStatus[0].gen_mission_msg(self.ac_id, self.db, InsertMode.ReplaceAll))
        for index in range(1,len(self.db.groundMissionStatus)):
            self.ivySender(self.db.groundMissionStatus[index].gen_mission_msg(self.ac_id, self.db, InsertMode.Append))

        self.updateStagedMissionList()
        self.updateUnstagedMissionList()

    def updateListViews(self):
        print("Needs to be completed")


    def createMissionButtonAction(self):
        waypointOneName = self.waypointOneComboBox.currentText()
        missionType = self.missionTypeComboBox.currentText().lower()
        radius = 0

        if missionType in [NavPattern.MISSION_SEGMENT.value, NavPattern.MISSION_PATH.value, NavPattern.MISSION_SURVEY.value]:
            waypointTwoName = self.waypointTwoComboBox.currentText()
            print('Waypoint 1: %s, Waypoint 2: %s, Mission Type: %s' % (waypointOneName, waypointTwoName, missionType))
            waypointArray = [waypointOneName, waypointTwoName]
        else:
            print('Waypoint 1: %s, Mission Type: %s' % (waypointOneName, missionType))
            waypointArray = [waypointOneName]
        if missionType == NavPattern.MISSION_CIRCLE.value:
            if self.radiusField.text().isdigit():
                radius = int(self.radiusField.text())
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Circle requires valid radius")
                ret = msgBox.exec_()
                raise AttributeError("Circle requires valid radius")
        # Create Mission Object. Add to missions database
        print('radius: %s' % (radius))
        missionObj = Mission(len(self.db.allMissions) + 1, -1, NavPattern(missionType + '_lla'), waypointArray, radius)
        print(missionObj.name)
        self.db.addMission([(missionObj.name , missionObj)])
        self.updateUnstagedMissionList()
        return missionObj

    def sendMissionButtonAction(self):
        missionObj = self.createMissionButtonAction()
        self.db.groundMissionStatus.add(missionObj)
        self.updateStagedMissionList()
        ivyMsg = missionObj.gen_mission_msg(self.ac_id, self.db,  InsertMode.Append)
        print(ivyMsg)
        self.ivySender(ivyMsg)


    def derouteButtonAction(self):
        waypointOneName = self.waypointOneComboBox.currentText()
        missionType = self.missionTypeComboBox.currentText().lower()
        radius = 0

        if missionType in [NavPattern.MISSION_SEGMENT.value, NavPattern.MISSION_PATH.value, NavPattern.MISSION_SURVEY.value]:
            waypointTwoName = self.waypointTwoComboBox.currentText()
            print('Waypoint 1: %s, Waypoint 2: %s, Mission Type: %s' % (waypointOneName, waypointTwoName, missionType))
            waypointArray = [waypointOneName, waypointTwoName]
        else:
            print('Waypoint 1: %s, Mission Type: %s' % (waypointOneName, missionType))
            waypointArray = [waypointOneName]
        if missionType == NavPattern.MISSION_CIRCLE.value:
            if self.radiusField.text().isdigit():
                radius = int(self.radiusField.text())
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Circle requires valid radius")
                ret = msgBox.exec_()
                raise AttributeError("Circle requires valid radius")
        # Create Mission Object. Add to missions database
        missionObj = Mission(len(self.db.allMissions) +1, -1, NavPattern(missionType + '_lla'), waypointArray, radius)
        print(missionObj.name)
        self.db.addMission([(missionObj.name , missionObj)])
        self.updateUnstagedMissionList()
        self.db.groundMissionStatus.add(missionObj)
        self.updateStagedMissionList()
        self.ivySender(missionObj.gen_mission_msg(self.ac_id, self.db, InsertMode.Prepend))


    def checkMissionTypeComboBox(self):
        missionType = self.missionTypeComboBox.currentText().lower()
        if missionType in [NavPattern.MISSION_SEGMENT.value, NavPattern.MISSION_PATH.value, NavPattern.MISSION_SURVEY.value]:
            self.waypointTwoComboBox.setEnabled(True)
        else:
            self.waypointTwoComboBox.setEnabled(False)
        if missionType == NavPattern.MISSION_CIRCLE.value:
            self.radiusField.setReadOnly(False)
            self.radiusField.setText("Enter radius")
        else:
            self.radiusField.setReadOnly(True)
            self.radiusField.setText(RADIUS_DISABLED_TEXT)

    def updateListViews(self):
        print("Needs to be completed")

    def saveMissionState(self):
        exportxml.bindDBandFilepath('data/', self.db)
        exportxml.writeXML()

    def setActiveFlightBlockAction(self, flightBlockName = 'checkDatabase'):
        '''
        Sends Ivy Message to jump to 'flightBlockName'. Also toggles UI buttons so only 'flightBlockName' is selected.
        '''

        if flightBlockName == 'checkDatabase': # Then its from main and only needs to update toggle
            flightBlockName = self.db.currentFlightBlock.name
        else:
            ivyMsg = self.db.flightBlocks.getFlightBlockByName(flightBlockName).gen_change_block_msg()
            print('Current Flight Block is now ' + flightBlockName)
            print(ivyMsg)
            self.ivySender(ivyMsg)

        for flightBlock in self.flightBlockDict.keys():
            if flightBlock == flightBlockName:
                self.flightBlockDict[flightBlock].setChecked(True)
            else:
                self.flightBlockDict[flightBlock].setChecked(False)



    # Used by Main Window Constructor
    def translateUi(self):
        self.setWindowTitle(translate("mainWindow", "Mission Commander"))
        self.derouteButton.setText(translate("mainWindow", "Quick Deroute"))
        self.sendMissionButton.setText(translate("mainWindow", "Send Mission"))
        self.createMissionButton.setText(translate("mainWindow", "Create Mission"))
        self.uasWaypointsLabel.setText(translate("mainWindow", "UAS Missions"))
        self.ivyMessageTSLabel.setText(translate("mainWindow", "Last Ivy Message Timestamp"))
        self.interopFreqLabel.setText(translate("mainWindow", "Interoperability Frequency"))
        self.unstagedLabel.setText(translate("mainWindow", "Unstaged Missions"))
        self.stagedLabel.setText(translate("mainWindow", "Staged Missions"))
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
        self.actionSave.setText(translate("mainWindow", "Save Project"))
        self.actionImport.setText(translate("mainWindow", "Import Project"))
        self.actionClose_Project.setText(translate("mainWindow", "Close Project"))
        self.actionExit_Program.setText(translate("mainWindow", "Exit Program"))
