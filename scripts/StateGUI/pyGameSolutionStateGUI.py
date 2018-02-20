from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *
from StateGUI.pyGameBoxLayoutWidget import *


class SolutionStateWidget(QWidget):
    def __init__(self, _logic):
        super().__init__()

        self.logic = _logic
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.logic.data.phrasing

        self.displaySolutionState()

    def displaySolutionState(self):
        query = self.phrasing.constructSolutionRequest()
        self.messageHistory.addProgramMessage(query)

        label = QLabel(query, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        self.solutionTextBox = QLineEdit(self)
        self.solutionTextBox.textChanged.connect(self.onTextInputChanged)

        noNumRegex = QRegExp("[a-zA-Z\s-]+")
        self.solutionTextBox.setValidator(QRegExpValidator(noNumRegex, self.solutionTextBox))

        sendButtonText = self.phrasing.constructSolutionButtonText()
        self.sendButton = QPushButton(sendButtonText, self)
        self.sendButton.setFont(QFont("Arial", 12))
        self.sendButton.setEnabled(False)
        self.sendButton.clicked.connect(self.onSolutionSent)

        emptyLabel = QLabel("", self)

        buttonRestartText = self.phrasing.constructRestartButtonText()
        buttonRestart = QPushButton(buttonRestartText, self)
        buttonRestart.setFont(QFont("Arial", 12))
        buttonRestart.clicked.connect(self.onRestart)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([label, self.solutionTextBox, self.sendButton, emptyLabel, emptyLabel, emptyLabel, buttonRestart])
        layout.addWidget(widget)

    def onTextInputChanged(self):
        solution = self.solutionTextBox.text()
        isEmpty = (solution == "")
        self.sendButton.setEnabled(not isEmpty)

    def onSolutionSent(self):
        solution = self.solutionTextBox.text()
        self.messageHistory.addPlayerMessage(solution)
        self.logic.inputEvent.onSolutionSent.emit(solution)
        self.close()

    def onRestart(self):
        buttonText = self.sender().text()
        self.messageHistory.addPlayerMessage(buttonText)
        self.logic.inputEvent.onRestart.emit()
        self.close()