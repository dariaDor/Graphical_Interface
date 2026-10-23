from PyQt5.QtCore import QObject, pyqtSignal


class RgbToHex(QObject):
    converted = pyqtSignal(str)

    @staticmethod
    def _clamp(value):
        return max(0, min(255, value))

    def convert(self, r, g, b):
        r, g, b = (self._clamp(v) for v in (r, g, b))
        hex_value = "#{:02X}{:02X}{:02X}".format(r, g, b)
        self.converted.emit(hex_value)
        return hex_value