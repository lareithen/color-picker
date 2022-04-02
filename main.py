from PyQt5.QtWidgets import QMainWindow, QShortcut, QApplication, QWidget, QFrame, QGroupBox, QLineEdit, QLabel, QListWidget, QCheckBox, QKeySequenceEdit, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5 import uic
from sys import argv, exit, executable
from threading import Thread
from pyautogui import position, screenshot
from json import loads, dumps

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('picker.ui', self)

        try:
            with open('config.larei', "r", encoding="utf-8") as file:
                conf = loads(file.read())
                self.alwa.setChecked(bool(conf['isChecked']))
                self.hotkey.setKeySequence(conf['hotkey'])
        except FileNotFoundError:
            self.save()

        self.run = True
        self.clipboard = QApplication.clipboard()

        self.savebut.clicked.connect(self.save)
        self.liste.itemClicked.connect(self.kopyala)
        self.shrtct = QShortcut(QKeySequence(self.hotkey.keySequence().toString()), self)
        self.shrtct.activated.connect(self.threadforshrtct)
        self.refreshbut.clicked.connect(self.refresh)

        if self.alwa.isChecked() == True:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()

        self.thread()
        self.show()

    def closeEvent(self, event):
        self.run = False
        event.accept()

    def thread(self):
        self.thr = Thread(target=self.handleColor)
        self.thr.start()

    def threadforshrtct(self):
        self.thr = Thread(target=self.ekle)
        self.thr.start()

    def handleColor(self):
        while self.run:
            x, y = position()
            PIXEL = screenshot(
                region=(
                    x, y, 1, 1
                )
            )

            COLOR = PIXEL.getcolors()
            self.rgbb = COLOR[0][1]
            self.hexx = '#' + ''.join(f'{i:02X}' for i in self.rgbb)
            self.hex.setText(self.hexx)
            self.rgb.setText(str(self.rgbb))
            self.frame.setStyleSheet("*{background-color: %s}" % self.hexx)
            
    def save(self):
        ischeck = self.alwa.isChecked()
        hotkey = self.hotkey.keySequence().toString()

        conf = {
            "isChecked": ischeck,
            "hotkey": hotkey
        }
        with open('config.larei', "w", encoding="utf-8") as file:
            file.write(dumps(conf))

    def ekle(self):
        self.liste.addItem(self.hexx)

    def kopyala(self):
        self.clipboard.setText(self.liste.currentItem().text())

    def refresh(self):
        self.run = False
        QCoreApplication.quit()
        QProcess.startDetached(executable, argv)

obje = QApplication(argv)
p = Window()
p.setWindowTitle("Color Picker")
p.setFixedSize(661, 231)
exit(obje.exec())
