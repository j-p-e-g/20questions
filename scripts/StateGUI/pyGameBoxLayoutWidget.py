from PyQt5.QtWidgets import *


class BoxWidget(QWidget):
    def __init__(self, _widgets):
        super().__init__()

        vLayout = QVBoxLayout()
        vLayout.setSpacing(5)
        vLayout.addStretch(1)

        for widget in _widgets:
            vLayout.addWidget(widget)

        vLayout.addStretch(1)

        hLayout = QHBoxLayout()
        hLayout.setSpacing(5)
        hLayout.addStretch(1)
        hLayout.addLayout(vLayout)
        hLayout.addStretch(1)

        self.setLayout(hLayout)
