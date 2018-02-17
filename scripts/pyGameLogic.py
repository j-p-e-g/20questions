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

        self.initRound()

    def initRound(self):
        self.previousQuestion = 0
        self.guesses = []

        self.initProperties()
        self.initObjects()

    def initProperties(self):
        self.properties = {}

        yesValueText = self.data.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        noValueText = self.data.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)

        for prop in self.data.properties[self.data.propertiesMainAttribute]:
            propEntry = {}
            propEntry["tried"] = False
            propEntry["value"] = KnowledgeValues.UNKNOWN

            propEntry["desc"] = prop["modal_verb"] + " " + prop["suffix"]

            # setup empty, will be filled in initObjects
            propEntry["objects"] = {}
            propEntry["objects"][yesValueText] = []
            propEntry["objects"][noValueText] = []

            self.properties[prop["identifier"]] = propEntry

    def initObjects(self):
        self.objects = {}

        yesValueText = self.data.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        noValueText = self.data.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)
        maybeValueText = self.data.phrasing.getTextForKnowledgeValue(KnowledgeValues.MAYBE)

        for obj in self.data.objects[self.data.objectsMainAttribute]:

            name = obj["name"]
            if name in self.objects:
                print("Warning: " + name + " already defined in objects!")
                continue

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
                    propEntry["objects"][yesValueText].append(name)
                elif value == KnowledgeValues.NO:
                    noProperties.append(identifier)
                    propEntry["objects"][noValueText].append(name)
                elif value == KnowledgeValues.MAYBE:
                    maybeProperties.append(identifier)

            objEntry = {}
            objEntry["properties"] = {}

            objEntry["properties"][yesValueText] = yesProperties
            objEntry["properties"][noValueText] = noProperties
            objEntry["properties"][maybeValueText] = maybeProperties

            self.objects[name] = objEntry

    def startRound(self):
        self.nextRun()

    def nextRun(self):
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
        try:
            objects = self.data.objects[self.data.objectsMainAttribute]
            for obj in objects:
                if not "name" in obj:
                    self.messageHistory.addErrorMessage("Key 'name' not found in data objects")
                else:
                    objName = obj["name"]
                    if objName in self.guesses:
                        continue

                    guess = self.data.constructGuess(objName)
                    if guess != "":
                        self.guesses.append(objName)
                        self.guessEvent.onGuessSent.emit(guess)
                        self.debugEvent.onObjectsUpdated.emit()
                        return True

        except KeyError:
            self.messageHistory.addErrorMessage("'" + self.data.objectsMainAttribute + "' not found in data objects")

        return False

    def onReceivedQuestionAnswer(self, _buttonText):
        value = self.data.phrasing.getKnowledgeValueForText(_buttonText)
        print("onReceivedQuestionAnswer: " + _buttonText + " -> " + str(value))

        if self.previousQuestion in self.properties:
            entry = self.properties[self.previousQuestion]
            entry["value"] = value
            self.debugEvent.onPropertiesUpdated.emit()
        else:
            errorMsg = "Identifier '" + str(self.previousQuestion) + "' not found in Logic properties!"
            print(errorMsg)
            self.messageHistory.addErrorMessage(errorMsg)

        self.nextRun()

    def onReceivedGuessResponse(self, _success):
        if _success:
            if len(self.guesses) == 0:
                errorMsg = "Guess got confirmed but is not stored!"
                print(errorMsg)
                self.messageHistory.addErrorMessage(errorMsg)
                return

            lastGuess = self.guesses[len(self.guesses) - 1]
            self.updateData(lastGuess)
            self.initRound()
            self.guessEvent.onRoundFinished.emit()
        else:
            # keep asking
            self.nextRun()

    def onReceivedSolution(self, _solution):
        print("OnReceivedSolution: " + _solution)
        self.updateData(_solution)
        self.initRound()
        self.guessEvent.onRoundFinished.emit()

    def updateData(self, _solution):
        # TODO: if solution already in list of objects, update properties
        #       else: add new object and the stored property values

        self.data.addOrUpdateObject(_solution, self.properties)
        self.data.saveObjects()
        self.data.saveProperties()
