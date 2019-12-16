import sys
import Updated_encrypt
import re
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.load_image_btn = QPushButton("Browse Encrypted")
        self.load_image_btn.clicked.connect(self.load_image)

        self.load_image2_btn = QPushButton("Browse UnEncrypted")
        self.load_image2_btn.clicked.connect(self.load_image2)

        self.image_lbl = QLabel()
        lay = QVBoxLayout(self)
        
        lay.addWidget(self.load_image_btn)
        lay.addWidget(self.image_lbl)

        lay.addWidget(self.load_image2_btn)
        lay.addWidget(self.image_lbl)                                

    def load_image(self):      
        image_path, _ = QFileDialog.getOpenFileName(self, "OpenFile", "", "")
        if image_path:
            updatedImage = Updated_encrypt.decrypt(image_path, 123, 59, 46, 16,0.8110155663012353, 0.8627450980392157, 1.673760664340451 )
            pixmap = QPixmap(updatedImage)
            self.image_lbl.setPixmap(QPixmap(pixmap))
            
            
    def load_image2(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "OpenFile", "", "")
        if image_path:
            updatedImage = Updated_encrypt.encrypt(image_path, 123)
            QPixmap(updatedImage)
            self.image_lbl.setPixmap(QPixmap(pixmap))
            
class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = "Encrypt/Decrypt"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(200, 500, 400, 300)

        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.clicked.connect(self.openSecondDialog)

        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.openSecondDialog)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.encrypt_btn)
        vbox.addWidget(self.decrypt_btn)

    def openSecondDialog(self):
        dialog = Dialog(self)
        dialog.show()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
