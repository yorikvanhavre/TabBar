#TabBar widget for FreeCAD
#Copyright (C) 2015, 2016  triplus @ FreeCAD
#
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


from PySide import QtCore


def singleInstance():
    from PySide import QtGui

    mw = FreeCADGui.getMainWindow()
    if mw:
        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "TabBar":
                i.deleteLater()

singleInstance()


def dockWidget():
    from PySide import QtGui
    from PySide import QtCore

    widget = QtGui.QDockWidget()
    widget.setWindowTitle("TabBar")
    widget.setObjectName("TabBar")
    mw = FreeCADGui.getMainWindow()
    if mw:
        mw.addDockWidget(QtCore.Qt.TopDockWidgetArea, widget)
    return widget

dockWidget()


def guiUp():
    from PySide import QtCore
    from PySide import QtGui
    import FlowLayout
    import InstallEvent

    noneIcon = ['16 16 3 1',
                ' 	c None',
                '.	c #CC0000',
                '+	c #204A87',
                '                ',
                ' ............   ',
                ' .              ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                '              + ',
                '   ++++++++++++ ',
                '                ']

    settingsIcon = ['16 16 2 1',
                    ' 	c None',
                    '.	c #888A85',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
                    '                ']

    indicatorBlue = ['16 16 2 1',
                     ' 	c None',
                     '.	c #204A87',
                     '                ',
                     '                ',
                     '                ',
                     '                ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '                ',
                     '                ',
                     '                ',
                     '                ']

    indicatorGray = ['16 16 2 1',
                     ' 	c None',
                     '.	c #888A85',
                     '                ',
                     '                ',
                     '                ',
                     '                ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '    ........    ',
                     '                ',
                     '                ',
                     '                ',
                     '                ']

    quickMenuStyle = ("padding: 5px")

    scrollStyle = ("""
        QScrollArea {
            border: none;
            background: transparent;
        }

        QScrollArea > QWidget > QWidget {
            border: none;
            background: transparent;
        }

        QScrollArea QToolButton {
            margin: 0;
            padding: 2px;
            padding-left: 4px;
            padding-right: 4px;
            border: 1px solid transparent;
            border-radius: 2px;
        }

        QScrollArea QToolButton#menuButton {
            padding-left: 1px;
            padding-right: 7px;
        }

        QScrollArea QToolButton:hover {
            border: 1px solid lightblue;
        }

        QScrollArea QToolButton:pressed {
            padding-left: 5px;
            padding-top: 3px;
        }

        QScrollArea QToolButton#menuButton:pressed {
            padding-left: 2px;
            padding-top: 3px;
        }

        QScrollArea QToolButton#menuButton::menu-button,
        QScrollArea QToolButton#menuButton::menu-indicator {
            margin: 0;
            padding: 0;
            border: none;
            background: transparent;
            width: 11px;
            height: 14px;
            subcontrol-origin: padding;
            subcontrol-position: bottom right;
        }
        """)

    def beforeStart():
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        paramGet.RemBool("AddRemove")

    beforeStart()

    def getSelectorActionGroup():
        mw = FreeCADGui.getMainWindow()
        paramGeneralGet = App.ParamGet("User parameter:BaseApp/Workbenches")

        actionList = {}
        for i in mw.findChildren(QtGui.QAction):
            actionList[i.objectName()] = i

        actionGroup = None

        if "NoneWorkbench" in actionList:
            actionGroup = actionList["NoneWorkbench"].parent()
        else:
            if paramGeneralGet.GetString("Enabled"):
                enabledList = (((paramGeneralGet.GetString("Enabled"))
                               .rsplit(',', 1)[0])
                               .split(","))
            else:
                enabledList = []

            tempActionList = []

            for i in mw.findChildren(QtGui.QAction):
                if i.objectName() in enabledList:
                    tempActionList.append(i)
                else:
                    pass

            actionGroup = tempActionList[0].parent()

        if actionGroup is None:
            actionGroup = QtGui.QActionGroup(mw)
        else:
            pass

        return actionGroup

    selectorActionGroup = getSelectorActionGroup()

    def getSelectorActionGroupAll():
        mw = FreeCADGui.getMainWindow()

        wbList = FreeCADGui.listWorkbenches()
        wbListSorted = sorted(wbList)

        selectorActionGroupAll = QtGui.QActionGroup(mw)

        for i in wbList:
            action = QtGui.QAction(selectorActionGroupAll)
            action.setObjectName(i)
            action.setCheckable(True)
            action.setText(wbList[i].MenuText)

            try:
                icon = wbIcon(wbList[i].Icon)
            except:
                icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

            action.setIcon(icon)

        activeWB = FreeCADGui.activeWorkbench().name()

        for i in selectorActionGroupAll.actions():
            if i.objectName() == activeWB:
                i.setChecked(True)
            else:
                pass

        return selectorActionGroupAll

    def xpmParse(i):
        icon = []
        for a in ((((i
                  .split('{', 1)[1])
                  .rsplit('}', 1)[0])
                  .strip())
                  .split("\n")):
            icon.append((a
                        .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        return icon

    def wbIcon(i):

        if str(i.find("XPM")) != "-1":
            icon = QtGui.QIcon(QtGui.QPixmap(xpmParse(i)))
        else:
            icon = QtGui.QIcon(QtGui.QPixmap(i))

        if icon.pixmap(QtCore.QSize(16, 16)).isNull():
            icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
        else:
            pass
        return icon

    def wbToolbars():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName() == "Std_ToolBarMenu":
                menu = i.menu()

        tempButton = QtGui.QPushButton(mw)
        tempButton.clicked.connect(menu.aboutToShow)
        tempButton.click()
        tempButton.deleteLater()

        toolbarList = []
        menuActions = menu.actions()
        for i in menuActions:
            if i.isEnabled():
                toolbarList.append(i.text())
        return toolbarList

    def findDockWidget():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "TabBar":
                dockWidget = i
        return dockWidget

    tbDock = findDockWidget()

    def tabWidget():
        widget = QtGui.QTabWidget()
        widget.tabBar().setDrawBase(False)
        widget.setMovable(True)
        return widget

    tbTabs = tabWidget()
    tbTabs.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)

    tbDockWidget = QtGui.QWidget()
    tbDockWidgetLayout = QtGui.QVBoxLayout()
    tbDockWidgetLayout.setContentsMargins(0, 1, 0, 0)
    tbDockWidget.setLayout(tbDockWidgetLayout)
    tbDockWidgetLayout.addWidget(tbTabs)
    tbDock.setWidget(tbDockWidget)

    tbDockTitleBar = tbDock.titleBarWidget()

    def tabPrefGeneral():
        groupTabStyle = QtGui.QGroupBox("Tab style:")
        layoutTabStyle = QtGui.QVBoxLayout()
        groupTabStyle.setLayout(layoutTabStyle)

        radioTabStyleDefault = QtGui.QRadioButton("Default")
        radioTabStyleIcon = QtGui.QRadioButton("Icon")
        radioTabStyleText = QtGui.QRadioButton("Text")

        layoutTabStyle.addWidget(radioTabStyleDefault)
        layoutTabStyle.addWidget(radioTabStyleIcon)
        layoutTabStyle.addWidget(radioTabStyleText)
        layoutTabStyle.addStretch(1)

        def onTabStyleDefault():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleDefault.isChecked():
                for i in xrange(tbTabs.count()):
                    try:
                        icon = wbIcon((FreeCADGui
                                      .getWorkbench(tbTabs.widget(i)
                                       .objectName())).Icon)
                    except:
                        icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                    tbTabs.setTabIcon(i, icon)
                    tbTabs.setTabText(i, tbTabs.widget(i).windowTitle())
                paramGet.SetString("TabStyle", "Default")
            else:
                pass

        radioTabStyleDefault.toggled.connect(onTabStyleDefault)

        def onTabStyleIcon():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleIcon.isChecked():
                for i in xrange(tbTabs.count()):
                    try:
                        icon = wbIcon((FreeCADGui
                                      .getWorkbench(tbTabs.widget(i)
                                       .objectName())).Icon)
                    except:
                        icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                    tbTabs.setTabText(i, "")
                    tbTabs.setTabIcon(i, icon)
                paramGet.SetString("TabStyle", "Icon")
            else:
                pass

        radioTabStyleIcon.toggled.connect(onTabStyleIcon)

        def onTabStyleText():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleText.isChecked():
                for i in xrange(tbTabs.count()):
                    tbTabs.setTabIcon(i, QtGui.QIcon())
                    tbTabs.setTabText(i, tbTabs.widget(i).windowTitle())
                paramGet.SetString("TabStyle", "Text")
            else:
                pass

        radioTabStyleText.toggled.connect(onTabStyleText)

        widgetGeneral = QtGui.QWidget()
        layoutGeneral = QtGui.QHBoxLayout()
        widgetGeneral.setLayout(layoutGeneral)

        layoutGeneralLeft = QtGui.QVBoxLayout()
        layoutGeneral.addLayout(layoutGeneralLeft)
        layoutGeneralLeft.addWidget(groupTabStyle)

        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        if paramGet.GetString("TabStyle"):
            if paramGet.GetString("TabStyle") == "Default":
                radioTabStyleDefault.setChecked(True)
            elif paramGet.GetString("TabStyle") == "Icon":
                radioTabStyleIcon.setChecked(True)
            elif paramGet.GetString("TabStyle") == "Text":
                radioTabStyleText.setChecked(True)
        else:
            radioTabStyleDefault.setChecked(True)

        return widgetGeneral

    def tabPrefToolbar():
        mw = FreeCADGui.getMainWindow()
        paramTBGet = App.ParamGet("User parameter:BaseApp/TabBar/Toolbars")

        activeWBLabel = QtGui.QLabel()
        menuText = Gui.activeWorkbench().MenuText
        activeWBLabel.setText(menuText.decode("UTF-8"))
        activeWBLabel.setWordWrap(1)
        activeWBLabel.setFrameStyle(QtGui.QFrame.StyledPanel)

        toolbarLocal = QtGui.QListWidget()
        toolbarLocal.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        def setActiveWB(activeWB):
            checkActiveWB = FreeCADGui.activeWorkbench().name()

            if checkActiveWB != activeWB:
                onSelector(activeWB)
            else:
                pass

        def activeWBLabelText():
            text = activeWBLabel.text()

            wbList = FreeCADGui.listWorkbenches()

            for i in wbList:
                if wbList[i].MenuText == text:
                    wbName = i

            return wbName

        def toolbarListLocal():
            activeWB = activeWBLabelText()
            setActiveWB(activeWB)

            paramActiveWBGet = paramTBGet.GetString(activeWB)

            if paramActiveWBGet:
                paramActiveWBGet = paramActiveWBGet.split(".,.")
            else:
                paramActiveWBGet = []

            paramTBOffGet = paramTBGet.GetString(activeWB + "-Off")

            if paramTBOffGet:
                paramTBOffGet = paramTBOffGet.split(".,.")
            else:
                paramTBOffGet = []

            toolbarList = wbToolbars()

            tbList = []
            for i in mw.findChildren(QtGui.QToolBar):
                if i.windowTitle() in toolbarList:
                    tbList.append(i)

            tbListObjectName = []
            for i in tbList:
                tbListObjectName.append(i.objectName())

            toolbarList = tbListObjectName

            for i in toolbarList:
                if i not in paramActiveWBGet:
                    paramActiveWBGet.append(i)
                else:
                    pass

            tbListAll = {}
            for i in mw.findChildren(QtGui.QToolBar):
                tbListAll[i.objectName()] = i

            toolbarLocal.blockSignals(True)

            delItem = toolbarLocal.takeItem(0)
            while delItem:
                delItem = toolbarLocal.takeItem(0)

            for i in paramActiveWBGet:
                item = QtGui.QListWidgetItem(toolbarLocal)

                if i in tbListObjectName:
                    item.setData(QtCore.Qt.UserRole, i)
                    for a in tbListAll:
                        if tbListAll[a].objectName() == i:
                            item.setText(tbListAll[a].windowTitle())

                elif i in tbListAll:
                    item.setData(QtCore.Qt.UserRole, i)
                    for a in tbListAll:
                        if tbListAll[a].objectName() == i:
                            item.setText(tbListAll[a].windowTitle())
                    item.setIcon(QtGui.QIcon(QtGui.QPixmap(indicatorBlue)))

                else:
                    item.setData(QtCore.Qt.UserRole, i)
                    item.setText(i)
                    item.setIcon(QtGui.QIcon(QtGui.QPixmap(indicatorGray)))

                item.setCheckState(QtCore.Qt.CheckState(2))

            items = []
            for index in xrange(toolbarLocal.count()):
                items.append(toolbarLocal.item(index))

            for i in items:
                if i.data(QtCore.Qt.UserRole) in paramTBOffGet:
                    i.setCheckState(QtCore.Qt.CheckState(0))
                else:
                    pass

            toolbarLocal.blockSignals(False)

        toolbarListLocal()

        def onToolbarListLocal():
            activeWB = activeWBLabelText()

            items = []
            for index in xrange(toolbarLocal.count()):
                items.append(toolbarLocal.item(index))

            checkList = []
            for i in items:
                if not i.checkState():
                    checkList.append(i.data(QtCore.Qt.UserRole))
                else:
                    pass

            paramTBGet.SetString(activeWB + "-Off", ".,.".join(checkList))

            onSelector(activeWB)

        toolbarLocal.itemChanged.connect(onToolbarListLocal)

        toolbarExternal = QtGui.QListWidget()
        toolbarExternal.setSortingEnabled(True)
        toolbarExternal.sortItems(QtCore.Qt.AscendingOrder)
        toolbarExternal.setHorizontalScrollBarPolicy(QtCore
                                                     .Qt.ScrollBarAlwaysOff)

        def toolbarListExternal():
            activeWB = activeWBLabelText()
            setActiveWB(activeWB)

            toolbarList = wbToolbars()

            tbList = []
            for i in mw.findChildren(QtGui.QToolBar):
                if i.windowTitle() not in toolbarList:
                    tbList.append(i)
                else:
                    pass

            paramTBExternalGet = paramTBGet.GetString(activeWB + "-External")

            toolbarExternalList = []
            if paramTBExternalGet:
                toolbarExternalList = paramTBExternalGet.split(".,.")
            else:
                toolbarExternalList = []

            toolbarExternal.blockSignals(True)

            delItem = toolbarExternal.takeItem(0)
            while delItem:
                delItem = toolbarExternal.takeItem(0)

            for i in tbList:
                item = QtGui.QListWidgetItem(toolbarExternal)
                item.setText(i.windowTitle())
                item.setCheckState(QtCore.Qt.CheckState(0))
                item.setData(QtCore.Qt.UserRole, i.objectName())
                item.setIcon(QtGui.QIcon(QtGui.QPixmap(indicatorBlue)))

            items = []
            for index in xrange(toolbarExternal.count()):
                items.append(toolbarExternal.item(index))

            for i in items:
                if i.data(QtCore.Qt.UserRole) in toolbarExternalList:
                    i.setCheckState(QtCore.Qt.CheckState(2))
                else:
                    pass

            toolbarExternal.blockSignals(False)

        toolbarListExternal()

        def onToolbarListExternal():
            activeWB = activeWBLabelText()
            setActiveWB(activeWB)

            items = []
            for index in xrange(toolbarExternal.count()):
                items.append(toolbarExternal.item(index))

            checkListOn = []
            checkListOff = []
            for i in items:
                if i.checkState():
                    checkListOn.append(i.data(QtCore.Qt.UserRole))
                else:
                    checkListOff.append(i.data(QtCore.Qt.UserRole))

            toolbarList = paramTBGet.GetString(activeWB)

            if toolbarList:
                toolbarList = toolbarList.split(".,.")
            else:
                toolbarList = wbToolbars()

                tbList = []
                for i in mw.findChildren(QtGui.QToolBar):
                    if i.windowTitle() in toolbarList:
                        tbList.append(i)

                tbListObjectName = []
                for i in tbList:
                    tbListObjectName.append(i.objectName())

                toolbarList = tbListObjectName

            for i in checkListOn:
                if i not in toolbarList:
                    toolbarList.append(i)
                else:
                    pass

            for i in checkListOff:
                if i in toolbarList:
                    toolbarList.remove(i)
                else:
                    pass

            paramTBGet.SetString(activeWB, ".,.".join(toolbarList))
            paramTBGet.SetString(activeWB + "-External",
                                 ".,.".join(checkListOn))

            toolbarListLocal()
            onSelector(activeWB)

        toolbarExternal.itemChanged.connect(onToolbarListExternal)

        selectorButton = QtGui.QToolButton()
        selectorButton.setAutoRaise(True)
        selectorButton.setPopupMode(QtGui.QToolButton
                                    .ToolButtonPopupMode.MenuButtonPopup)
        selectorMenu = QtGui.QMenu()
        selectorButton.setMenu(selectorMenu)
        selectorList = sorted(FreeCADGui.listWorkbenches())

        selectorActions = {}
        for i in getSelectorActionGroupAll().actions():
            selectorActions[i.objectName()] = i

        selectorGroup = QtGui.QActionGroup(selectorMenu)

        defaultAction = QtGui.QAction(selectorMenu)
        selectorButton.setDefaultAction(defaultAction)

        for i in selectorList:
            if i in selectorActions:
                selectorAction = QtGui.QAction(selectorGroup)
                selectorAction.setIcon(selectorActions[i].icon())
                selectorAction.setText(selectorActions[i].text())
                selectorAction.setObjectName(selectorActions[i].objectName())
                selectorAction.setCheckable(True)
                selectorMenu.addAction(selectorAction)
                if selectorActions[i].isChecked():
                    selectorAction.setChecked(True)
                    defaultAction.setIcon(selectorGroup.checkedAction().icon())
                    selectorButton.setDefaultAction(defaultAction)
                else:
                    pass
            else:
                pass

        def onSelectorGroup():
            menuText = selectorGroup.checkedAction().text()
            activeWBLabel.setText(menuText.decode("UTF-8"))
            defaultAction.setIcon(selectorGroup.checkedAction().icon())
            toolbarListLocal()
            toolbarListExternal()

        selectorGroup.triggered.connect(onSelectorGroup)

        buttonLeft = QtGui.QToolButton()
        buttonLeft.setArrowType(QtCore.Qt.LeftArrow)

        buttonRight = QtGui.QToolButton()
        buttonRight.setArrowType(QtCore.Qt.RightArrow)

        buttonUp = QtGui.QToolButton()
        buttonUp.setArrowType(QtCore.Qt.ArrowType(1))

        buttonDown = QtGui.QToolButton()
        buttonDown.setArrowType(QtCore.Qt.DownArrow)

        buttonLocalReset = QtGui.QToolButton()
        buttonLocalReset.setText(u'\u27F3')

        buttonExternalGetAll = QtGui.QToolButton()
        buttonExternalGetAll.setText(u'\u26C1')

        buttonSelectorToggle = QtGui.QToolButton()

        def onButtonLeft():
            tbTabs.setCurrentIndex(tbTabs.currentIndex() - 1)
            menuText = Gui.activeWorkbench().MenuText
            activeWBLabel.setText(menuText.decode("UTF-8"))
            toolbarListLocal()
            toolbarListExternal()
            for i in selectorGroup.actions():
                if i.text() == menuText:
                    i.setChecked(True)
                    onSelectorGroup()
                else:
                    pass

        buttonLeft.clicked.connect(onButtonLeft)

        def onButtonRight():
            tbTabs.setCurrentIndex(tbTabs.currentIndex() + 1)
            menuText = Gui.activeWorkbench().MenuText
            activeWBLabel.setText(menuText.decode("UTF-8"))
            toolbarListLocal()
            toolbarListExternal()
            for i in selectorGroup.actions():
                if i.text() == menuText:
                    i.setChecked(True)
                    onSelectorGroup()
                else:
                    pass

        buttonRight.clicked.connect(onButtonRight)

        def onButtonUp():
            activeWB = activeWBLabelText()
            currentIndex = toolbarLocal.currentRow()

            if currentIndex != 0:
                currentItem = toolbarLocal.takeItem(currentIndex)
                toolbarLocal.insertItem(currentIndex - 1, currentItem)
                toolbarLocal.setCurrentRow(currentIndex - 1)

                items = []
                for index in xrange(toolbarLocal.count()):
                    items.append(toolbarLocal.item(index))

                toolbarData = []
                for i in items:
                    toolbarData.append(i.data(QtCore.Qt.UserRole))

                paramTBGet.SetString(activeWB, ".,.".join(toolbarData))

                onSelector(activeWB)
            else:
                pass

        buttonUp.clicked.connect(onButtonUp)

        def onButtonDown():
            activeWB = activeWBLabelText()
            currentIndex = toolbarLocal.currentRow()

            if currentIndex != toolbarLocal.count() - 1:
                currentItem = toolbarLocal.takeItem(currentIndex)
                toolbarLocal.insertItem(currentIndex + 1, currentItem)
                toolbarLocal.setCurrentRow(currentIndex + 1)

                items = []
                for index in xrange(toolbarLocal.count()):
                    items.append(toolbarLocal.item(index))

                toolbarData = []
                for i in items:
                    toolbarData.append(i.data(QtCore.Qt.UserRole))

                paramTBGet.SetString(activeWB, ".,.".join(toolbarData))

                onSelector(activeWB)
            else:
                pass

        buttonDown.clicked.connect(onButtonDown)

        def onButtonLocalReset():
            activeWB = activeWBLabelText()
            setActiveWB(activeWB)

            paramTBGet.RemString(activeWB)
            paramTBGet.RemString(activeWB + "-Off")
            paramTBGet.RemString(activeWB + "-External")

            toolbarListLocal()
            toolbarListExternal()
            onSelector(activeWB)

        buttonLocalReset.clicked.connect(onButtonLocalReset)

        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        def onButtonExternalGetAll():
            activeWB = FreeCADGui.activeWorkbench().name()

            progressBar = QtGui.QProgressBar(activeWBLabel)
            progressBar.setMinimumSize(activeWBLabel.size())

            progressBar.show()

            wbList = []
            for i in FreeCADGui.listWorkbenches():
                wbList.append(i)

            wbList.remove(activeWB)

            progressBar.setMaximum(len(wbList))

            n = 0
            for i in wbList:
                n = n + 1
                progressBar.setValue(n)
                FreeCADGui.activateWorkbench(i)

            FreeCADGui.activateWorkbench(activeWB)

            progressBar.hide()
            progressBar.deleteLater()

            toolbarListLocal()
            toolbarListExternal()
            onSelector(activeWB)

        buttonExternalGetAll.clicked.connect(onButtonExternalGetAll)

        def onToggleButton():
            if toolbarExternal.isHidden():
                toolbarExternal.show()
                buttonExternalGetAll.show()
                buttonSelectorToggle.setArrowType(QtCore.Qt.RightArrow)
                paramGet.SetBool("ToggleExternal", 1)
            else:
                toolbarExternal.hide()
                buttonExternalGetAll.hide()
                buttonSelectorToggle.setArrowType(QtCore.Qt.LeftArrow)
                paramGet.SetBool("ToggleExternal", 0)

        buttonSelectorToggle.clicked.connect(onToggleButton)

        if paramGet.GetBool("ToggleExternal"):
            buttonSelectorToggle.setArrowType(QtCore.Qt.RightArrow)
        else:
            toolbarExternal.hide()
            buttonExternalGetAll.hide()
            buttonSelectorToggle.setArrowType(QtCore.Qt.LeftArrow)

        layoutLabel = QtGui.QHBoxLayout()
        layoutLabel.addWidget(activeWBLabel)
        layoutLabel.addWidget(selectorButton)
        layoutLabel.addWidget(buttonLeft)
        layoutLabel.addWidget(buttonRight)

        layoutToolbarList = QtGui.QHBoxLayout()
        layoutToolbarList.addWidget(toolbarLocal)
        layoutToolbarList.addWidget(toolbarExternal)

        layoutButtons = QtGui.QHBoxLayout()
        layoutButtons.addWidget(buttonLocalReset)
        layoutButtons.addWidget(buttonDown)
        layoutButtons.addWidget(buttonUp)
        layoutButtons.addStretch(1)
        layoutButtons.addWidget(buttonExternalGetAll)
        layoutButtons.addWidget(buttonSelectorToggle)

        layoutToolbar = QtGui.QVBoxLayout()
        layoutToolbar.insertLayout(0, layoutLabel)
        layoutToolbar.insertLayout(1, layoutToolbarList)
        layoutToolbar.insertLayout(2, layoutButtons)

        widgetToolbar = QtGui.QWidget()
        widgetToolbar.setLayout(layoutToolbar)

        return widgetToolbar

    def tabPrefSelector():
        mw = FreeCADGui.getMainWindow()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        paramGeneralGet = App.ParamGet("User parameter:BaseApp/Workbenches")

        selectorList = QtGui.QListWidget()
        selectorList.setIconSize(QtCore.QSize(20, 20))
        selectorList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        def makeSelectorList():
            selectorList.blockSignals(True)
            selectorList.setSortingEnabled(False)

            def addItem(a, b):

                listOff = paramGet.GetString("SelectorList-Off")
                listOff = listOff.split(".,.")

                item = QtGui.QListWidgetItem(selectorList)
                item.setText(a.MenuText)
                item.setData(QtCore.Qt.UserRole, b)

                if paramGet.GetString("SelectorMode") == "Custom":
                    if b in listOff:
                        item.setCheckState(QtCore.Qt.CheckState(0))
                    else:
                        item.setCheckState(QtCore.Qt.CheckState(2))
                else:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                    item.setCheckState(QtCore.Qt.CheckState(2))

                try:
                    icon = wbIcon(a.Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                item.setIcon(icon)

            def sortedList():
                selectorList.clear()

                wbList = FreeCADGui.listWorkbenches()
                selectorList.setSortingEnabled(True)
                selectorList.sortItems(QtCore.Qt.AscendingOrder)

                for i in wbList:
                    addItem(wbList[i], i)

            if paramGet.GetString("SelectorMode") == "Default":
                if paramGeneralGet.GetString("Enabled"):
                    listEnabled = (((paramGeneralGet.GetString("Enabled"))
                                   .rsplit(',', 1)[0])
                                   .split(","))

                    tempWBList = FreeCADGui.listWorkbenches()

                    selectorList.clear()

                    for i in listEnabled:
                        if i in tempWBList:
                            addItem(tempWBList[i], i)
                        else:
                            pass

                else:
                    wbList = sortedList()

            elif paramGet.GetString("SelectorMode") == "Custom":
                if paramGet.GetString("SelectorList"):
                    listCustom = paramGet.GetString("SelectorList")
                    listCustom = listCustom.split(".,.")

                    tempWBList = FreeCADGui.listWorkbenches()

                    selectorList.clear()

                    for i in listCustom:
                        if i in tempWBList:
                            addItem(tempWBList[i], i)
                        else:
                            pass

                else:
                    sortedList()
            else:
                sortedList()

            selectorList.blockSignals(False)

        def onMakeSelectorList():
            activeWB = FreeCADGui.activeWorkbench().name()

            items = []
            for index in xrange(selectorList.count()):
                items.append(selectorList.item(index))

            checkListOff = []
            for i in items:
                if not i.checkState():
                    checkListOff.append(i.data(QtCore.Qt.UserRole))
                else:
                    pass

            if checkListOff:
                data = ".,.".join(checkListOff)
                paramGet.SetString("SelectorList-Off", data)
            else:
                pass

            tbTabs.blockSignals(True)
            tbTabs.clear()
            tbTabs.blockSignals(False)

            onSelector(activeWB, mode=1)

        selectorList.itemChanged.connect(onMakeSelectorList)

        selectorModeGroup = QtGui.QGroupBox("Mode:")

        radioSelectorDefault = QtGui.QRadioButton("Default")
        radioSelectorCustom = QtGui.QRadioButton("Custom")

        buttonSelectorUp = QtGui.QToolButton()
        buttonSelectorUp.setArrowType(QtCore.Qt.ArrowType(1))

        buttonSelectorDown = QtGui.QToolButton()
        buttonSelectorDown.setArrowType(QtCore.Qt.DownArrow)

        buttonSelectorReset = QtGui.QToolButton()
        buttonSelectorReset.setText(u'\u27F3')

        buttonSelectorToggle = QtGui.QToolButton()

        def onRadioSelectorDefault():
            activeWB = FreeCADGui.activeWorkbench().name()

            buttonSelectorUp.setEnabled(False)
            buttonSelectorDown.setEnabled(False)
            buttonSelectorReset.setEnabled(False)

            paramGet.SetString("SelectorMode", "Default")

            tbTabs.blockSignals(True)
            tbTabs.clear()
            tbTabs.blockSignals(False)

            makeSelectorList()

            onSelector(activeWB, mode=1)

        radioSelectorDefault.clicked.connect(onRadioSelectorDefault)

        def onRadioSelectorCustom():
            activeWB = FreeCADGui.activeWorkbench().name()

            buttonSelectorUp.setEnabled(True)
            buttonSelectorDown.setEnabled(True)
            buttonSelectorReset.setEnabled(True)

            paramGet.SetString("SelectorMode", "Custom")

            tbTabs.blockSignals(True)
            tbTabs.clear()
            tbTabs.blockSignals(False)

            makeSelectorList()

            onSelector(activeWB, mode=1)

        radioSelectorCustom.clicked.connect(onRadioSelectorCustom)

        def onButtonSelectorUp():
            activeWB = FreeCADGui.activeWorkbench().name()
            currentIndex = selectorList.currentRow()

            selectorList.setSortingEnabled(False)
            if currentIndex != 0:
                currentItem = selectorList.takeItem(currentIndex)
                selectorList.insertItem(currentIndex - 1, currentItem)
                selectorList.setCurrentRow(currentIndex - 1)

                items = []
                for index in xrange(selectorList.count()):
                    items.append(selectorList.item(index))

                selectorListData = []
                for i in items:
                    selectorListData.append(i.data(QtCore.Qt.UserRole))

                data = ".,.".join(selectorListData)
                paramGet.SetString("SelectorList", data)

                tbTabs.blockSignals(True)
                tbTabs.clear()
                tbTabs.blockSignals(False)

                onSelector(activeWB, mode=1)
            else:
                pass

        buttonSelectorUp.clicked.connect(onButtonSelectorUp)

        def onButtonSelectorDown():
            activeWB = FreeCADGui.activeWorkbench().name()
            currentIndex = selectorList.currentRow()

            selectorList.setSortingEnabled(False)
            if currentIndex != selectorList.count() - 1:
                currentItem = selectorList.takeItem(currentIndex)
                selectorList.insertItem(currentIndex + 1, currentItem)
                selectorList.setCurrentRow(currentIndex + 1)

                items = []
                for index in xrange(selectorList.count()):
                    items.append(selectorList.item(index))

                selectorListData = []
                for i in items:
                    selectorListData.append(i.data(QtCore.Qt.UserRole))

                data = ".,.".join(selectorListData)
                paramGet.SetString("SelectorList", data)

                tbTabs.blockSignals(True)
                tbTabs.clear()
                tbTabs.blockSignals(False)

                onSelector(activeWB, mode=1)
            else:
                pass

        buttonSelectorDown.clicked.connect(onButtonSelectorDown)

        def onButtonSelectorReset():
            activeWB = FreeCADGui.activeWorkbench().name()
            paramGet.RemString("SelectorList")
            paramGet.RemString("SelectorList-Off")
            makeSelectorList()

            tbTabs.blockSignals(True)
            tbTabs.clear()
            tbTabs.blockSignals(False)

            onSelector(activeWB, mode=1)

        buttonSelectorReset.clicked.connect(onButtonSelectorReset)

        def onButtonSelectorToggle():
            if selectorModeGroup.isHidden():
                selectorModeGroup.show()
                paramGet.SetBool("ToggleSelector", 1)
                buttonSelectorToggle.setArrowType(QtCore.Qt.RightArrow)
            else:
                selectorModeGroup.hide()
                paramGet.SetBool("ToggleSelector", 0)
                buttonSelectorToggle.setArrowType(QtCore.Qt.LeftArrow)

        buttonSelectorToggle.clicked.connect(onButtonSelectorToggle)

        if paramGet.GetBool("ToggleSelector"):
            buttonSelectorToggle.setArrowType(QtCore.Qt.RightArrow)
        else:
            selectorModeGroup.hide()
            buttonSelectorToggle.setArrowType(QtCore.Qt.LeftArrow)

        selectorModeGroupLayout = QtGui.QVBoxLayout()
        selectorModeGroup.setLayout(selectorModeGroupLayout)

        selectorModeGroupLayout.addWidget(radioSelectorDefault)
        selectorModeGroupLayout.addWidget(radioSelectorCustom)
        selectorModeGroupLayout.addStretch(1)

        selectorLayoutMain = QtGui.QHBoxLayout()
        selectorLayoutMain.addWidget(selectorList)
        selectorLayoutMain.addWidget(selectorModeGroup)

        selectorLayoutButtons = QtGui.QHBoxLayout()
        selectorLayoutButtons.addWidget(buttonSelectorReset)
        selectorLayoutButtons.addWidget(buttonSelectorDown)
        selectorLayoutButtons.addWidget(buttonSelectorUp)
        selectorLayoutButtons.addStretch(1)
        selectorLayoutButtons.addWidget(buttonSelectorToggle)

        widgetSelector = QtGui.QWidget()
        widgetSelectorLayout = QtGui.QVBoxLayout()
        widgetSelector.setLayout(widgetSelectorLayout)

        widgetSelectorLayout.insertLayout(0, selectorLayoutMain)
        widgetSelectorLayout.insertLayout(1, selectorLayoutButtons)

        if paramGet.GetString("SelectorMode") == "Custom":
            radioSelectorCustom.setChecked(True)
            makeSelectorList()
        else:
            radioSelectorDefault.setChecked(True)
            makeSelectorList()

        return widgetSelector

    def tabPrefAutoload():
        wbList = QtGui.QListWidget()
        wbList.setIconSize(QtCore.QSize(20, 20))
        wbList.setSortingEnabled(True)
        wbList.sortItems(QtCore.Qt.AscendingOrder)
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        wbList.setHorizontalScrollBarPolicy(QtCore
                                            .Qt.ScrollBarAlwaysOff)

        paramGenGet = App.ParamGet("User parameter"
                                   ":BaseApp/Preferences/General")

        autoLoadModule = paramGenGet.GetString("AutoloadModule")

        if not autoLoadModule:
            autoLoadModule = "StartWorkbench"
        else:
            pass

        def workbenchList():
            listWorkbenches = FreeCADGui.listWorkbenches()

            for i in listWorkbenches:
                item = QtGui.QListWidgetItem(wbList)

                try:
                    icon = wbIcon(listWorkbenches[i].Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                item.setIcon(icon)

                if i == autoLoadModule:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                    item.setText(listWorkbenches[i].MenuText)
                    item.setCheckState(QtCore.Qt.CheckState(2))
                else:
                    item.setFlags(item.flags())
                    item.setText(listWorkbenches[i].MenuText)
                    item.setCheckState(QtCore.Qt.CheckState(0))

            modulesList = (paramGet.GetString("LoadModules")).split(",")

            autoLoad = []
            for i in modulesList:
                if i in listWorkbenches:
                    autoLoad.append(listWorkbenches[i].MenuText)

            item = []
            for i in xrange(wbList.count()):
                item.append(wbList.item(i))

            for i in item:
                if i.text() in autoLoad:
                    i.setCheckState(QtCore.Qt.CheckState(2))

        workbenchList()

        def onWorkbenchList():
            listWorkbenches = FreeCADGui.listWorkbenches()

            item = []
            for i in xrange(wbList.count()):
                item.append(wbList.item(i))

            checkList = []
            for i in item:
                if i.checkState():
                    checkList.append(i.text())

            autoLoad = []
            for i in listWorkbenches:
                if listWorkbenches[i].MenuText in checkList:
                    autoLoad.append(i)

            paramGet.SetString("LoadModules", ",".join(autoLoad))

        wbList.itemChanged.connect(onWorkbenchList)

        layoutAutoload = QtGui.QVBoxLayout()
        layoutAutoload.addWidget(wbList)

        widgetAutoload = QtGui.QWidget()
        widgetAutoload.setLayout(layoutAutoload)

        return widgetAutoload

    def onControl():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDialog):
            if i.objectName() == "tbPreferences":
                i.deleteLater()

        tbPrefDialog = QtGui.QDialog(mw)
        tbPrefDialog.resize(600, 400)
        tbPrefDialog.setObjectName("tbPreferences")
        tbPrefDialog.setWindowTitle("TabBar")
        tbPrefDialogLayout = QtGui.QVBoxLayout()
        tbPrefDialog.setLayout(tbPrefDialogLayout)
        tbPrefDialog.show()

        tbPrefTabs = QtGui.QTabWidget()
        tbPrefDialogLayout.addWidget(tbPrefTabs)

        tbPrefTabs.addTab(tabPrefGeneral(), "General")
        tbPrefTabs.addTab(tabPrefToolbar(), "Toolbar")
        tbPrefTabs.addTab(tabPrefSelector(), "Selector")
        tbPrefTabs.addTab(tabPrefAutoload(), "Autoload")

    def quickMenu():
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        menu = QtGui.QMenu()
        menu.setStyleSheet(quickMenuStyle)

        lockAction = QtGui.QAction(menu)
        lockAction.setIconText("Lock")
        lockAction.setCheckable(True)

        radioTop = QtGui.QRadioButton("Top")
        radioActionTop = QtGui.QWidgetAction(menu)
        radioActionTop.setDefaultWidget(radioTop)

        radioBottom = QtGui.QRadioButton("Bottom")
        radioActionBottom = QtGui.QWidgetAction(menu)
        radioActionBottom.setDefaultWidget(radioBottom)

        radioLeft = QtGui.QRadioButton("Left")
        radioActionLeft = QtGui.QWidgetAction(menu)
        radioActionLeft.setDefaultWidget(radioLeft)

        radioRight = QtGui.QRadioButton("Right")
        radioActionRight = QtGui.QWidgetAction(menu)
        radioActionRight.setDefaultWidget(radioRight)

        prefAction = QtGui.QAction(menu)
        prefAction.setIconText("Preferences")
        prefButton = QtGui.QToolButton()
        prefButton.setDefaultAction(prefAction)
        prefButtonAction = QtGui.QWidgetAction(menu)
        prefButtonAction.setDefaultWidget(prefButton)

        menu.addAction(lockAction)
        menu.addSeparator()
        menu.addAction(radioActionTop)
        menu.addAction(radioActionBottom)
        menu.addAction(radioActionLeft)
        menu.addAction(radioActionRight)
        menu.addSeparator()
        menu.addAction(prefButtonAction)

        menuButton = QtGui.QToolButton()
        menuButton.setMenu(menu)
        menuButton.setAutoRaise(True)
        menuButton.setIcon(QtGui.QIcon(QtGui.QPixmap(settingsIcon)))
        menuButton.setPopupMode(QtGui.QToolButton
                                .ToolButtonPopupMode.InstantPopup)

        def toTop():
            if radioTop.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.North)
                paramGet.SetString("Position", "North")
            else:
                pass

        radioTop.toggled.connect(toTop)

        def toBottom():
            if radioBottom.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.South)
                paramGet.SetString("Position", "South")
            else:
                pass

        radioBottom.toggled.connect(toBottom)

        def toLeft():
            if radioLeft.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.West)
                paramGet.SetString("Position", "West")
            else:
                pass

        radioLeft.toggled.connect(toLeft)

        def toRight():
            if radioRight.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.East)
                paramGet.SetString("Position", "East")
            else:
                pass

        radioRight.toggled.connect(toRight)

        def onLockToggle():
            if lockAction.isChecked():
                tbDock.setTitleBarWidget(QtGui.QWidget(None))
                paramGet.SetBool("Lock", 1)
            else:
                tbDock.setTitleBarWidget(tbDockTitleBar)
                paramGet.SetBool("Lock", 0)

        lockAction.changed.connect(onLockToggle)

        prefButton.clicked.connect(onControl)

        def onOpen():
            if paramGet.GetString("Position"):
                if paramGet.GetString("Position") == "North":
                    radioTop.setChecked(True)
                elif paramGet.GetString("Position") == "South":
                    radioBottom.setChecked(True)
                elif paramGet.GetString("Position") == "West":
                    radioLeft.setChecked(True)
                elif paramGet.GetString("Position") == "East":
                    radioRight.setChecked(True)
            else:
                radioTop.setChecked(True)

            if paramGet.GetBool("Lock"):
                lockAction.setChecked(True)
            else:
                lockAction.setChecked(False)

        menu.aboutToShow.connect(onOpen)

        onOpen()

        return menuButton

    def tabsList(activeWB):
        mw = FreeCADGui.getMainWindow()
        wbList = FreeCADGui.listWorkbenches()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        paramWBGet = App.ParamGet("User parameter:BaseApp/Workbenches")
        paramGen = App.ParamGet("User parameter:BaseApp/Preferences/General")

        if paramGet.GetString("SelectorMode") == "Custom":
            sortedWBList = paramGet.GetString("SelectorList")

            if sortedWBList:
                sortedWBList = sortedWBList.split(".,.")
            else:
                unsortedWBList = []
                for i in wbList:
                    unsortedWBList.append(i)
                sortedWBList = sorted(unsortedWBList)

            wbListOff = paramGet.GetString("SelectorList-Off")

            if wbListOff:
                wbListOff = wbListOff.split(".,.")
                for i in wbListOff:
                    if i in sortedWBList:
                        sortedWBList.remove(i)
                    else:
                        pass
            else:
                pass

        else:
            unsortedWBList = []
            for i in wbList:
                unsortedWBList.append(i)

            sortedWBList = sorted(unsortedWBList)

            if paramWBGet.GetString("Disabled"):
                disabledList = (((paramWBGet.GetString("Disabled"))
                                .rsplit(',', 1)[0])
                                .split(","))
                for i in disabledList:
                    if i in sortedWBList:
                        sortedWBList.remove(i)
                    else:
                        pass
            else:
                pass

            if paramWBGet.GetString("Enabled"):
                tempWBList = []
                enabledList = (((paramWBGet.GetString("Enabled"))
                               .rsplit(',', 1)[0])
                               .split(","))
                for i in enabledList:
                    if i in sortedWBList:
                        tempWBList.append(i)
                    else:
                        pass

                sortedWBList = tempWBList
            else:
                pass

        if activeWB not in sortedWBList:
            sortedWBList.append(activeWB)
            paramGet.SetBool("AddRemove", 1)
        else:
            paramGet.SetBool("AddRemove", 0)

        return sortedWBList

    def removeTabs(WorkbenchName):
        sortedWBList = tabsList(WorkbenchName)

        tbTabsList = {}
        for i in xrange(tbTabs.count()):
            a = tbTabs.widget(i).objectName()
            b = tbTabs.indexOf(tbTabs.widget(i))
            tbTabsList[a] = b

        for i in tbTabsList:
            if i not in sortedWBList:
                tbTabs.blockSignals(True)
                tbTabs.removeTab(tbTabsList[i])
                tbTabs.blockSignals(True)
            else:
                pass

    def addTabs(WorkbenchName):
        sortedWBList = tabsList(WorkbenchName)
        wbList = FreeCADGui.listWorkbenches()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        paramGen = App.ParamGet("User parameter:BaseApp/Preferences/General")

        tbTabsList = []
        for i in xrange(tbTabs.count()):
            tbTabsList.append(tbTabs.widget(i).objectName())

        tbTabs.blockSignals(True)

        for i in sortedWBList:
            if i in wbList and i not in tbTabsList:
                widget = QtGui.QWidget()
                widget.setObjectName(i)
                layout = FlowLayout.FlowLayout()
                layout.setObjectName(i)
                widget.setLayout(layout)
                widget.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                     QtGui.QSizePolicy.Ignored)
                scroll = QtGui.QScrollArea()
                scroll.setStyleSheet(scrollStyle)
                scroll.setObjectName(i)
                scroll.setWindowTitle(wbList[i].MenuText)
                scroll.setWidgetResizable(True)
                scroll.setVerticalScrollBarPolicy((QtCore.Qt
                                                  .ScrollBarAlwaysOff))
                scroll.setHorizontalScrollBarPolicy((QtCore.Qt
                                                    .ScrollBarAlwaysOff))
                scroll.setWidget(widget)

                try:
                    icon = wbIcon(wbList[i].Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                if paramGet.GetString("TabStyle"):
                    if paramGet.GetString("TabStyle") == "Default":
                        tbTabs.addTab(scroll, icon, wbList[i].MenuText)
                    elif paramGet.GetString("TabStyle") == "Icon":
                        tbTabs.addTab(scroll, icon, "")
                    elif paramGet.GetString("TabStyle") == "Text":
                        tbTabs.addTab(scroll, wbList[i].MenuText)
                else:
                    tbTabs.addTab(scroll, icon, wbList[i].MenuText)

                tbTabs.setTabToolTip(tbTabs.indexOf(scroll), wbList[i].ToolTip)
            else:
                pass

        if tbTabs.count() == 0:
            widget = QtGui.QWidget()
            layout = FlowLayout.FlowLayout()
            widget.setLayout(layout)

            try:
                FreeCADGui.activateWorkbench("NoneWorkbench")
            except:
                pass

            icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
            iconSize = paramGen.GetInt("ToolbarIconSize")

            if not iconSize:
                iconSize = 24
            else:
                pass

            tbTabs.addTab(widget, icon, "None")
            quickMenuButton = quickMenu()
            quickMenuButton.setIconSize(QtCore.QSize(iconSize, iconSize))
            layout.addWidget(quickMenuButton)
        else:
            pass

        tbTabs.blockSignals(False)

    def onSelector(WorkbenchName, mode=0):
        mw = FreeCADGui.getMainWindow()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        if WorkbenchName is "None":
            pass
        else:
            if mode == 0:
                currentAction = None
                activeWB = FreeCADGui.activeWorkbench()

                if activeWB.name() != WorkbenchName:
                    for i in selectorActionGroup.actions():
                        if i.objectName() == WorkbenchName:
                            currentAction = i
                        else:
                            pass

                    if currentAction is not None:
                        currentAction.trigger()
                    else:
                        FreeCADGui.doCommand((str('Gui.activateWorkbench("'
                                                  + WorkbenchName + '")')))
                else:
                    pass
            else:
                pass

            scrollList = []
            for i in xrange(tbTabs.count()):
                scrollList.append(tbTabs.widget(i).objectName())

            if paramGet.GetBool("AddRemove"):
                removeTabs(WorkbenchName)
            else:
                pass

            if WorkbenchName not in scrollList:
                addTabs(WorkbenchName)
            else:
                pass

            scrollList = []
            for i in tbTabs.findChildren(QtGui.QScrollArea):
                scrollList.append(i)

            for i in scrollList:
                if i.objectName() == WorkbenchName:
                    tbTabs.blockSignals(True)
                    tbTabs.setCurrentIndex(tbTabs.indexOf(i))
                    tbTabs.blockSignals(False)
                else:
                    pass

        onTabChange(WorkbenchName)

    def onTabChange(activeWB):
        mw = FreeCADGui.getMainWindow()
        paramTBGet = App.ParamGet("User parameter:BaseApp/TabBar/Toolbars")
        paramGen = App.ParamGet("User parameter:BaseApp/Preferences/General")

        activeTab = tbTabs.currentWidget().objectName()

        iconSize = paramGen.GetInt("ToolbarIconSize")

        if not iconSize:
            iconSize = 24

        for i in tbTabs.findChildren(QtGui.QLayout):
            if i.objectName() == activeTab:
                layout = i
            else:
                pass

        if not layout:
            layout = FlowLayout.FlowLayout()
        else:
            pass

        item = layout.takeAt(0)
        while item:
            item.widget().hide()
            del item
            item = layout.takeAt(0)

        toolbarList = wbToolbars()

        toolbarAll = {}
        for i in mw.findChildren(QtGui.QToolBar):
            toolbarAll[i.windowTitle()] = i

        toolbarObjectNameList = []
        for i in toolbarList:
            if i in toolbarAll:
                toolbarObjectNameList.append(toolbarAll[i].objectName())

        toolbarSortedList = []
        toolbarSortedList = paramTBGet.GetString(activeWB)
        toolbarSortedList = toolbarSortedList.split(".,.")

        for i in toolbarObjectNameList:
            if i not in toolbarSortedList:
                toolbarSortedList.append(i)
            else:
                pass

        toolbarOffList = []
        toolbarOffList = paramTBGet.GetString(activeWB + "-Off")
        toolbarOffList = toolbarOffList.split(".,.")

        for i in toolbarOffList:
            if i in toolbarSortedList:
                toolbarSortedList.remove(i)
            else:
                pass

        tbObjectNameAll = {}
        for i in mw.findChildren(QtGui.QToolBar):
            tbObjectNameAll[i.objectName()] = i

        toolbarButtons = []
        if "Workbench" not in toolbarSortedList:
                selectorButton = QtGui.QToolButton()
                selectorButton.setObjectName("WorkbenchSelector")
                toolbarButtons.append(selectorButton)
        else:
            pass

        for a in toolbarSortedList:
            if a in tbObjectNameAll:
                if a == "Workbench":
                    selectorButton = QtGui.QToolButton()
                    selectorButton.setObjectName("WorkbenchSelector")
                    toolbarButtons.append(selectorButton)
                else:
                    pass

                for b in tbObjectNameAll[a].findChildren(QtGui.QToolButton):
                    try:
                        if not b.defaultAction().isSeparator():
                            toolbarButtons.append(b)
                        else:
                            pass
                    except:
                        pass

        def workbenchSelector():
            selectorButton = QtGui.QToolButton()
            selectorMenu = QtGui.QMenu()
            selectorButton.setMenu(selectorMenu)
            selectorButton.setIconSize(QtCore.QSize(iconSize, iconSize))
            selectorButton.setPopupMode(QtGui.QToolButton
                                        .ToolButtonPopupMode.InstantPopup)
            layout.addWidget(selectorButton)

            wbList = FreeCADGui.listWorkbenches()
            wbListSorted = sorted(wbList)

            selectorActions = {}
            selectorGroup = QtGui.QActionGroup(selectorMenu)
            for i in wbList:
                action = QtGui.QAction(selectorGroup)
                action.setObjectName(i)
                action.setCheckable(True)
                action.setText(wbList[i].MenuText)

                try:
                    icon = wbIcon(wbList[i].Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                action.setIcon(icon)

                selectorActions[action.objectName()] = action

            for i in wbListSorted:
                if i in selectorActions:
                    selectorMenu.addAction(selectorActions[i])
                else:
                    pass

            for i in selectorGroup.actions():
                if i.objectName() == activeWB:
                    i.setChecked(True)
                    selectorButton.setDefaultAction(i)
                else:
                    pass

            def onSelectorGroup():

                if selectorGroup.checkedAction():
                    onSelector(selectorGroup.checkedAction().objectName())
                else:
                    pass

            selectorGroup.triggered.connect(onSelectorGroup)

        def buttonAdd(i):

            if i.objectName() == "WorkbenchSelector":
                workbenchSelector()

            elif i.menu() is None:
                toolButton = QtGui.QToolButton()
                toolButton.setAutoRaise(i.autoRaise())
                toolButton.setDefaultAction(i.defaultAction())
                toolButton.setIconSize(QtCore.QSize(iconSize, iconSize))
                toolButton.installEventFilter((InstallEvent
                                              .InstallEvent(toolButton)))
                layout.addWidget(toolButton)

                if i.defaultAction().menu() is None:
                    pass
                else:
                    toolButton.setObjectName("menuButton")

            else:
                toolButton = QtGui.QToolButton()
                toolButton.setObjectName("menuButton")
                toolButton.setAutoRaise(i.autoRaise())
                toolButton.setDefaultAction(i.defaultAction())
                toolButton.setIconSize(QtCore.QSize(iconSize, iconSize))
                toolButton.installEventFilter((InstallEvent
                                              .InstallEvent(toolButton)))
                toolButton.setMenu(i.menu())
                toolButton.setPopupMode(i.popupMode())
                layout.addWidget(toolButton)

        for i in toolbarButtons:
            buttonAdd(i)

        quickMenuButton = quickMenu()
        quickMenuButton.setIconSize(QtCore.QSize(iconSize, iconSize))

        layout.addWidget(quickMenuButton)

    def onTabs():

        activeTab = tbTabs.currentWidget().objectName()

        if activeTab:
            onSelector(activeTab)
        else:
            pass

    tbTabs.currentChanged.connect(onTabs)

    def afterStart():
        mw = FreeCADGui.getMainWindow()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        if paramGet.GetString("Position"):
            if paramGet.GetString("Position") == "North":
                tbTabs.setTabPosition(QtGui.QTabWidget.North)
            elif paramGet.GetString("Position") == "South":
                tbTabs.setTabPosition(QtGui.QTabWidget.South)
            elif paramGet.GetString("Position") == "West":
                tbTabs.setTabPosition(QtGui.QTabWidget.West)
            elif paramGet.GetString("Position") == "East":
                tbTabs.setTabPosition(QtGui.QTabWidget.East)
        else:
            tbTabs.setTabPosition(QtGui.QTabWidget.North)

        if paramGet.GetBool("Lock"):
            tbDock.setTitleBarWidget(QtGui.QWidget(None))
        else:
            tbDock.setTitleBarWidget(tbDockTitleBar)

        def autoloadModules():
            listWorkbenches = FreeCADGui.listWorkbenches()
            modulesList = (paramGet.GetString("LoadModules")).split(",")

            paramGenGet = App.ParamGet("User parameter"
                                       ":BaseApp/Preferences/General")

            autoLoadModule = paramGenGet.GetString("AutoloadModule")

            if not autoLoadModule:
                autoLoadModule = "StartWorkbench"
            else:
                pass

            if autoLoadModule in modulesList:
                modulesList.remove(autoLoadModule)

            for i in modulesList:
                if i in listWorkbenches:
                    Gui.activateWorkbench(i)

            if autoLoadModule in listWorkbenches:
                Gui.activateWorkbench(autoLoadModule)

        autoloadModules()

        def onSelectorActionGroup():
            checkedAction = selectorActionGroup.checkedAction().objectName()
            onSelector(checkedAction, mode=1)

        selectorActionGroup.triggered.connect(onSelectorActionGroup)

        activeWB = FreeCADGui.activeWorkbench().name()
        onSelector(activeWB, mode=1)

    afterStart()

timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(guiUp)
timer.start(1000)
FreeCAD.timer = timer
