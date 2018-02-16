from PyQt5.QtCore import QObject, pyqtSignal

import pyGameData
from pyGameGlobals import KnowledgeValues

class InputEvent(QObject):
    onGameStart = pyqtSignal()
    onQuestionAnswered = pyqtSignal(int)
    onGuessReaction = pyqtSignal(bool)

class MsgEvent(QObject):
    onMessagesUpdated = pyqtSignal()

class GuessEvent(QObject):
    onStartGame = pyqtSignal()
    onGuessSent = pyqtSignal(str)
    onQuestionSent = pyqtSignal(str)
    onRequestSolution = pyqtSignal()

class GameLogic():
    def __init__(self, _data):
        self.data = _data
        self.properties = {}
        self.messageHistory = []

        self.msgEvent = MsgEvent()
        self.guessEvent = GuessEvent()
        self.inputEvent = InputEvent()

        self.inputEvent.onGameStart.connect(self.startRound)
        self.inputEvent.onQuestionAnswered.connect(self.onReceivedQuestionAnswer)
        self.inputEvent.onGuessReaction.connect(self.onReceivedGuessResponse)

        self.initRound(_data)

    def initRound(self, data):
        self.guesses = []
        self.previousQuestion = 0
        self.currentGuess = {}

        for prop in data.properties[data.propertiesMainAttribute]:
            propEntry = {}
            propEntry["tried"] = False
            propEntry["value"] = KnowledgeValues.UNKNOWN
            self.properties[prop["identifier"]] = propEntry

    def startRound(self):
        # 1. iterate over all properties for the current guess
        # 2. assign weights to each object
        # 3. if there's a single object matching all properties, guess!
        # 4. otherwise, ask a question that hasn't been asked before
        # 5. if all questions were asked and no object matches, ask for the solution
        self.nextRun()

    def nextRun(self):
        for identifier in self.properties:
            entry = self.properties[identifier]
            if not entry["tried"]:
                question = self.data.constructQuestion(identifier)
                if question != "":
                    self.previousQuestion = identifier
                    self.guessEvent.onQuestionSent.emit(question)
                    entry["tried"] = True
                    return

        guess = self.data.constructGuess("airplane")
        if guess != "":
            self.guesses = []
            self.guessEvent.onGuessSent.emit(guess)
            return

        self.guessEvent.onRequestSolution.emit()

    def onReceivedQuestionAnswer(self, _value):
        print("onReceivedQuestionAnswer: " + str(_value))
        if self.previousQuestion in self.properties:
            entry = self.properties[self.previousQuestion]
            entry["value"] = _value
        else:
            errorMsg = "Identifier '" + str(self.previousQuestion) + "' not found in Logic properties!"
            print(errorMsg)
            self.addErrorMessage(errorMsg)

        self.nextRun()

    def onReceivedGuessResponse(self, _result):
        print("onReceivedGuessResponse: " + str(_result))

        if _result:
            self.updateData()
            self.guessEvent.onStartGame.emit()
        else:
            # keep asking
            self.nextRun()

    # current session messages
    def clearMessageHistory(self):
        self.messageHistory.clear()

    def addPlayerMessage(self, _msg):
        self.addMessage("\"" + _msg + "\"")

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

    def updateData(self):
        self.data.saveObjects()
        self.data.saveProperties()
