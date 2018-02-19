from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *
from StateGUI.pyGameBoxLayoutWidget import *


class GuessStateWidget(QWidget):
    def __init__(self, _mainWindow, _logic, _guess):
        super().__init__()

        self.mainWindow = _mainWindow
        self.logic = _logic
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.logic.data.phrasing

        self.displayGuessState(_guess)

    def displayGuessState(self, _guess):
        self.messageHistory.addProgramMessage(_guess)

        label = QLabel(_guess, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonYesText = self.phrasing.constructGuessResponseButtonText(True)
        buttonYes = QPushButton(buttonYesText, self)
        buttonYes.setFont(QFont("Arial", 12))
        buttonYes.clicked.connect(self.onAnswerGuessTrue)

        buttonNoText = self.phrasing.constructGuessResponseButtonText(False)
        buttonNo = QPushButton(buttonNoText, self)
        buttonNo.setFont(QFont("Arial", 12))
        buttonNo.clicked.connect(self.onAnswerGuessFalse)

        emptyLabel = QLabel("", self)

        buttonRestartText = self.phrasing.constructRestartButtonText()
        buttonRestart = QPushButton(buttonRestartText, self)
        buttonRestart.setFont(QFont("Arial", 12))
        buttonRestart.clicked.connect(self.onRestart)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([label, buttonYes, buttonNo, emptyLabel, emptyLabel, emptyLabel, buttonRestart])
        layout.addWidget(widget)

    def onAnswerGuessTrue(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGuessReaction.emit(True)
        self.logic.guessEvent.onRoundFinished.emit()
        self.close()

    def onAnswerGuessFalse(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGuessReaction.emit(False)
        self.close()

    def onRestart(self):
        self.logic.inputEvent.onRestart.emit()
        self.close()