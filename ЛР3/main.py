import sqlite3
import sys

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QGridLayout, QInputDialog,
                             QMainWindow, QMessageBox, QPushButton, QTableView, QTabWidget,
                             QVBoxLayout, QWidget)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Работа с БД")
        self.resize(900, 600)
        self.con = None

        menu = self.menuBar().addMenu("Меню")
        menu.addAction("Подключить БД", self.connect_db)
        menu.addAction("Разорвать текущее соединение", self.close_db)

        self.query1, self.query2, self.query3, self.query4 = (QPushButton(t) for t in ("Запрос 1", "Запрос 2", "Запрос 3", "Ввести запрос"))
        self.combo = QComboBox()
        self.combo.setPlaceholderText("Colums")

        self.tabs = QTabWidget()
        self.views = [QTableView() for _ in range(6)]
        for i, v in enumerate(self.views, 1):
            v.setEditTriggers(QTableView.NoEditTriggers)
            self.tabs.addTab(v, f"Tab{i}")

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.addWidget(self.query1)
        lay.addWidget(self.query2)
        lay.addWidget(self.query3)
        lay.addWidget(self.combo)
        lay.addWidget(self.query4)
        lay.addWidget(self.tabs)
        self.setCentralWidget(central)

        self.query1.clicked.connect(lambda: self.show_query(1, "SELECT name FROM sqlite_master"))
        self.combo.activated[str].connect(lambda c: self.show_query(2, f'SELECT "{c}" FROM sqlite_master'))
        self.query2.clicked.connect(lambda: self.show_query(3, "SELECT * FROM sqlite_master WHERE type='table'"))
        self.query3.clicked.connect(lambda: self.show_query(4, "SELECT name, tbl_name FROM sqlite_master WHERE type='index'"))
        self.query4.clicked.connect(lambda: self.ask_query(5, "SELECT * FROM sqlite_master"))

    def show_query(self, tab, sql):
        cur = self.con.execute(sql)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([d[0] for d in cur.description or []])
        for row in cur:
            model.appendRow([QStandardItem("" if c is None else str(c)) for c in row])
        self.views[tab].setModel(model)
        self.views[tab].resizeColumnsToContents()
        self.tabs.setCurrentIndex(tab)

    def ask_query(self, tab, default):
        sql, ok = QInputDialog.getMultiLineText(self, f"Запрос -> Tab{tab + 1}", "SQL:", default)
        if ok and sql.strip():
            self.show_query(tab, sql)

    def connect_db(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите БД")
        self.close_db()
        self.con = sqlite3.connect(path)
        self.con.execute("SELECT 1 FROM sqlite_master")
       
        self.combo.addItems(r[1] for r in self.con.execute("PRAGMA table_info(sqlite_master)"))
        self.combo.setCurrentIndex(-1)
        self.show_query(0, "SELECT * FROM sqlite_master")

    def close_db(self):
        if self.con:
            self.con.close()
        self.con = None
        for v in self.views:
            v.setModel(None)
        self.combo.clear()


DB_NAME = "test.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER
        )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
