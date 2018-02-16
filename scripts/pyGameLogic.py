from PyQt5.QtCore import QObject, pyqtSignal

import pyGameData
from pyGameGlobals import KnowledgeValues

class MsgEvent(QObject):
    onMessagesUpdated = pyqtSignal()

class GameLogic():
    def __init__(self, _data):
        self.currentGuess = {}
        self.messageHistory = []
        self.msgEvent = MsgEvent()

    # current session messages
    def clearMessageHistory(self):
        self.messageHistory.clear()

    def addPlayerMessage(self, _msg):
        self.addMessage(_msg)

    def addProgramMessage(self, _msg):
        self.addFormattedMessage(_msg, "blue")

    def addDebugMessage(self, _msg):
        self.addFormattedMessage(_msg, "gray")

    def addErrorMessage(self, _msg):
        self.addFormattedMessage(_msg, "red")

    def addFormattedMessage(self, _msg, _color):
        self.addMessage("<font color='" + _color + "'>" + _msg + "</font")

    def addMessage(self, _msg):
        self.messageHistory.append(_msg)
        self.msgEvent.onMessagesUpdated.emit()
