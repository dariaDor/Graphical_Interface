from PyQt5.QtCore import QObject, pyqtSignal


class HexToRgb(QObject):
    converted = pyqtSignal(int, int, int)

    def convert(self, hex_value):
        hex_value = hex_value.strip().lstrip("#")
        if len(hex_value) != 6:
            return None
        
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)

        self.converted.emit(r, g, b)
        return r, g, b