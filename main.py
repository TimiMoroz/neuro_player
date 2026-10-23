import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer

from app.setup_screen import Setup
from app.main_screen import MainScreen
from app.arduino_reader import Arduino


def shadow(w):
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(25)
    s.setYOffset(5)
    s.setColor(QColor(0, 0, 0, 30))
    w.setGraphicsEffect(s)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Нейро-плеер")
        self.sw = QStackedWidget()
        self.setCentralWidget(self.sw)

        self.setup = Setup()
        self.main = MainScreen()
        self.sw.addWidget(self.setup)
        self.sw.addWidget(self.main)

        self.setup.go.connect(self.start)

        self.ard = Arduino()
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.main.update(self.ard.read()))

        for w in [self.main.card_hz, self.main.card_rh, self.main.card_sl, self.main.graph.parentWidget()]:
            shadow(w)

    def start(self, port, age):
        if self.ard.connect(port):
            self.ard.set_age(age)
            self.main.set_start(age)
            self.main.update(self.main.val)
            self.sw.setCurrentWidget(self.main)
            self.timer.start(100)
        else:
            QMessageBox.critical(self, "Ошибка", "Arduino не найдена!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open("app/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Файл стилей не найден")

    w = App()
    w.showMaximized()
    sys.exit(app.exec())