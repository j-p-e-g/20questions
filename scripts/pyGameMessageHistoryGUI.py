from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *

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
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(1000, 150, 300, 500)
        self.setWindowTitle("Message History")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        tab = ScrollBar(self.mainWindow.data)
        self.addTab(tab, "ScrollBar")

    def closeEvent(self, event):
        self.mainWindow.onMsgWindowClosed()
        event.accept()  # let the window close
