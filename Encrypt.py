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


    #
    # def initUI(self):
    #     self.setWindowTitle(self.title)
    #     self.setGeometry(self.left, self.top, self.width, self.height)
    #
    #     dialog_Box = QVBoxLayout()
    #     dialog_Box2 = QVBoxLayout()
    #
    #     self.btn = QPushButton('Encrypt')
    #     self.btn.clicked.connect(self.open_FileDialog)
    #     dialog_Box.addWidget(self.btn)
    #
    #     self.btn2 = QPushButton('Decrypt')
    #     self.btn2.clicked.connect(self.test)
    #     dialog_Box2.addWidget(self.btn2)
    #
    #     self.label = QLabel()
    #     dialog_Box.addWidget(self.label)
    #     self.setLayout(dialog_Box)
    #     self.show()
    #
    #     self.label2 = QLabel()
    #     dialog_Box2.addWidget(self.label2)
    #     self.setLayout(dialog_Box2)
    #     self.show()
    #
    # def test(self):
    #     self.setWindowTitle(self.title)
    #     self.setGeometry(self.left, self.top, self.width, self.height)
    #     print('2')
    #
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
        file_Name = QFileDialog.getOpenFileName(self,
                                                '',
                                                '',
                                                '')
        imagePath = file_Name[0]
        pixmap = QPixmap(imagePath)
        label.setPixmap(QPixmap(pixmap))
        resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
