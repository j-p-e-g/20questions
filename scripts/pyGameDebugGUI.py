from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyGameGlobals import *
import pyGameScrollBarGUI as scrollBar


class DebugPropertyTab(scrollBar.ScrollBar):
    def __init__(self, _logic, _scrollToBottom):
        super().__init__(_scrollToBottom)

        self.logic = _logic
        self.data = self.logic.data
        self.phrasing = self.data.phrasing

        self.logic.debugEvent.onPropertiesUpdated.connect(self.displayProperties)

        self.displayProperties()

    def displayProperties(self):
        display = []

        triedProperties = {}
        untriedProperties = {}

        for prop in self.logic.properties:
            propEntry = self.logic.properties[prop]
            if propEntry["tried"]:
                triedProperties[prop] = propEntry
            else:
                untriedProperties[prop] = propEntry

        # first add properties that already got asked (sort by order they were asked)
        display.append("<h3>Asked</h3>")

        def sortByNum(value):
            key, dict = value
            return dict["order"]

        for propId, propEntry in sorted(triedProperties.items(), key = sortByNum):
            orderDesc = str(propEntry["order"]) + ". "

            question = orderDesc + self.data.constructQuestion(propId) + "</b> (" + str(propId) + ")"
            display.append("<h4>" + question + "</h4>")

            value = propEntry["value"]
            objects = propEntry["objects"]

            color = "black"
            if value == KnowledgeValues.YES:
                color = "green"
            elif value == KnowledgeValues.NO:
                color = "red"

            answerText = "<font color=\"" + color + "\">" + self.phrasing.getTextForKnowledgeValue(value) + "</font>"

            excludedObjectNames = ""
            if value == KnowledgeValues.NO and len(objects[self.logic.yesValueText]) > 0:
                excludedObjectNames = ", ".join(objects[self.logic.yesValueText])
            elif value == KnowledgeValues.YES and len(objects[self.logic.noValueText]) > 0:
                excludedObjectNames = ", ".join(objects[self.logic.noValueText])

            if excludedObjectNames != "":
                display.append(answerText + ": <s>" + excludedObjectNames + "</s>")
            else:
                display.append(answerText)

        # then add the remaining properties (sort by score)
        display.append("<hr>")
        display.append("<h3>Other</h3>")

        def sortByScore(value):
            key, dict = value
            return dict["score"]

        for propId, propEntry in sorted(untriedProperties.items(), key = sortByScore, reverse = True):
            question = self.data.constructQuestion(propId) + " (" + str(propId) + ")"
            display.append("<h4>" + question + "</h4>")
            display.append("Score: " + "{:.2f}".format(propEntry["score"]))

            objects = propEntry["objects"]
            if len(objects[self.logic.yesValueText]) > 0:
                display.append(self.logic.yesValueText + ": " + ", ".join(objects[self.logic.yesValueText]))
            if len(objects[self.logic.noValueText]) > 0:
                display.append(self.logic.noValueText + ": " + ", ".join(objects[self.logic.noValueText]))

        self.update(display)

class DebugObjectTab(scrollBar.ScrollBar):
    def __init__(self, _logic, _scrollToBottom):
        super().__init__(_scrollToBottom)

        self.logic = _logic
        self.data = self.logic.data
        self.phrasing = self.data.phrasing

        self.logic.debugEvent.onObjectsUpdated.connect(self.displayObjects)
        self.logic.debugEvent.onPropertiesUpdated.connect(self.displayObjects)

        self.displayObjects()

    def displayObjects(self):
        display = []

        def sortByScore(value):
            key, dict = value
            return dict["score"]

        for objName, objEntry in sorted(self.logic.objects.items(), key = sortByScore, reverse = True):
            if objName in self.logic.guesses:
                display.append("<s><h3>" + objName + "</h3></s>")
                display = self.displayObject(display, objEntry)

        display.append("<hr>")
        for objName, objEntry in sorted(self.logic.objects.items(), key = sortByScore, reverse = True):
            if not objName in self.logic.guesses:
                display.append("<h3>" + objName + "</h3>")
                display = self.displayObject(display, objEntry)

        self.update(display)

    def displayObject(self, _display, _objEntry):
        yesValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.YES)
        noValueText = self.phrasing.getTextForKnowledgeValue(KnowledgeValues.NO)

        objScore = _objEntry["score"]
        objProperties = _objEntry["properties"]

        _display.append("<b>Score: " + "{:.2f}".format(objScore) + "</b>")

        for prop in objProperties[yesValueText]:
            propEntry = self.logic.properties[prop]

            color = "black"
            value = propEntry["value"]
            if value == KnowledgeValues.YES:
                color = "green"
            elif value == KnowledgeValues.NO:
                color = "red"

            desc = "<font color=\"" + color + "\">\t" + propEntry["desc"] + " : " + yesValueText + "</font>"
            _display.append(desc)

        for prop in objProperties[noValueText]:
            propEntry = self.logic.properties[prop]

            color = "black"
            value = propEntry["value"]
            if value == KnowledgeValues.NO:
                color = "green"
            elif value == KnowledgeValues.YES:
                color = "red"

            desc = "<font color=\"" + color + "\">\t" + propEntry["desc"] + " : " + noValueText + "</font>"
            _display.append(desc)

        return _display


# window capable of showing debug information
class DebugWindow(QTabWidget):
    def __init__(self, _mainWindow, _logic):
        super().__init__()

        self.mainWindow = _mainWindow

        self.initMe(_logic)
        self.show()

    def initMe(self, _logic):
        global PROGRAM_ICON_PATH

        # pos(x, y), size(width, height)
        self.setGeometry(50, 300, 300, 300)
        self.setWindowTitle("Debug window")
        self.setWindowIcon(QIcon(PROGRAM_ICON_PATH))

        tabObj = DebugObjectTab(_logic, False)
        tabProp = DebugPropertyTab(_logic, False)
        self.addTab(tabObj, "Objects")
        self.addTab(tabProp, "Properties")


    def closeEvent(self, event):
        self.mainWindow.onDebugWindowClosed()
        event.accept()  # let the window close
