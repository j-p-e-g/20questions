from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# implement scrollable window
class ScrollBar(QWidget):
    def __init__(self, _data):
        super().__init__()

        self.data = _data

        self.initMe()
        self.show()

    def initMe(self):
        box = QVBoxLayout(self)
        self.setLayout(box)

        scroll = QScrollArea(self)
        box.addWidget(scroll)
        scroll.setWidgetResizable(True)

        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        for msg in self.data.messageHistory:
            scrollLayout.addWidget(QLabel(msg))

        scroll.setWidget(scrollContent)

# scrollable window capable of showing the message history
class MessageHistoryWindow(QTabWidget):
    def __init__(self, _mainWindow):
        super().__init__()

        self.mainWindow = _mainWindow

        self.initMe()
        self.show()

    def initMe(self):
        # pos(x, y), size(width, height)
        self.setGeometry(1000, 150, 300, 500)
        self.setWindowTitle("Message History")
        self.setWindowIcon(QIcon("images/questionExclamationMark.png"))

        tab = ScrollBar(self.mainWindow.data)
        self.addTab(tab, "ScrollBar")

    def closeEvent(self, event):
        self.mainWindow.onMsgWindowClosed()
        event.accept()  # let the window close

# window capable of showing debug information
class DebugWindow(QTabWidget):
    def __init__(self, _mainWindow):
        super().__init__()

        self.mainWindow = _mainWindow

        self.initMe()
        self.show()

    def initMe(self):
        # pos(x, y), size(width, height)
        self.setGeometry(50, 300, 300, 300)
        self.setWindowTitle("Debug window")
        self.setWindowIcon(QIcon("images/questionExclamationMark.png"))

        tabObj = QWidget()
        tabProp = QWidget()
        self.addTab(tabObj, "Objects")
        self.addTab(tabProp, "Properties")

    def closeEvent(self, event):
        self.mainWindow.onDebugWindowClosed()
        event.accept()  # let the window close

# application main window
class MainWindow(QMainWindow):
    def __init__(self, _data):
        super().__init__()

        self.msgWindowVisible = False
        self.debugWindowVisible = False
        self.data = _data

        self.initMe()
        self.show()

    def initMe(self):
        # pos(x, y), size(width, height)
        self.setGeometry(400, 200, 500, 400)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon("images/questionExclamationMark.png"))

        self.statusBar().showMessage("Status bar")

        # set up exit action
        self.msgAction = QAction(QIcon("images/tickMark.png"), "&Show History", self)
        self.msgAction.setIconVisibleInMenu(False)
        self.msgAction.setShortcut("Ctrl+M")
        self.msgAction.setStatusTip("Show message history")
        self.msgAction.triggered.connect(self.onToggleMessageHistory)

        self.debugAction = QAction(QIcon("images/tickMark.png"), "&Show Debug", self)
        self.debugAction.setIconVisibleInMenu(False)
        self.debugAction.setShortcut("Ctrl+D")
        self.debugAction.setStatusTip("Show debug window")
        self.debugAction.triggered.connect(self.onToggleDebug)

        # set up menu with sub action
        menubar = self.menuBar()
        file = menubar.addMenu("&View")
        file.addAction(self.msgAction)
        file.addAction(self.debugAction)

    def closeEvent(self, event):
        exit()

    def onToggleMessageHistory(self):
        if self.msgWindowVisible:
            self.msgWindow.close()
            self.onMsgWindowClosed()
        else:
            self.msgWindow = MessageHistoryWindow(self)
            self.msgAction.setIconVisibleInMenu(True)
            self.msgWindowVisible = True

    def onMsgWindowClosed(self):
        self.msgWindowVisible = False
        self.msgAction.setIconVisibleInMenu(False)

    def onToggleDebug(self):
        if self.debugWindowVisible:
            self.debugWindow.close()
            self.onDebugWindowClosed()
        else:
            self.debugWindow = DebugWindow(self)
            self.debugAction.setIconVisibleInMenu(True)
            self.debugWindowVisible = True

    def onDebugWindowClosed(self):
        self.debugWindowVisible = False
        self.debugAction.setIconVisibleInMenu(False)
