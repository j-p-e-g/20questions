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

    # helper methods
    def isArticle(self, word):
        return word == "a" or word == "an" or word == "the"

    def isVowel(self, char):
        return char == 'a' or char == 'e' or char == 'i' or char == 'o'

    def splitStringIntoArticleAndNoun(self, _str):
        elements = _str.split()
        article = ""
        noun = _str

        if len(elements) > 1:
            if self.isArticle(elements[0]):
                article = elements[0]
                noun = " ".join(elements[1:len(elements)])

        if article == "":
            if self.isVowel(noun[0]):
                article = "an"
            else:
                article = "a"

        print(_str + " split into '" + article + "' and '" + noun + "'")
        return article, noun
