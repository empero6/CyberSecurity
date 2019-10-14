from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QDialog,QVBoxLayout
from PyQt5.QtCore import pyqtSlot
import sys
import PyQt5.QtGui
from PyQt5.QtGui import QPixmap

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Encryptor/Decryptor Dialogue'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vBox = QVBoxLayout()


        self.btn = QPushButton('File Dialogue')
        self.btn.setFont(PyQt5.QtGui.QFont('Sanserif', 15))
        self.btn.clicked.connect(self.open_FileDialog)
        self.btn.clicked.connect(self.getImage)

        vBox.addWidget(self.btn)
        self.setLayout(vBox)

        #
        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()

        self.show()

    def open_FileDialog(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()',
                                                'Image Files (*);; Image Files (*.jpeg)',
                                                options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, 'QFileDialog.getOpenFileNames()',
                                                '',
                                                'Image Files (*);; Image Files(*.jpeg)',
                                                options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'QFileDialog.getSaveFileName()',
                                                  '',
                                                  'Image Files (*);; Image Files (*jpeg)',
                                                  options=options)
        if fileName:
            print(fileName)

    def getImage(self):
        file_Name = QFileDialog.getOpenFileName(self, 'Open',
                                                '/users/stephenagbenu')
        imagePath = file_Name[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
