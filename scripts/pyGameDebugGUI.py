from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *

# window capable of showing debug information
class DebugWindow(QTabWidget):
    def __init__(self, _mainWindow):
        super().__init__()

        self.mainWindow = _mainWindow

        self.initMe()
        self.show()

    def initMe(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(50, 300, 300, 300)
        self.setWindowTitle("Debug window")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        tabObj = QWidget()
        tabProp = QWidget()
        self.addTab(tabObj, "Objects")
        self.addTab(tabProp, "Properties")

    def closeEvent(self, event):
        self.mainWindow.onDebugWindowClosed()
        event.accept()  # let the window close
