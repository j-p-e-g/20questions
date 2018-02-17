from PyQt5.QtCore import QObject, pyqtSignal

import pyGameMessageHistory as msgHistory
from pyGameGlobals import KnowledgeValues


class InputEvent(QObject):
    onGameStart = pyqtSignal()
    onQuestionAnswered = pyqtSignal(str)
    onGuessReaction = pyqtSignal(bool)
    onSolutionSent = pyqtSignal(str)


class GuessEvent(QObject):
    onGuessSent = pyqtSignal(str)
    onQuestionSent = pyqtSignal(str)
    onRequestSolution = pyqtSignal()
    onRoundFinished = pyqtSignal()


class DebugEvent(QObject):
    onPropertiesUpdated = pyqtSignal()
    onObjectsUpdated = pyqtSignal()


class GameLogic():
    def __init__(self, _data):
        self.data = _data
        self.phrasing = self.data.phrasing

        self.properties = {}
        self.objects = {}
        self.messageHistory = msgHistory.MessageHistory()

        self.guessEvent = GuessEvent()
        self.inputEvent = InputEvent()
        self.debugEvent = DebugEvent()

        self.inputEvent.onGameStart.connect(self.startRound)
        self.inputEvent.onQuestionAnswered.connect(self.onReceivedQuestionAnswer)
        self.inputEvent.onGuessReaction.connect(self.onReceivedGuessResponse)
        self.inputEvent.onSolutionSent.connect(self.onReceivedSolution)

        self.yesValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        self.noValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)
        self.maybeValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.MAYBE)

        self.initRound()

    def initRound(self):
        self.previousQuestion = 0
        self.guesses = []
        self.objectCandidates = []

        self.initProperties()
        self.initObjects()

    def initProperties(self):
        self.properties = {}

        for prop in self.data.properties[self.data.propertiesMainAttribute]:
            propEntry = {}
            propEntry["tried"] = False
            propEntry["value"] = KnowledgeValues.UNKNOWN

            propEntry["desc"] = prop["modal_verb"] + " " + prop["suffix"]

            # setup empty, will be filled in initObjects
            propEntry["objects"] = {}
            propEntry["objects"][self.yesValueText] = []
            propEntry["objects"][self.noValueText] = []

            self.properties[prop["identifier"]] = propEntry

    def initObjects(self):
        self.objects = {}

        for obj in self.data.objects[self.data.objectsMainAttribute]:

            name = obj["name"]
            if name in self.objects:
                print("Warning: " + name + " already defined in objects!")
                continue

            self.objectCandidates.append(name)

            yesProperties = []
            noProperties = []
            maybeProperties = []

            for prop in obj["properties"]:
                identifier = prop["identifier"]
                value = prop["value"]

                if not identifier in self.properties:
                    print("Warning: Property '" + str(identifier) + "' not defined in properties!")
                    continue

                if value == KnowledgeValues.UNKNOWN:
                    continue

                propEntry = self.properties[identifier]

                if value == KnowledgeValues.YES:
                    yesProperties.append(identifier)
                    propEntry["objects"][self.yesValueText].append(name)
                elif value == KnowledgeValues.NO:
                    noProperties.append(identifier)
                    propEntry["objects"][self.noValueText].append(name)
                elif value == KnowledgeValues.MAYBE:
                    maybeProperties.append(identifier)

            objEntry = {}
            objEntry["properties"] = {}

            objEntry["properties"][self.yesValueText] = yesProperties
            objEntry["properties"][self.noValueText] = noProperties
            objEntry["properties"][self.maybeValueText] = maybeProperties

            self.objects[name] = objEntry

    def startRound(self):
        self.nextRun()

    def nextRun(self):

        if len(self.objectCandidates) == 1:
            guess = self.data.constructGuess(self.objectCandidates[0])
            if guess != "":
                self.guesses.append(self.objectCandidates[0])
                self.guessEvent.onGuessSent.emit(guess)
                self.debugEvent.onObjectsUpdated.emit()
                return

        # 1. iterate over all properties for the current guess
        # 2. assign weights to each object
        # 3. if there's a single object matching all properties, guess!
        # 4. otherwise, ask a question that hasn't been asked before
        # 5. if all questions were asked and no object matches, ask for the solution

        # ask questions to narrow down the solution space
        if self.tryFindGoodQuestion():
            return

        # guess the object
        if self.tryFindGoodGuess():
            return

        # if nothing else works, ask for the solution
        self.guessEvent.onRequestSolution.emit()

    def tryFindGoodQuestion(self):
        for identifier in self.properties:
            entry = self.properties[identifier]
            if entry["tried"]:
                continue

            question = self.data.constructQuestion(identifier)
            if question != "":
                self.previousQuestion = identifier
                self.guessEvent.onQuestionSent.emit(question)
                entry["tried"] = True
                self.debugEvent.onPropertiesUpdated.emit()
                return True

        return False

    def tryFindGoodGuess(self):
        for objName in self.objectCandidates:
            if objName in self.guesses:
                continue

            guess = self.data.constructGuess(objName)
            if guess != "":
                self.guesses.append(objName)
                self.guessEvent.onGuessSent.emit(guess)
                self.debugEvent.onObjectsUpdated.emit()
                return True

        return False

    def onReceivedQuestionAnswer(self, _buttonText):
        value = self.data.phrasing.getKnowledgeValueForText(_buttonText)
        print("onReceivedQuestionAnswer: " + _buttonText + " -> " + str(value))

        if self.previousQuestion in self.properties:
            entry = self.properties[self.previousQuestion]
            entry["value"] = value

            # If the player answered yes or no, remove all objects with the opposite value
            # from the list of candidates.
            if value == KnowledgeValues.YES:
                for objName in entry["objects"][self.noValueText]:
                    if objName in self.objectCandidates:
                        self.objectCandidates.remove(objName)
            elif value == KnowledgeValues.NO:
                for objName in entry["objects"][self.yesValueText]:
                    if objName in self.objectCandidates:
                        self.objectCandidates.remove(objName)

            self.debugEvent.onPropertiesUpdated.emit()
        else:
            errorMsg = "Identifier '" + str(self.previousQuestion) + "' not found in Logic properties!"
            print(errorMsg)
            self.messageHistory.addErrorMessage(errorMsg)

        self.nextRun()

    def onReceivedGuessResponse(self, _success):
        prevGuess = self.guesses[len(self.guesses) - 1]

        if _success:
            if len(self.guesses) == 0:
                errorMsg = "Guess got confirmed but is not stored!"
                print(errorMsg)
                self.messageHistory.addErrorMessage(errorMsg)
                return

            self.updateData(prevGuess)
            self.initRound()
            self.guessEvent.onRoundFinished.emit()
        else:
            # keep asking
            if prevGuess in self.objectCandidates:
                self.objectCandidates.remove(prevGuess)

            self.nextRun()

    def onReceivedSolution(self, _solution):
        self.updateData(_solution)
        self.initRound()
        self.guessEvent.onRoundFinished.emit()

    def updateData(self, _solution):
        self.data.addOrUpdateObject(_solution, self.properties)
        self.data.saveObjects()
        self.data.saveProperties()
