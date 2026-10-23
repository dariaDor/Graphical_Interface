
import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (
    QApplication, QFormLayout, QFrame, QLabel, QLineEdit, QMainWindow,
    QVBoxLayout, QWidget,
)

import cl1
import cl2


class Data:
    def __init__(self):
        self.myData = [0, 0, 0]

    def getData(self):
        return self.myData

    def setData(self, r, g, b):
        self.myData = [r, g, b]


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RGB - HEX converter")
        self.data = Data()

        self.rgbToHex = cl1.RgbToHex()
        self.hexToRgb = cl2.HexToRgb()
        self.rgbToHex.converted.connect(self.showHex)
        self.hexToRgb.converted.connect(self.showRgb)

        self.rEdit = self._makeRgbEdit()
        self.gEdit = self._makeRgbEdit()
        self.bEdit = self._makeRgbEdit()

        self.hexEdit = QLineEdit("#000000")
        self.hexEdit.setMaxLength(7)
        self.hexEdit.setValidator(QRegExpValidator(QRegExp("#?[0-9A-Fa-f]{0,6}")))

        self.preview = QFrame()
        self.preview.setMinimumHeight(60)
        self.preview.setFrameShape(QFrame.Box)
        self._updatePreview()

        form = QFormLayout()
        form.addRow("R (0-255):", self.rEdit)
        form.addRow("G (0-255):", self.gEdit)
        form.addRow("B (0-255):", self.bEdit)
        form.addRow("HEX:", self.hexEdit)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(QLabel("Цвет:"))
        layout.addWidget(self.preview)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        for edit in (self.rEdit, self.gEdit, self.bEdit):
            edit.textEdited.connect(self.onRgbEdited)
        self.hexEdit.textEdited.connect(self.onHexEdited)

    @staticmethod
    def _makeRgbEdit():
        edit = QLineEdit("0")
        edit.setValidator(QIntValidator(0, 255))
        edit.setMaxLength(3)
        return edit

    @staticmethod
    def _toInt(text):
        return int(text) if text else 0

    def onRgbEdited(self):
        r = self._toInt(self.rEdit.text())
        g = self._toInt(self.gEdit.text())
        b = self._toInt(self.bEdit.text())
        self.data.setData(r, g, b)
        self.rgbToHex.convert(r, g, b)

    def onHexEdited(self, text):
        self.hexToRgb.convert(text)

    def showHex(self, hex_value):
        self.hexEdit.setText(hex_value)
        self._updatePreview()

    def showRgb(self, r, g, b):
        self.data.setData(r, g, b)
        self.rEdit.setText(str(r))
        self.gEdit.setText(str(g))
        self.bEdit.setText(str(b))
        self._updatePreview()

    def _updatePreview(self):
        r, g, b = self.data.getData()
        self.preview.setStyleSheet(
            "background-color: rgb({}, {}, {});".format(r, g, b)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())