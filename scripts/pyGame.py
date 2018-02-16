import sys
import pyGameGUI as gui
import pyGameData as data
from PyQt5.QtWidgets import QApplication

class MainProgram():
    def __init__(self):

        self.data = data.GameData()

        # create basic window widget
        self.main = gui.MainWindow(self.data)


app = QApplication(sys.argv)

program = MainProgram()

# exit when the application is closed
sys.exit(app.exec_())
