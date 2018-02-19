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
        noNumRegex = QRegExp("[a-zA-Z\s-]+")
        self.solutionTextBox.setValidator(QRegExpValidator(noNumRegex, self.solutionTextBox))

        buttonText = self.phrasing.constructSolutionButtonText()
        button = QPushButton(buttonText, self)
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(self.onSolutionSent)

        emptyLabel = QLabel("", self)

        buttonRestartText = self.phrasing.constructRestartButtonText()
        buttonRestart = QPushButton(buttonRestartText, self)
        buttonRestart.setFont(QFont("Arial", 12))
        buttonRestart.clicked.connect(self.onRestart)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([label, self.solutionTextBox, button, emptyLabel, emptyLabel, emptyLabel, buttonRestart])
        layout.addWidget(widget)

    def onSolutionSent(self):
        solution = self.solutionTextBox.text()
        if len(solution) > 0:
            self.messageHistory.addPlayerMessage(solution)
            self.logic.inputEvent.onSolutionSent.emit(solution)
            self.close()
        else:
            msg = "Type the name of your object"
            self.messageHistory.addProgramMessage(msg)
            print(msg)

    def onRestart(self):
        self.logic.inputEvent.onRestart.emit()
        self.close()