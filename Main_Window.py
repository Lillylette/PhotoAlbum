
from PyQt6.QtWidgets import QWidget, QPushButton

import Open_Folders_Photo_Window as Ofpw
import Gallery_Photo_Window as Gpw


class Main_Window(QWidget):
    def __init__(self, conn, cursor, GALLERY_DIR):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
        self.GALLERY_DIR = GALLERY_DIR
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 400, 400)
        self.setWindowTitle('Первое окно')
        self.button_1 = QPushButton(self)
        self.button_1.resize(150, 150)
        self.button_1.move(25, 110)
        self.button_1.clicked.connect(self.Second_Window)
        self.button_1.setText("Добавить фото")
        self.button_2 = QPushButton(self)
        self.button_2.resize(150, 150)
        self.button_2.move(225, 110)
        self.button_2.clicked.connect(self.Third_Window)
        self.button_2.setText("Открыть свои фото")

    def Second_Window(self):
        self.second_window = Ofpw.Open_Folders_Photo_Window(self.conn, self.cursor, self.GALLERY_DIR)
        self.second_window.show()

    def Third_Window(self):
        self.third_window = Gpw.Gallery_Photo_Window(self.conn, self.cursor, self.GALLERY_DIR)
        self.third_window.show()