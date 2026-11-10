import os
import sys
from datetime import datetime

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Interface(QObject):
    statusChanged = pyqtSignal(str)

    def __init__(self, canvas=None, interval=5, save_dir="saved_canvas"):
        super().__init__()
        self.canvas = canvas
        self.save_dir = save_dir
        self.not_saved = False
        self.result = None

        self._status = f"Автосохранение каждые {interval} с"

        os.makedirs(save_dir, exist_ok=True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save)
        self.timer.start(interval * 1000)

    @pyqtProperty(str, notify=statusChanged)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if self._status != value:
            self._status = value
            self.statusChanged.emit(value)

    @pyqtSlot()
    def set_not_saved(self):
        self.not_saved = True

    def save(self):
        if not self.not_saved:
            return
        self.not_saved = False

        self.result = self.canvas.grabToImage()
        self.result.ready.connect(self.write)

    def write(self):
        now = datetime.now()

        name = now.strftime("canvas_%Y-%m-%d_%H-%M-%S.png")

        if self.result.saveToFile(os.path.join(self.save_dir, name)):
            self.status = f"Сохранено в {now.strftime('%d.%m.%Y в %H:%M:%S')}"
        else:
            self.status = "Ошибка сохранения"


if __name__ == '__main__':

    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()


    interface = Interface(interval=1)
    engine.rootContext().setContextProperty("_backend", interface)

    # Загружаем QML
    engine.load(os.path.join(BASE_DIR, "mainWindow.qml"))

    # Проверка успешной загрузки QML
    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)


    canvas = engine.rootObjects()[0].findChild(QQuickItem, "canvas")    
    interface.canvas = canvas

    sys.exit(app.exec())
