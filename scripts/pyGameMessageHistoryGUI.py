from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *
import pyGameScrollBarGUI as scrollBar


# scrollable window capable of showing the message history
class MessageHistoryWindow(QTabWidget):
    def __init__(self, _mainWindow):
        super().__init__()

        self.mainWindow = _mainWindow

        self.messageHistory = self.mainWindow.logic.messageHistory
        self.messageHistory.msgEvent.onMessagesUpdated.connect(self.updateMessages)

        self.initMe()
        self.updateMessages()
        self.show()

    def initMe(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(1000, 150, 300, 500)
        self.setWindowTitle("Message History")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        self.scrollBar = scrollBar.ScrollBar(True)
        self.addTab(self.scrollBar, "Messages")

    def updateMessages(self):
        self.scrollBar.update(self.messageHistory.list)

    def closeEvent(self, event):
        self.mainWindow.onMsgWindowClosed()
        event.accept()  # let the window close
