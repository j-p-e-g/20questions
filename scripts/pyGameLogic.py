from PyQt5.QtCore import QObject, pyqtSignal

import pyGameMessageHistory as msgHistory
from pyGameGlobals import *


class InputEvent(QObject):
    onGameStart = pyqtSignal()
    onQuestionAnswered = pyqtSignal(str)
    onGuessReaction = pyqtSignal(bool)
    onSolutionSent = pyqtSignal(str)
    onPropertySent = pyqtSignal(str, bool, str)
    onRestart = pyqtSignal()


class GuessEvent(QObject):
    onGuessSent = pyqtSignal(str)
    onQuestionSent = pyqtSignal(str)
    onRequestSolution = pyqtSignal()
    onRequestDisambiguation = pyqtSignal(str, str)
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
        self.debugObjectScore = False
        self.debugPropertyScore = False

        self.numCurrentRound = 0
        self.numCurrentQuestion = 0
        self.numCurrentGuess = 0

        self.guessEvent = GuessEvent()
        self.inputEvent = InputEvent()
        self.debugEvent = DebugEvent()

        self.inputEvent.onGameStart.connect(self.startRound)
        self.inputEvent.onQuestionAnswered.connect(self.onReceivedQuestionAnswer)
        self.inputEvent.onGuessReaction.connect(self.onReceivedGuessResponse)
        self.inputEvent.onSolutionSent.connect(self.onReceivedSolution)
        self.inputEvent.onPropertySent.connect(self.onReceivedDisambiguation)
        self.inputEvent.onRestart.connect(self.onRestart)

        self.debugEvent.onObjectsUpdated.connect(self.updateScores)
        self.debugEvent.onPropertiesUpdated.connect(self.updateScores)

        self.yesValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        self.noValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)
        self.maybeValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.MAYBE)

        self.initRound()

    def initRound(self):
        self.numCurrentRound = self.numCurrentRound + 1
        self.messageHistory.addFormattedMessage("Round " + str(self.numCurrentRound), "green")

        self.previousQuestion = 0
        self.numCurrentQuestion = 0
        self.numCurrentGuess = 0

        self.guesses = []
        self.objectCandidates = []

        self.initProperties()
        self.initObjects()

        # send these now that both sets have been initialized
        self.debugEvent.onObjectsUpdated.emit()
        self.debugEvent.onPropertiesUpdated.emit()

    def updateScores(self):
        self.updateObjectScore()
        self.updatePropertyScore()

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

            propEntry["score"] = 0

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

            objEntry["score"] = 0

            self.objects[name] = objEntry

    def updatePropertyScore(self):
        if self.debugPropertyScore:
            print("\nupdatePropertyScore")

        countTotalObjects = len(self.objects) + 2

        for propId in self.properties:
            propEntry = self.properties[propId]

            objects = propEntry["objects"]
            countYes = 1
            countNo = 1

            for objYes in objects[self.yesValueText]:
                if objYes in self.objectCandidates:
                    countYes = countYes + 1

            for objNo in objects[self.noValueText]:
                if objNo in self.objectCandidates:
                    countNo = countNo + 1

            score = (countYes/countTotalObjects) * (countNo/countTotalObjects)
            propEntry["score"] = score

            if self.debugPropertyScore:
                print("\t" + propEntry["desc"] + " (" + str(propId) + ")")
                print("\t\t#countYes: " + str(countYes))
                print("\t\t#countNo: " + str(countNo))
                print("\t==> score: " + str(score) + "\n")

    def updateObjectScore(self):
        if self.debugObjectScore:
            print("\nupdateObjectScore")

        # increase total count by 1 to ensure we never divide by zero
        countTotalProperties = len(self.properties) + 1

        for objId in self.objects:
            countMatches = 0
            countMismatches = 0

            objEntry = self.objects[objId]
            objProperties = objEntry["properties"]
            for yespropid in objProperties[self.yesValueText]:
                if yespropid in self.properties:
                    propEntry = self.properties[yespropid]
                    value = propEntry["value"]
                    if value == KnowledgeValues.YES:
                        countMatches = countMatches + 1
                    elif value == KnowledgeValues.NO:
                        countMismatches = countMismatches + 1

            for nopropid in objProperties[self.noValueText]:
                if nopropid in self.properties:
                    propEntry = self.properties[nopropid]
                    value = propEntry["value"]
                    if value == KnowledgeValues.YES:
                        countMismatches = countMismatches + 1
                    elif value == KnowledgeValues.NO:
                        countMatches = countMatches + 1

            matchRatio = countMatches/countTotalProperties
            mismatchRatio = 1 - (countMismatches/countTotalProperties)
            score = (countTotalProperties * mismatchRatio + matchRatio)/(countTotalProperties+1)
            objEntry["score"] = score

            if self.debugObjectScore:
                print("\t" + objId)
                print("\t\t#matches: " + str(countMatches))
                print("\t\t#mismatches: " + str(countMismatches))
                print("\t\t#matchRatio: " + str(matchRatio))
                print("\t\t#mismatchRatio: " + str(mismatchRatio))
                print("\t==> score: " + str(score) + "\n")

    def startRound(self):
        self.nextRun()

    def nextRun(self):

        # 1. iterate over all properties for the current guess
        # 2. assign weights to each object
        # 3. if there's a single object matching all properties, guess!
        # 4. otherwise, ask a question that hasn't been asked before
        # 5. when you run out of questions, guess
        # 6. if neither asking nor guessing are possible (or make sense) anymore, ask for the solution

        if self.numCurrentGuess < MAX_NUM_GUESSES and len(self.objectCandidates) == 1:
            if self.setupGuess(self.objectCandidates[0]):
                return

        # ask questions to narrow down the solution space
        if self.numCurrentQuestion < MAX_NUM_QUESTIONS and self.tryFindGoodQuestion():
            return

        # guess the object
        if self.numCurrentGuess < MAX_NUM_GUESSES and self.tryFindGoodGuess():
            return

        # if nothing else works, ask for the solution
        self.guessEvent.onRequestSolution.emit()

    def tryFindGoodQuestion(self):
        bestProperty = -1
        bestScore = -1

        for identifier in self.properties:
            propEntry = self.properties[identifier]
            if propEntry["tried"]:
                continue

            score = propEntry["score"]
            if score > bestScore:
                bestProperty = identifier
                bestScore = score

        if bestProperty == -1:
            return False

        question = self.data.constructQuestion(bestProperty)
        if question != "":
            self.previousQuestion = bestProperty

            self.numCurrentQuestion = self.numCurrentQuestion + 1
            self.messageHistory.addProgramMessage(str(self.numCurrentQuestion) + ". question: " + question)
            self.guessEvent.onQuestionSent.emit(question)

            propEntry = self.properties[bestProperty]
            propEntry["order"] = self.numCurrentQuestion

            self.debugEvent.onPropertiesUpdated.emit()
            return True

        return False

    def tryFindGoodGuess(self):
        bestGuess = ""
        bestScore = -1

        for objName in self.objectCandidates:
            if objName in self.guesses:
                continue

            if objName in self.objects:
                score = self.objects[objName]["score"]
                if score > bestScore:
                    bestScore = score
                    bestGuess = objName

        if bestGuess == "":
            return False

        return self.setupGuess(bestGuess)

    def setupGuess(self, bestGuess):
        guessText = self.data.constructGuess(bestGuess)
        if guessText == "":
            return False

        self.guesses.append(bestGuess)

        self.numCurrentGuess = self.numCurrentGuess + 1
        self.messageHistory.addProgramMessage(str(self.numCurrentGuess) + ". guess: " + guessText)
        self.guessEvent.onGuessSent.emit(guessText)

        # self.debugEvent.onObjectsUpdated.emit()
        return True

    def onRestart(self):
        self.initRound()
        self.guessEvent.onRoundFinished.emit()

    def onReceivedQuestionAnswer(self, _buttonText):
        value = self.data.phrasing.getKnowledgeValueForText(_buttonText)

        if self.previousQuestion in self.properties:
            propEntry = self.properties[self.previousQuestion]
            propEntry["value"] = value
            propEntry["tried"] = True

            # If the player answered yes or no, remove all objects with the opposite value
            # from the list of candidates.
            if value == KnowledgeValues.YES:
                for objName in propEntry["objects"][self.noValueText]:
                    if objName in self.objectCandidates:
                        self.objectCandidates.remove(objName)
            elif value == KnowledgeValues.NO:
                for objName in propEntry["objects"][self.yesValueText]:
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
            self.onRestart()
        else:
            # keep asking
            if prevGuess in self.objectCandidates:
                self.objectCandidates.remove(prevGuess)

            self.nextRun()

    def onReceivedSolution(self, _solution):
        self.updateData(_solution)

        if self.data.latestObject != "" and len(self.guesses) > 0:

            self.bestGuess = self.guesses[0]
            if self.data.latestObject != self.bestGuess:
                newObj = self.data.getNameWithArticle(self.data.latestObject)
                oldObj = self.data.getNameWithArticle(self.bestGuess)
                self.guessEvent.onRequestDisambiguation.emit(newObj, oldObj)
                return

        self.onRestart()

    def onReceivedDisambiguation(self, _modalVerb, _negatedForNewObject, _suffix):
        if _negatedForNewObject:
            yesObjName = self.bestGuess
            noObjName = self.data.latestObject
        else:
            yesObjName = self.data.latestObject
            noObjName = self.bestGuess

        # add to properties, update objects
        self.data.addOrUpdateProperty(_modalVerb, _suffix, yesObjName, noObjName)
        self.data.saveObjects()
        self.data.saveProperties()

        self.onRestart()

    def updateData(self, _solution):
        self.data.addOrUpdateObject(_solution, self.properties)
        self.data.saveObjects()
