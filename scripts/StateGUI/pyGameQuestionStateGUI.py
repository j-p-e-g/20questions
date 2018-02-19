from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *
from StateGUI.pyGameBoxLayoutWidget import *


class QuestionStateWidget(QWidget):
    def __init__(self, _logic, _question):
        super().__init__()

        self.logic = _logic
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.logic.data.phrasing

        self.displayQuestionState(_question)

    def displayQuestionState(self, _question):
        self.messageHistory.addProgramMessage(_question)

        label = QLabel(_question, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonYesText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        buttonNoText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)
        buttonMaybeText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.MAYBE)
        buttonUnknownText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.UNKNOWN)
        maxTextWidth = 10*max(len(buttonYesText), len(buttonNoText), len(buttonMaybeText), len(buttonUnknownText))

        buttonYes = QPushButton(buttonYesText, self)
        buttonYes.setFont(QFont("Arial", 12))
        buttonYes.clicked.connect(self.onAnswerQuestion)
        buttonYes.setMinimumWidth(maxTextWidth)

        buttonNo = QPushButton(buttonNoText, self)
        buttonNo.setFont(QFont("Arial", 12))
        buttonNo.clicked.connect(self.onAnswerQuestion)
        buttonNo.setMinimumWidth(maxTextWidth)

        buttonMaybe = QPushButton(buttonMaybeText, self)
        buttonMaybe.setFont(QFont("Arial", 12))
        buttonMaybe.clicked.connect(self.onAnswerQuestion)
        buttonMaybe.setMinimumWidth(maxTextWidth)

        buttonUnknown = QPushButton(buttonUnknownText, self)
        buttonUnknown.setFont(QFont("Arial", 12))
        buttonUnknown.clicked.connect(self.onAnswerQuestion)
        buttonUnknown.setMinimumWidth(maxTextWidth)

        emptyLabel = QLabel("", self)

        buttonRestartText = self.phrasing.constructRestartButtonText()
        buttonRestart = QPushButton(buttonRestartText, self)
        buttonRestart.setFont(QFont("Arial", 12))
        buttonRestart.clicked.connect(self.onRestart)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([label, buttonYes, buttonNo, buttonMaybe, buttonUnknown, emptyLabel, emptyLabel, emptyLabel, buttonRestart])
        layout.addWidget(widget)

    def onAnswerQuestion(self):
        buttonText = self.sender().text()
        self.messageHistory.addPlayerMessage(buttonText)
        self.logic.inputEvent.onQuestionAnswered.emit(buttonText)
        self.close()

    def onRestart(self):
        self.logic.inputEvent.onRestart.emit()
        self.close()