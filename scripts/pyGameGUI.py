from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *
import pyGameDebugGUI as debugGUI
import pyGameMessageHistoryGUI as msgGUI
from enum import Enum

class GameState(Enum):
    START = 0
    QUESTION = 1
    GUESS = 2
    SOLUTION = 3
    DISTINCTION = 4

class BoxWidget(QWidget):
    def __init__(self, _widgets):
        super().__init__()

        vLayout = QVBoxLayout()
        vLayout.setSpacing(5)
        vLayout.addStretch(1)

        for widget in _widgets:
            vLayout.addWidget(widget)

        vLayout.addStretch(1)

        hLayout = QHBoxLayout()
        hLayout.setSpacing(5)
        hLayout.addStretch(1)
        hLayout.addLayout(vLayout)
        hLayout.addStretch(1)

        self.setLayout(hLayout)


# application main window
class MainWindow(QMainWindow):
    def __init__(self, _logic):
        super().__init__()

        self.msgWindowVisible = False
        self.debugWindowVisible = False
        self.logic = _logic
        self.logic.guessEvent.onGuessSent.connect(self.onReceivedGuess)
        self.logic.guessEvent.onQuestionSent.connect(self.onReceivedQuestion)
        self.logic.guessEvent.onRequestSolution.connect(self.onSolutionRequested)
        self.logic.guessEvent.onRoundFinished.connect(self.onRoundFinished)

        self.data = self.logic.data
        self.phrasing = self.data.phrasing

        self.messageHistory = self.logic.messageHistory

        self.initWindow()
        self.displayStartState()

    def initWindow(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(400, 200, 500, 400)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        self.statusBar().showMessage("Status bar")

        self.setupMenu()

    def onReceivedGuess(self, _guess):
        self.displayGuessState(_guess)
        self.show()

    def onReceivedQuestion(self, _question):
        self.displayQuestionState(_question)
        self.show()

    def onSolutionRequested(self):
        self.displaySolutionState()
        self.show()

    def onRoundFinished(self):
        self.displayStartState()

    def closeEvent(self, event):
        # close the entire application even if other windows are still open
        exit()

    def setupMenu(self):
        global TICK_ICON_PATH

        # set up exit action
        self.msgAction = QAction(QIcon(TICK_ICON_PATH), "&Show History", self)
        self.msgAction.setIconVisibleInMenu(False)
        self.msgAction.setShortcut("Ctrl+M")
        self.msgAction.setStatusTip("Show message history")
        self.msgAction.triggered.connect(self.onToggleMessageHistory)
        self.debugAction = QAction(QIcon(TICK_ICON_PATH), "&Show Debug", self)
        self.debugAction.setIconVisibleInMenu(False)
        self.debugAction.setShortcut("Ctrl+D")
        self.debugAction.setStatusTip("Show debug window")
        self.debugAction.triggered.connect(self.onToggleDebug)

        # set up menu with sub action
        menubar = self.menuBar()
        file = menubar.addMenu("&View")
        file.addAction(self.msgAction)
        file.addAction(self.debugAction)

    def displayStartState(self):
        self.messageHistory.addFormattedMessage("New round", "green")

        msg = self.phrasing.constructInitialPrompt()
        self.messageHistory.addProgramMessage(msg)

        label = QLabel(msg, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonText = self.phrasing.constructInitialPromptButtonText()
        button = QPushButton(buttonText, self)
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(self.onStart)

        widget = BoxWidget([label, button])
        self.setCentralWidget(widget)
        self.show()

    def displayQuestionState(self, _question):
        self.messageHistory.addProgramMessage(_question)

        label = QLabel(_question, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonYesText = self.phrasing.constructAnswerButtonText(KnowledgeValues.YES)
        buttonNoText = self.phrasing.constructAnswerButtonText(KnowledgeValues.NO)
        buttonMaybeText = self.phrasing.constructAnswerButtonText(KnowledgeValues.MAYBE)
        buttonUnknownText = self.phrasing.constructAnswerButtonText(KnowledgeValues.UNKNOWN)
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

        widget = BoxWidget([label, buttonYes, buttonNo, buttonMaybe, buttonUnknown])
        self.setCentralWidget(widget)
        self.show()

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

        widget = BoxWidget([label, buttonYes, buttonNo])
        self.setCentralWidget(widget)
        self.show()

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

        widget = BoxWidget([label, self.solutionTextBox, button])
        self.setCentralWidget(widget)
        self.show()

    def displayDistinctionState(self):
        print("distinction state")
        # TODO: allow specifying new properties to distinguish between objects
        self.displayStartState()

    def onStart(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGameStart.emit()

    def onAnswerQuestion(self):
        buttonText = self.sender().text()
        self.messageHistory.addPlayerMessage(buttonText)
        self.logic.inputEvent.onQuestionAnswered.emit(buttonText)

    def onAnswerGuessTrue(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGuessReaction.emit(True)
        self.displayStartState()

    def onAnswerGuessFalse(self):
        self.messageHistory.addPlayerMessage(self.sender().text())
        self.logic.inputEvent.onGuessReaction.emit(False)

    def onSolutionSent(self):
        solution = self.solutionTextBox.text()
        if len(solution) > 0:
            self.messageHistory.addPlayerMessage(solution)
            self.logic.inputEvent.onSolutionSent.emit(solution)
        else:
            msg = "Type the name of your object"
            self.messageHistory.addProgramMessage(msg)
            print(msg)

    def onToggleMessageHistory(self):
        if self.msgWindowVisible:
            self.msgWindow.close()
            self.onMsgWindowClosed()
        else:
            self.msgWindow = msgGUI.MessageHistoryWindow(self)
            self.msgAction.setIconVisibleInMenu(True)
            self.msgWindowVisible = True

    def onMsgWindowClosed(self):
        self.msgWindowVisible = False
        self.msgAction.setIconVisibleInMenu(False)

    def onToggleDebug(self):
        if self.debugWindowVisible:
            self.debugWindow.close()
            self.onDebugWindowClosed()
        else:
            self.debugWindow = debugGUI.DebugWindow(self)
            self.debugAction.setIconVisibleInMenu(True)
            self.debugWindowVisible = True

    def onDebugWindowClosed(self):
        self.debugWindowVisible = False
        self.debugAction.setIconVisibleInMenu(False)
