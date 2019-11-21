from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtCore import QRect
import sys
from PyQt5.QtGui import QPixmap


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Encryptor/Decryptor Dialogue'
        self.left = 10
        self.top = 10
        self.width = 250
        self.height = 400

        self.encrypt()
        self.decrypt()
        self.show()

    def decrypt(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        button = QPushButton('Decrypt', self)
        button.setGeometry((QRect(65, 50, 100, 25)))

    def encrypt(self):
        button2 = QPushButton('Encrypt', self)
        button2.clicked.connect(self.open_FileDialog)
        button2.setGeometry(QRect(65, 75, 100, 25))

    def open_FileDialog(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.getImage()


    def getImage(self):
        vbox = QVBoxLayout()
        file_Name = QFileDialog.getOpenFileName(self,
                                                '',
                                                '',
                                                '')
        label = QLabel(self)
        image_path = file_Name[0]
        if image_path.lower().endswith(('jpeg', 'jpg' or 'txt' or 'mp3')):
            pixmap = QPixmap(image_path)
            pixmap2 = pixmap.scaledToHeight(128)
            pixmap3 = pixmap.scaledToWidth(128)
            label.setPixmap(pixmap2)
            vbox.addWidget(label)

            self.setLayout(vbox)

            self.show()
        else:
            print('Not a supported format')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
