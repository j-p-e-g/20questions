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
        vLayout.addStretch(1)

        for widget in _widgets:
            vLayout.addWidget(widget)

        vLayout.addStretch(1)

        hLayout = QHBoxLayout()
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
        self.state = GameState.START

        self.initWindow()
        self.displayState()

    def initWindow(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(400, 200, 500, 400)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        self.statusBar().showMessage("Status bar")

        self.setupMenu()

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

    def displayState(self):
        if self.state == GameState.START:
            self.displayStartState()
        elif self.state == GameState.QUESTION:
            self.displayQuestionState()
        elif self.state == GameState.GUESS:
            self.displayGuessState()
        elif self.state == GameState.SOLUTION:
            self.displaySolutionState()
        elif self.state == GameState.DISTINCTION:
            self.displayDistinctionState()

        self.show()

    def displayStartState(self):
        #self.logic.clearMessageHistory()
        self.logic.addFormattedMessage("New round", "green")

        msg = "Think of an object"
        self.logic.addProgramMessage(msg)

        label = QLabel(msg, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        button = QPushButton("Got it!", self)
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(self.onStart)

        widget = BoxWidget([label, button])
        self.setCentralWidget(widget)

    def displayQuestionState(self):
        # TODO: get identifier from data
        identifier = 25368
        modalVerb = "is"
        suffix = "an animal"

        question = modalVerb.capitalize() + " it " + suffix + "?"
        self.logic.addProgramMessage(question)

        label = QLabel(question, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonYes = QPushButton("Yes", self)
        buttonYes.setFont(QFont("Arial", 12))
        buttonYes.clicked.connect(self.onAnswerQuestion)

        buttonNo = QPushButton("No", self)
        buttonNo.setFont(QFont("Arial", 12))
        buttonNo.clicked.connect(self.onAnswerQuestion)

        buttonMaybe = QPushButton("Maybe", self)
        buttonMaybe.setFont(QFont("Arial", 12))
        buttonMaybe.clicked.connect(self.onAnswerQuestion)

        buttonUnknown = QPushButton("I don't know", self)
        buttonUnknown.setFont(QFont("Arial", 12))
        buttonUnknown.clicked.connect(self.onAnswerQuestion)

        widget = BoxWidget([label, buttonYes, buttonNo, buttonMaybe, buttonUnknown])
        self.setCentralWidget(widget)

    def displayGuessState(self):
        # TODO: get guess from data
        article = "a"
        noun = "banana"

        guess = "I think it's " + article + " " + noun
        self.logic.addProgramMessage(guess)

        label = QLabel(guess, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        buttonYes = QPushButton("Correct", self)
        buttonYes.setFont(QFont("Arial", 12))
        buttonYes.clicked.connect(self.onAnswerGuess)

        buttonNo = QPushButton("Wrong", self)
        buttonNo.setFont(QFont("Arial", 12))
        buttonNo.clicked.connect(self.onAnswerGuess)

        widget = BoxWidget([label, buttonYes, buttonNo])
        self.setCentralWidget(widget)

    def displaySolutionState(self):
        query = "I give up! What is it?"
        self.logic.addProgramMessage(query)

        label = QLabel(query, self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("QLabel { color : blue; }");

        self.solution = QLineEdit(self)
        noNumRegex = QRegExp("[a-zA-Z\s-]+")
        self.solution.setValidator(QRegExpValidator(noNumRegex, self.solution))

        button = QPushButton("Send", self)
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(self.onSolution)

        widget = BoxWidget([label, self.solution, button])
        self.setCentralWidget(widget)

    def displayDistinctionState(self):
        print("distinction state")
        # TODO: allow specifying new properties to distinguish between objects
        self.changeState(GameState.START)

    def changeState(self, newState):
        self.state = newState
        self.displayState()

    def onStart(self):
        self.logic.addPlayerMessage(self.sender().text())
        self.changeState(GameState.QUESTION)

    def onAnswerQuestion(self):
        self.logic.addPlayerMessage(self.sender().text())

        # TODO: pass answer to data
        # TODO: actually keep asking question until we either run out of questions or identify the object
        self.changeState(GameState.GUESS)

    def onAnswerGuess(self):
        self.logic.addPlayerMessage(self.sender().text())

        if self.sender().text() == "Wrong":
            # TODO: actually this is only needed if we have no further guesses
            self.changeState(GameState.SOLUTION)
        else:
            # TODO: pass result to data and save
            self.changeState(GameState.START)

    def onSolution(self):
        if len(self.solution.text()) > 0:
            self.changeState(GameState.DISTINCTION)
        else:
            print("Type the name of your object")

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
