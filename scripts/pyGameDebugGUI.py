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

        # first add properties that already got asked
        display.append("<h3>Asked</h3>")

        for prop in self.logic.properties:
            propEntry = self.logic.properties[prop]
            if propEntry["tried"]:
                display.append(self.constructPropertyDisplay(prop, propEntry))

        # then add the remaining properties
        # TODO: sort by probability (?)
        display.append("<hr>")
        display.append("<h3>Other</h3>")

        for prop in self.logic.properties:
            propEntry = self.logic.properties[prop]
            if not propEntry["tried"]:
                display.append(self.constructPropertyDisplay(prop, propEntry))

        self.update(display)

    def constructPropertyDisplay(self, _identifier, _data):
        question = self.data.constructQuestion(_identifier) + " (" + str(_identifier) + ")"

        value = _data["value"]
        color = "black"
        if value == KnowledgeValues.YES:
            color = "green"
        elif value == KnowledgeValues.NO:
            color = "red"

        answerText = self.phrasing.constructAnswerButtonText(_data["value"])
        answer = "<font color=\"" + color + "\">" + answerText + "</font>"

        line = question + " : " + answer
        return line


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

        tabObj = QWidget()
        tabProp = DebugPropertyTab(_logic, False)
        self.addTab(tabObj, "Objects")
        self.addTab(tabProp, "Properties")


    def closeEvent(self, event):
        self.mainWindow.onDebugWindowClosed()
        event.accept()  # let the window close
