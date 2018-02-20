from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyGameGlobals import *
from StateGUI.pyGameBoxLayoutWidget import *


class DisambiguationStateWidget(QWidget):
    def __init__(self, _logic, _newObjName, _oldObjName):
        super().__init__()

        self.logic = _logic
        self.data = self.logic.data
        self.messageHistory = self.logic.messageHistory
        self.phrasing = self.data.phrasing

        self.displayDisambiguationState(_newObjName, _oldObjName)

    def displayDisambiguationState(self, _newObjName, _oldObjName):
        query = self.phrasing.constructDisambiguationRequest(_newObjName, _oldObjName)
        self.messageHistory.addProgramMessage(query)

        queryLabel = QLabel(query, self)
        queryLabel.setFont(QFont("Arial", 14))
        queryLabel.setStyleSheet("QLabel { color : blue; }");

        emptyLabel = QLabel("", self)

        self.sentenceStart = _newObjName.capitalize()
        sentenceStartLabel = QLabel(self.sentenceStart, self)
        sentenceStartLabel.setFont(QFont("Arial", 12))

        self.verbComboBox = QComboBox()
        self.verbComboBox.setFont(QFont("Arial", 12))
        self.verbComboBox.addItem("can")
        self.verbComboBox.addItem("does")
        self.verbComboBox.addItem("is")
        self.verbComboBox.currentIndexChanged.connect(self.onVerbComboBoxIndexChanged)

        self.toggleNotButton = QPushButton("(not)", self)
        self.toggleNotButton.setFont(QFont("Arial", 12))
        self.toggleNotButton.setStyleSheet("color: gray")
        self.toggleNotButton.setCheckable(True)
        self.toggleNotButton.setMaximumWidth(50)
        self.toggleNotButton.clicked[bool].connect(self.onToggledNotButton)

        hLayoutStart = QHBoxLayout()
        hLayoutStart.setSpacing(5)
        hLayoutStart.addStretch(1)
        hLayoutStart.addWidget(sentenceStartLabel)
        hLayoutStart.addWidget(self.verbComboBox)
        hLayoutStart.addWidget(self.toggleNotButton)
        hLayoutStart.addStretch(1)

        sentenceStartWidget = QWidget(self)
        sentenceStartWidget.setLayout(hLayoutStart)

        # allow the player to either choose from a dropdown menu of existing objects, or add a new one
        self.suffixComboBox = QComboBox()
        self.suffixComboBox.setFont(QFont("Arial", 12))
        self.fillSuffixComboBox()
        self.suffixComboBox.currentIndexChanged.connect(self.onSuffixComboBoxIndexChanged)

        orLabel = QLabel("or", self)
        orLabel.setFont(QFont("Arial", 12))
        orLabel.setAlignment(Qt.AlignCenter)

        self.suffixTextBox = QLineEdit(self)
        self.suffixTextBox.setFont(QFont("Arial", 12))
        self.suffixTextBox.textChanged.connect(self.onTextInputChanged)

        sizePolicy = self.suffixTextBox.sizePolicy();
        sizePolicy.setHorizontalStretch(1);
        self.suffixTextBox.setSizePolicy(sizePolicy);

        sentenceEndLabel = QLabel(".", self)
        sentenceEndLabel.setFont(QFont("Arial", 12))

        hLayoutEnd = QHBoxLayout()
        hLayoutEnd.setSpacing(5)
        hLayoutEnd.addWidget(self.suffixTextBox)
        hLayoutEnd.addWidget(sentenceEndLabel)

        sentenceEndWidget = QWidget(self)
        sentenceEndWidget.setLayout(hLayoutEnd)

        vLayout = QVBoxLayout()
        vLayout.addWidget(sentenceStartWidget)
        vLayout.addWidget(self.suffixComboBox)
        vLayout.addWidget(orLabel)
        vLayout.addWidget(sentenceEndWidget)

        sentenceWidget = QWidget(self)
        sentenceWidget.setLayout(vLayout)

        buttonSendText = self.phrasing.constructDisambiguationButtonText()
        self.sendButton = QPushButton(buttonSendText, self)
        self.sendButton.setFont(QFont("Arial", 12))
        self.sendButton.clicked.connect(self.onPropertySent)
        self.sendButton.setEnabled(False)

        skipButtonText = self.phrasing.constructSkipDisambiguationButtonText()
        skipButton = QPushButton(skipButtonText, self)
        skipButton.setFont(QFont("Arial", 12))
        skipButton.clicked.connect(self.onSkipDisambiguation)

        layout = QStackedLayout()
        self.setLayout(layout)

        widget = BoxWidget([queryLabel, emptyLabel, sentenceWidget, self.sendButton, emptyLabel, emptyLabel, emptyLabel, skipButton])
        layout.addWidget(widget)

    def onVerbComboBoxIndexChanged(self, index):
        # update suffix dropdown menu every time the modal verb changes
        self.fillSuffixComboBox()

    def fillSuffixComboBox(self):
        modalVerb = self.verbComboBox.currentText()

        self.suffixComboBox.clear()
        self.suffixComboBox.addItem("(existing attribute)")

        # add new entries
        propertyList = self.data.getListOfAllSuffixesMatchingVerb(modalVerb)

        for suffix in propertyList:
            self.suffixComboBox.addItem(suffix)

    def onToggledNotButton(self, _down):
        if _down:
            self.toggleNotButton.setText("NOT")
            self.toggleNotButton.setStyleSheet("color: red")
        else:
            self.toggleNotButton.setText("(not)")
            self.toggleNotButton.setStyleSheet("color: gray")

    def onSuffixComboBoxIndexChanged(self, index):
        if index != 0:
            self.suffixTextBox.setText("")

        self.updateSendButton()

    def onTextInputChanged(self):
        if self.suffixTextBox.text() != "":
            self.suffixComboBox.setCurrentIndex(0)

        self.updateSendButton()

    def updateSendButton(self):
        if self.suffixComboBox.currentIndex() > 0:
            self.sendButton.setEnabled(True)
        else:
            isEmpty = (self.suffixTextBox.text() == "")
            self.sendButton.setEnabled(not isEmpty)

    def onPropertySent(self):
        modalVerb, notValue, suffix = self.getValues()

        self.messageHistory.addPlayerMessage(self.getFullSentence(modalVerb, notValue, suffix))

        self.logic.inputEvent.onPropertySent.emit(modalVerb, notValue, suffix)
        self.close()

    def getValues(self):
        modalVerb = self.verbComboBox.currentText()

        notValue = False
        if self.toggleNotButton.isChecked():
            notValue = True

        if self.suffixComboBox.currentIndex() > 0:
            suffix = self.suffixComboBox.currentText()
        else:
            suffix = self.suffixTextBox.text()

        return modalVerb, notValue, suffix

    def getFullSentence(self, modalVerb, notValue, suffix):
        notText = " "
        if notValue:
            notText = " not "

        fullSentence = self.sentenceStart + " " + modalVerb + notText + suffix + "."
        return fullSentence

    def onSkipDisambiguation(self):
        buttonText = self.sender().text()
        self.messageHistory.addPlayerMessage(buttonText)
        self.logic.inputEvent.onRestart.emit()
        self.close()