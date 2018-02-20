import json
from pyGamePhrasing import *
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

        self.phrasing = GamePhrasing()

        self.objects = {}
        self.properties = {}
        self.highestPropertyId = 0

        self.latestObject = ""

        self.initData()

    def initData(self):
        self.readObjects()
        self.printObjects()

        self.readProperties()
        self.printProperties()

    # read/write object data
    def readObjects(self):
        try:
            with open(OBJECTS_DATA_FILE) as infile:
                self.objects = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + OBJECTS_DATA_FILE + "!")

    def addOrUpdateObject(self, _name, _allProperties):

        article, noun = self.phrasing.splitStringIntoArticleAndNoun(_name)
        self.latestObject = noun

        for obj in self.objects[self.objectsMainAttribute]:
            if obj["name"] == noun:
                # the object already exists -> update properties

                _objProperties = []

                # replace existing property values
                for prop in obj["properties"]:
                    identifier = prop["identifier"]
                    if identifier in _allProperties:
                        _objProperties.append(identifier)
                        value = _allProperties[identifier]["value"]
                        if value != prop["value"]:
                            if value == KnowledgeValues.YES or value == KnowledgeValues.NO:
                                prop["value"] = value

                # add new properties
                for propId in _allProperties:
                    if propId not in _objProperties:
                        value = _allProperties[propId]["value"]
                        if value == KnowledgeValues.YES or value == KnowledgeValues.NO:
                            obj["properties"].append({
                                "identifier": propId,
                                "value": value
                            })

                return

        # not already in the dictionary, so it's a new object
        # TODO: validate _name (?)
        properties = []
        for prop in _allProperties:
            tempPropEntry = _allProperties[prop]
            if not tempPropEntry["tried"]:
                continue

            if tempPropEntry["value"] != KnowledgeValues.UNKNOWN:
                propEntry = {}
                propEntry["identifier"] = prop
                propEntry["value"] = tempPropEntry["value"]
                properties.append(propEntry)

        newObject = {}
        newObject["article"] = article
        newObject["name"] = noun
        newObject["properties"] = properties

        self.objects[self.objectsMainAttribute].append(newObject)

    def printObjects(self):
        print("Objects:")
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
                    print(" - " + obj["article"] + " " + obj["name"])

        else:
            print("ERROR: Missing '" + self.objectsMainAttribute + "' key in " + OBJECTS_DATA_FILE)

    def saveObjects(self):
        with open(OBJECTS_DATA_FILE, "w") as outfile:
            json.dump(self.objects, outfile, indent=4)

    # read/write properties data
    def readProperties(self):
        try:
            with open(PROPERTIES_DATA_FILE) as infile:
                self.properties = json.load(infile)
        except FileNotFoundError:
            print("ERROR: Trying to open non-existing file " + PROPERTIES_DATA_FILE + "!")

        # update property id counter
        if self.propertiesMainAttribute in self.properties:
            for prop in self.properties[self.propertiesMainAttribute]:
                if prop["identifier"] > self.highestPropertyId:
                    self.highestPropertyId = prop["identifier"]
        else:
            print("ERROR: Missing '" + self.propertiesMainAttribute + "' key in " + PROPERTIES_DATA_FILE)

    def addOrUpdateProperty(self, _modalVerb, _suffix, _yesObjName, _noObjName):

        identifier = 0
        for prop in self.properties[self.propertiesMainAttribute]:
            if prop["modal_verb"] == _modalVerb and prop["suffix"] == _suffix:
                # the property already exists
                identifier = prop["identifier"]
                break

        if identifier == 0:
            self.highestPropertyId = self.highestPropertyId + 1
            identifier = self.highestPropertyId

            propEntry = {}
            propEntry["identifier"] = identifier
            propEntry["modal_verb"] = _modalVerb
            propEntry["suffix"] = _suffix

            self.properties[self.propertiesMainAttribute].append(propEntry)

        # update object properties
        changeCount = 0
        for obj in self.objects[self.objectsMainAttribute]:
            if obj["name"] != _yesObjName and obj["name"] != _noObjName:
                continue

            propEntry = {}
            propEntry["identifier"] = identifier

            if obj["name"] == _yesObjName:
                propEntry["value"] = KnowledgeValues.YES
            else:
                propEntry["value"] = KnowledgeValues.NO

            properties = obj["properties"]
            for prop in properties:
                if prop["identifier"] == identifier:
                    # update existing property
                    prop["value"] = propEntry["value"]
                    return

            obj["properties"].append(propEntry)

            changeCount = changeCount + 1
            if changeCount == 2:
                return

    def printProperties(self):
        print("Properties:")
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
                    print(" - " + prop["modal_verb"] + " " + prop["suffix"] + " (" + str(prop["identifier"]) + ")")

        else:
            print("ERROR: Missing '" + self.propertiesMainAttribute + "' key in " + PROPERTIES_DATA_FILE)

    def saveProperties(self):
        with open(PROPERTIES_DATA_FILE, "w") as outfile:
            json.dump(self.properties, outfile, indent=4)

    def getNameWithArticle(self, _objectName):
        for prop in self.objects[self.objectsMainAttribute]:
            if prop["name"] == _objectName:
                return prop["article"] + " " + prop["name"]

        return ""

    def constructQuestion(self, _propIdentifier):
        for prop in self.properties[self.propertiesMainAttribute]:
            if prop["identifier"] == _propIdentifier:
                return self.phrasing.constructQuestion(prop["modal_verb"], prop["suffix"])

        return ""

    def constructGuess(self, _objectName):
        for prop in self.objects[self.objectsMainAttribute]:
            if prop["name"] == _objectName:
                return self.phrasing.constructGuess(prop["article"], prop["name"])

        return ""
