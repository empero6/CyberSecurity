from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QDialog, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, QRect
import sys
import PyQt5.QtGui
from PyQt5.QtGui import QPixmap

class App(QWidget):
    def __init__(self):
        super().__init__()
        title = 'Encryptor/Decryptor Dialogue'
        left = 10
        top = 10
        width = 320
        height = 200

        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)

        # self.initUI()
        self.encrypt()
        self.decrypt()
        self.show()

    def decrypt(self):
        button = QPushButton('Decrypt', self)
        button.setGeometry((QRect(100, 100, 111, 30)))

    def encrypt(self):
        button2 = QPushButton('Encrypt', self)
        button2.clicked.connect(self.open_FileDialog)
        button2.setGeometry(QRect(100, 80, 111, 30))

    def open_FileDialog(self):
        title = 'Hello'
        left = 100
        width = 320
        top = 10
        height = 200
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)

        self.getImage()

    def getImage(self):
        vbox = QVBoxLayout()
        file_Name = QFileDialog.getOpenFileName(self,
                                                '',
                                                '',
                                                '')
        label = QLabel(self)
        image_path = file_Name[0]
        if image_path.lower().endswith(('jpg' or 'txt' or 'mp3')):
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            vbox.addWidget(label)
            self.setLayout(vbox)
            self.show()
        else:
            print('Not a supported format')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
