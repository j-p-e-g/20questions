import json
from pyGameGlobals import KnowledgeValues

OBJECTS_DATA_FILE = "data/objects.json"
PROPERTIES_DATA_FILE  = "data/properties.json"
OBJECTS_REQUIRED_ATTRIBUTES = ["name", "article", "properties"]
PROPERTIES_REQUIRED_ATTRIBUTES = ["identifier", "modal_verb", "suffix"]

class GameData():
    def __init__(self):
        self.requiredObjectAttributes = OBJECTS_REQUIRED_ATTRIBUTES
        self.requiredPropertyAttributes = PROPERTIES_REQUIRED_ATTRIBUTES

        self.objectsMainAttribute = "objects"
        self.propertiesMainAttribute = "properties"

        self.objects = {}
        self.properties = {}
        self.propertyValues = {}

        self.setupPropertyValues()
        self.initData()

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

    # read/write object data
    def readObjects(self):
        try:
            with open(OBJECTS_DATA_FILE) as infile:
                self.objects = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + OBJECTS_DATA_FILE + "!")

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
                        print("Warning: Missing key '" + attr + "' for entry " + str(count) + " in " + OBJECTS_DATA_FILE)
                        skip = True

                if not skip:
                    print(obj["article"] + " " + obj["name"])

        else:
            print("ERROR: Missing '" + self.objectsMainAttribute + "' key in " + OBJECTS_DATA_FILE)

    def saveObjects(self):
        print("saving objects")
        with open(OBJECTS_DATA_FILE, "w") as outfile:
            json.dump(self.objects, outfile, indent=4)

    # read/write properties data
    def readProperties(self):
        try:
            with open(PROPERTIES_DATA_FILE) as infile:
                self.properties = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + PROPERTIES_DATA_FILE + "!")

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
                        print("Warning: Missing key '" + attr + "' for entry " + str(count) + " in " + PROPERTIES_DATA_FILE)
                        skip = True

                if not skip:
                    print(str(prop["identifier"]) + " " + prop["modal_verb"] + " " + prop["suffix"])

        else:
            print("ERROR: Missing '" + self.propertiesMainAttribute + "' key in " + PROPERTIES_DATA_FILE)

    def saveProperties(self):
        print("saving properties")
        with open(PROPERTIES_DATA_FILE, "w") as outfile:
            json.dump(self.properties, outfile, indent=4)

    def constructQuestion(self, _propIdentifier):
        for prop in self.properties[self.propertiesMainAttribute]:
            if prop["identifier"] == _propIdentifier:
                question = prop["modal_verb"].capitalize() + " it " + prop["suffix"] + "?"
                return question

        return ""

    def constructGuess(self, _objectName):
        for prop in self.objects[self.objectsMainAttribute]:
            if prop["name"] == _objectName:
                guess = "I think it's " + prop["article"] + " " + prop["name"] + "."
                return guess

        return ""
