import json
from enum import Enum

class KnowledgeValues(Enum):
    UNKNOWN = 0
    YES = 1
    NO = 2
    MAYBE = 3

class GameData():
    def __init__(self):
        self.objectsDataFileName = "data/objects.json"
        self.propertiesDataFileName = "data/properties.json"
        self.objectsMainAttribute = "objects"
        self.propertiesMainAttribute = "properties"
        self.requiredObjectAttributes = ["name", "article", "properties"]
        self.requiredPropertyAttributes = ["identifier", "modal_verb", "suffix"]

        self.objects = {}
        self.properties = {}
        self.propertyValues = {}
        self.messageHistory = []

        self.setupPropertyValues()
        self.initData()
        self.setupFakeMessageHistory()

    def initData(self):
        # self.setupFakeObjectsData()
        # self.saveObjects()

        # self.setupFakePropertiesData()
        # self.saveProperties()

        self.readObjects()
        self.printObjects()
        # self.saveObjects()

        self.readProperties()
        self.printProperties()
        # self.saveProperties()

    def setupPropertyValues(self):
        self.propertyValues[KnowledgeValues.UNKNOWN] = "unknown"
        self.propertyValues[KnowledgeValues.YES] = "yes"
        self.propertyValues[KnowledgeValues.NO] = "no"
        self.propertyValues[KnowledgeValues.MAYBE] = "it depends"

    # current session messages
    def addMessage(self, value):
        self.messageHistory.append(value)

    def setupFakeMessageHistory(self):
        for i in range(10):
            self.addMessage("test")
            self.addMessage("blablabla")
            self.addMessage("test xyz")
            self.addMessage("xyzzy")
            self.addMessage("testitest")

    # read/write object data
    def readObjects(self):
        try:
            with open(self.objectsDataFileName) as infile:
                self.objects = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + self.objectsDataFileName + "!")

    def setupFakeObjectsData(self):
        self.objects[self.objectsMainAttribute] = []

        properties = []
        properties.append({
            "identifier": 12563,
            "value": 1
        })
        properties.append({
            "identifier": 7269,
            "value": 2
        })

        self.objects[self.objectsMainAttribute].append({
            "name": "airplane",
            "article": "an",
            "properties": properties
        })

        properties = []
        properties.append({
            "identifier": 7269,
            "value": 1
        })

        self.objects[self.objectsMainAttribute].append({
            "name": "banana",
            "article": "a",
            "properties": properties
        })

        properties = []
        properties.append({
            "identifier": 12563,
            "value": 0
        })

        self.objects[self.objectsMainAttribute].append({
            "name": "moon",
            "article": "the",
            "properties": properties
        })

        self.printObjects()

    def printObjects(self):
        if self.objectsMainAttribute in self.objects:
            count = 0
            for obj in self.objects[self.objectsMainAttribute]:
                count = count + 1
                skip = False
                for attr in self.requiredObjectAttributes:
                    if not attr in obj:
                        print("Warning: Missing key '" + attr + "' for entry " + str(count) + " in " + self.objectsDataFileName)
                        skip = True

                if not skip:
                    print(obj["article"] + " " + obj["name"])

        else:
            print("ERROR: Missing '" + self.objectsMainAttribute + "' key in " + self.objectsDataFileName)

    def saveObjects(self):
        with open(self.objectsDataFileName, "w") as outfile:
            json.dump(self.objects, outfile, indent=4)

    # read/write properties data
    def readProperties(self):
        try:
            with open(self.propertiesDataFileName) as infile:
                self.properties = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + self.propertiesDataFileName + "!")

    def setupFakePropertiesData(self):
        self.properties[self.propertiesMainAttribute] = []

        self.properties[self.propertiesMainAttribute].append({
            "identifier": 12563,
            "modal_verb": "can",
            "suffix": "fly"
        })
        self.properties[self.propertiesMainAttribute].append({
            "identifier": 7269,
            "modal_verb": "is",
            "suffix": "a type of fruit"
        })

        self.printProperties()

    def printProperties(self):
        if self.propertiesMainAttribute in self.properties:
            count = 0
            for prop in self.properties[self.propertiesMainAttribute]:
                count = count + 1
                skip = False
                for attr in self.requiredPropertyAttributes:
                    if not attr in prop:
                        print("Warning: Missing key '" + attr + "' for entry " + str(count) + " in " + self.propertiesDataFileName)
                        skip = True

                if not skip:
                    print(str(prop["identifier"]) + " " + prop["modal_verb"] + " " + prop["suffix"])

        else:
            print("ERROR: Missing '" + self.propertiesMainAttribute + "' key in " + self.propertiesDataFileName)

    def saveProperties(self):
        with open(self.propertiesDataFileName, "w") as outfile:
            json.dump(self.properties, outfile, indent=4)
