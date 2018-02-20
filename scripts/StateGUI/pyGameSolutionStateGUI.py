from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *
from StateGUI.pyGameBoxLayoutWidget import *


class SolutionStateWidget(QWidget):
    def __init__(self, _logic):
        super().__init__()

        self.logic = _logic
        self.data = self.logic.data
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.data.phrasing

        self.displaySolutionState()

    def displaySolutionState(self):
        query = self.phrasing.constructSolutionRequest()
        self.messageHistory.addProgramMessage(query)

        label = QLabel(query, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }")

        # allow the player to either choose from a dropdown menu of existing objects, or add a new one
        objectList = self.data.getListOfAllObjectNames()

        self.comboBox = QComboBox()
        self.comboBox.setFont(QFont("Arial", 12))
        self.comboBox.addItem("add new object, or pick one:")
        for objName in objectList:
            self.comboBox.addItem(objName)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)

        self.solutionTextBox = QLineEdit(self)
        self.solutionTextBox.setFont(QFont("Arial", 12))
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

        widget = BoxWidget([label, emptyLabel, self.comboBox, self.solutionTextBox, emptyLabel, self.sendButton, emptyLabel, emptyLabel, emptyLabel, buttonRestart])
        layout.addWidget(widget)

    def onComboBoxIndexChanged(self, index):
        if index != 0:
            self.solutionTextBox.setVisible(False)
            self.solutionTextBox.setText("")
        else:
            self.solutionTextBox.setVisible(True)

        self.updateSendButton()

    def onTextInputChanged(self):
        if self.solutionTextBox.text() != "":
            self.comboBox.setCurrentIndex(0)

        self.updateSendButton()

    def updateSendButton(self):
        if self.comboBox.currentIndex() > 0:
            self.sendButton.setEnabled(True)
        else:
            isEmpty = (self.solutionTextBox.text() == "")
            self.sendButton.setEnabled(not isEmpty)

    def onSolutionSent(self):
        if self.comboBox.currentIndex() > 0:
            solution = self.comboBox.currentText()
        else:
            solution = self.solutionTextBox.text()

        self.messageHistory.addPlayerMessage(solution)
        self.logic.inputEvent.onSolutionSent.emit(solution)
        self.close()

    def onRestart(self):
        buttonText = self.sender().text()
        self.messageHistory.addPlayerMessage(buttonText)
        self.logic.inputEvent.onRestart.emit()
        self.close()