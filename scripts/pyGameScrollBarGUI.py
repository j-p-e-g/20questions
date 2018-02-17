from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyGameGlobals import *


# implement scrollable window
class ScrollBar(QWidget):
    def __init__(self, _scrollToBottom):
        super().__init__()

        self.initMe(_scrollToBottom)

    def initMe(self, _scrollToBottom):
        box = QVBoxLayout(self)
        self.setLayout(box)

        self.scrollArea = QScrollArea(self)
        box.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)

        # after each update, scroll to the bottom of the list
        scrollBar = self.scrollArea.verticalScrollBar()

        if _scrollToBottom:
            scrollBar.rangeChanged.connect(lambda: scrollBar.setValue(scrollBar.maximum()))

        self.scrollContent = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContent)

        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.scrollContent.setLayout(self.scrollLayout)

    def update(self, _content):
        self.clearLayout()

        for line in _content:
            label = QLabel(line)
            self.scrollLayout.addWidget(label)

        self.show()

    def clearLayout(self):
        while self.scrollLayout.count() > 0:
            item = self.scrollLayout.takeAt(0)
            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()
