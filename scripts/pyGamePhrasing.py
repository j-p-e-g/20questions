import json
from pyGameGlobals import KnowledgeValues

class GamePhrasing():
    def __init__(self):
        self.knowledgeValues = {}
        self.knowledgeValues[KnowledgeValues.UNKNOWN] = "I don't know"
        self.knowledgeValues[KnowledgeValues.YES] = "Yes"
        self.knowledgeValues[KnowledgeValues.NO] = "No"
        self.knowledgeValues[KnowledgeValues.MAYBE] = "It depends"

    def constructInitialPrompt(self):
        return "Think of an object (not an abstract concept)"

    def constructInitialPromptButtonText(self):
        return "Got it!"

    def constructAnswerButtonText(self, _value):
        if _value in self.knowledgeValues:
            return self.knowledgeValues[_value]

        return ""

    def getKnowledgeValueForText(self, _text):
        for val in self.knowledgeValues:
            if self.knowledgeValues[val] == _text:
                return val

        return KnowledgeValues.UNKNOWN

    def constructGuessResponseButtonText(self, _result):
        if _result:
            return "Yes, that's it!"
        else:
            return "No"

    def constructQuestion(self, _modalVerb, _suffix):
        question = _modalVerb.capitalize() + " it " + _suffix + "?"
        return question

    def constructGuess(self, _article, _noun):
        guess = "I think it's " + _article + " " + _noun + "."
        return guess

    def constructSolutionRequest(self):
        return "I give up! What is it?"

    def constructSolutionButtonText(self):
        return "Send"
