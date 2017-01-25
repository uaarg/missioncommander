# Form implementation generated from reading ui file 'main_ui_template.ui'
# Created by: PyQt5 UI code generator 5.5.1

import sys
from threading import Thread
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from mission import NavPattern

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
        self.RightPlane.addWidget(self.ivyMessageTSLabel, 2, 0, 1, 1)
        self.ivyMessageTSDisplay = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.ivyMessageTSDisplay.setSizePolicy(sizePolicy)
        self.ivyMessageTSDisplay.setFont(font)
        self.ivyMessageTSDisplay.setObjectName("ivyMessageTSDisplay")
        self.ivyMessageTSDisplay.setReadOnly(True)
        self.RightPlane.addWidget(self.ivyMessageTSDisplay, 2, 1, 1, 1)
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
        self.waypointTwoComboBox.setObjectName("waypointOneComboBox")
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
        self.translateUi()

        ################################################
        ###  END OF QT DESIGNER AUTO-GENERATED CODE  ###
        ################################################

        # QWidget Initializations
        self.checkMissionTypeComboBox()

        # Model for Unstaged Listview
        unstagedListViewModel = QtGui.QStandardItemModel(self.upperPane)
        for mission in self.db.allMissions.lst:
            item = QtGui.QStandardItem(mission.name)
            item.setCheckable(True)
            item.setEditable(False)
            unstagedListViewModel.appendRow(item)
        self.unstagedListView.setModel(unstagedListViewModel)

        # Model for staged Listview
        stagedlistViewModel = QtGui.QStandardItemModel(self.upperPane)
        for stagedMission in self.db.airMissionStatus.airMissionList.lst:
            item = QtGui.QStandardItem(stagedMission.name)
            item.setEditable(False)
            stagedlistViewModel.appendRow(item)
        self.stagedlistView.setModel(stagedlistViewModel)

        # Model for staged Listview
        stagedlistViewModel = QtGui.QStandardItemModel(self.upperPane)
        for stagedMission in self.db.airMissionStatus.airMissionList.lst:
            item = QtGui.QStandardItem(stagedMission.name)
            item.setEditable(False)
            stagedlistViewModel.appendRow(item)
        self.stagedlistView.setModel(stagedlistViewModel)

        # Waypoint Comboboxes Content
        waypointComboBoxModel = QtGui.QStandardItemModel(self.upperPane)
        for waypoint in self.db.waypoints.lst:
            item = QtGui.QStandardItem(waypoint.name)
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

        # Signals
        self.missionTypeComboBox.currentIndexChanged.connect(lambda: self.checkMissionTypeComboBox())

        QtCore.QMetaObject.connectSlotsByName(self)

    # Prepend Button clicked_slot():
    def prependButtonAction(self):
        print('Prepend Button Pressed')
        print('List of Selected Mission')
        model = self.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))

    # Append Button clicked_slot():
    def appendButtonAction(self):
        print('Append Button Pressed')
        print('List of Selected Mission')
        model = self.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))

    def replaceButtonAction(self):
        print('Replace button Pressed')
        model = self.unstagedListView.model()

        #Find selected row
        print('Replace mission:')
        selectedIndexes = self.stagedlistView.selectedIndexes()
        if len(selectedIndexes) == 1:
            print(selectedIndexes[0].data())
        else:
            print('Select one and only one mission')
            return

        # Find Checkboxed Items
        print('List of Selected Missions')
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))

    def replaceAllButtonAction(self):
        print('replace all button pressed')
        print('List of Selected Missions')
        model = self.unstagedListView.model()

        # Find Checkboxed Items
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                print('Index %s with Mission: %s' % (item.row(), item.index().data()))


    def updateListViews(self):
        print("Needs to be completed")

    def sendMissionButtonAction(self):
        waypointOneName = self.waypointOneComboBox.currentText()
        missionType = self.missionTypeComboBox.currentText().lower()

        if missionType in [NavPattern.MISSION_SEGMENT.value, NavPattern.MISSION_PATH.value, NavPattern.MISSION_SURVEY.value]:
            waypointTwoName = self.waypointTwoComboBox.currentText()
            print('Waypoint 1: %s, Waypoint 2: %s, Mission Type: %s' % (waypointOneName, waypointTwoName, missionType))

        else:
            print('Waypoint 1: %s, Mission Type: %s' % (waypointOneName, missionType))

        # Create Mission Object. Add to missions database

    def checkMissionTypeComboBox(self):
        missionType = self.missionTypeComboBox.currentText().lower()
        if missionType in [NavPattern.MISSION_SEGMENT.value, NavPattern.MISSION_PATH.value, NavPattern.MISSION_SURVEY.value]:
            self.waypointTwoComboBox.setEnabled(True)
        else:
            self.waypointTwoComboBox.setEnabled(False)

    def updateListViews(self):
        print("Needs to be completed")

    # Used by Main Window Constructor
    def translateUi(self):
        self.setWindowTitle(translate("mainWindow", "Mission Commander"))
        self.derouteButton.setText(translate("mainWindow", "Quick Deroute"))
        self.sendMissionButton.setText(translate("mainWindow", "Send Mission"))
        self.uasWaypointsLabel.setText(translate("mainWindow", "Last UAS Waypoints"))
        self.ivyMessageTSLabel.setText(translate("mainWindow", "Last Ivy Message Timestamp"))
        self.interopFreqLabel.setText(translate("mainWindow", "Interoperability Frequency"))
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
