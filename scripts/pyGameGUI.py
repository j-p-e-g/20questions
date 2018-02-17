from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *
import pyGameDebugGUI as debugGUI
import pyGameMessageHistoryGUI as msgGUI
import StateGUI.pyGameStartStateGUI as startState
import StateGUI.pyGameQuestionStateGUI as questionState
import StateGUI.pyGameGuessStateGUI as guessState
import StateGUI.pyGameSolutionStateGUI as solutionState


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

        self.initWindow()

        self.setCentralWidget(startState.StartStateWidget(self.logic))
        self.show()

    def initWindow(self):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(400, 200, 500, 400)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))
#        self.statusBar().showMessage("Status bar")

        self.setupMenu()

    def onReceivedQuestion(self, _question):
        self.setCentralWidget(questionState.QuestionStateWidget(self.logic, _question))
        self.show()

    def onReceivedGuess(self, _guess):
        self.setCentralWidget(guessState.GuessStateWidget(self, self.logic, _guess))
        self.show()

    def onSolutionRequested(self):
        self.setCentralWidget(solutionState.SolutionStateWidget(self.logic))
        self.show()

    def onRoundFinished(self):
        self.setCentralWidget(startState.StartStateWidget(self.logic))
        self.show()

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
