import sys
import pyqrcode
import pyperclip
from PIL import Image
from pyzbar.pyzbar import decode
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sqlalchemy import except_all

app = QApplication(sys.argv)

class ShortCutsWindow(QMainWindow):
    def __init__(self):
        super(ShortCutsWindow, self).__init__()
        uic.loadUi("shortcuts.ui", self)

        self.actionQuit.triggered.connect(lambda x: ShortCutsWindow.close())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("mainwindow.ui", self)

        self.gen.clicked.connect(self.generate)
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.generate)
        self.actionSave.triggered.connect(self.generate)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+E'), self)
        self.shortcut_open.activated.connect(self.open)
        self.actionOpen.triggered.connect(self.open)

        self.actionCopy.triggered.connect(self.copy)

        self.actionShortCuts.triggered.connect(self.shortcuts)

        self.qr = None
        self.data = None

    def generate(self):
        text = self.text.text()

        if text:
            self.qr = pyqrcode.create(text)

            fname = QFileDialog.getSaveFileName(self, "Save file", "", "Image Files (*.png)")
            try:
                self.qr.png(fname[0], scale=8)
                
                msg = QMessageBox()
                msg.setWindowTitle("Plik zapisany")
                msg.setText(f"Plik zostaał zapisany w  '{fname[0]}'")
                msg.setIcon(QMessageBox.Information)
                
                msg.exec_()

                self.text.setText("")
            except:
                pass

    def open(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "", "Image Files (*.png)")
        try:
            self.data = decode(Image.open(fname[0]))
            self.data = self.data[0].data.decode("utf-8")

            self.IMAGE.setText(self.data)

            self.copy()
        except:
            pass

    def copy(self):
        msg = QMessageBox()
        msg.setWindowTitle("Copying")
        msg.setText("Do you want to copy the text from QR?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)

        button = msg.exec_()
        if button == QMessageBox.Ok:
            if self.data:
                pyperclip.copy(self.data)

    def shortcuts(self):
        msg = QMessageBox()
        msg.setWindowTitle("Shortcuts")
        msg.setText("List of shortcuts: \n\n - Save -> Ctrl + S \n - Open -> Ctrl + E")
        msg.setIcon(QMessageBox.Information)
        
        msg.exec_()

def main():
    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()