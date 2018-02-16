class FakeData():
    def __init__(self):
        self.messageHistory = []

        for i in range(10):
            self.addMessage("test")
            self.addMessage("blablabla")
            self.addMessage("test xyz")
            self.addMessage("xyzzy")
            self.addMessage("testitest")

    def addMessage(self, value):
        self.messageHistory.append(value)
