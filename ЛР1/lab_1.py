import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class QuickApp(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(400, 400)

        self.label = QLabel("Текст", self)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton("Кнопка", self)

        self.btn.clicked.connect(self.change_to_image)

    def change_to_image(self):
        pixmap = QPixmap("photo.webp").scaled(400,400)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuickApp()
    window.show()
    sys.exit(app.exec_())
