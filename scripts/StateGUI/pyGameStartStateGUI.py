from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from StateGUI.pyGameBoxLayoutWidget import *


class StartStateWidget(QWidget):
    def __init__(self, _logic):
        super().__init__()

        self.logic = _logic
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.logic.data.phrasing

        self.displayStartState()

    def displayStartState(self):
        msg = self.phrasing.constructInitialPrompt()
        self.messageHistory.addProgramMessage(msg)

        label = QLabel(msg, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonText = self.phrasing.constructInitialPromptButtonText()
        button = QPushButton(buttonText, self)
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(self.onStart)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([label, button])
        layout.addWidget(widget)

    def onStart(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGameStart.emit()
        self.close()
