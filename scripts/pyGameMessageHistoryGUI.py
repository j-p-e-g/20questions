from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *

# implement scrollable window
class ScrollBar(QWidget):
    def __init__(self, _logic):
        super().__init__()

        self.logic = _logic
        self.logic.msgEvent.onMessagesUpdated.connect(self.updateMessages)

        self.initMe()

        self.updateMessages()

    def initMe(self):
        box = QVBoxLayout(self)
        self.setLayout(box)

        self.scrollArea = QScrollArea(self)
        box.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)

        # after each update, scroll to the bottom of the list
        scrollBar = self.scrollArea.verticalScrollBar()
        scrollBar.rangeChanged.connect(lambda: scrollBar.setValue(scrollBar.maximum()))

        self.scrollContent = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContent)

        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.scrollContent.setLayout(self.scrollLayout)

    def updateMessages(self):
        # clear layout
        while self.scrollLayout.count() > 0:
            item = self.scrollLayout.takeAt(0)
            if not item:
                continue

            w = item.widget()
            if w:
                 w.deleteLater()

        for msg in self.logic.messageHistory:
            label = QLabel(msg)
            self.scrollLayout.addWidget(label)

        self.show()


# scrollable window capable of showing the message history
class MessageHistoryWindow(QTabWidget):
    def __init__(self, _mainWindow):
        super().__init__()

        self.mainWindow = _mainWindow

        self.initMe()
        self.scrollBar.updateMessages()
        self.show()

    def initMe(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(1000, 150, 300, 500)
        self.setWindowTitle("Message History")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        self.scrollBar = ScrollBar(self.mainWindow.logic)
        self.addTab(self.scrollBar, "ScrollBar")

    def closeEvent(self, event):
        self.mainWindow.onMsgWindowClosed()
        event.accept()  # let the window close
