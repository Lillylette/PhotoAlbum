import sys
import os

from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLabel, 
                             QLineEdit, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class First_Window(QWidget):
    def __init__(self):
        super().__init__()
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
        self.second_window = Second_Window()  
        self.second_window.show()

    def Third_Window(self):
        self.third_window = Third_Window()  
        self.third_window.show()

class PreviewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Предпросмотр изображения")
        self.setGeometry(600, 300, 600, 400)

        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap.scaled(self.scroll_area.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.show()
        else:
            self.label.setText("Не удалось загрузить изображение")

class Second_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.preview_window = None 
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Добавить фото')

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.button_second = QPushButton("Открыть папку")
        self.button_second.resize(160, 50)
        self.button_second.clicked.connect(self.open_folder)

        self.button_second2 = QPushButton("Добавить в галерею")
        self.button_second2.resize(160, 50)
        self.button_second2.clicked.connect(self.Fourth_Window)

        top_layout.addWidget(self.button_second)
        top_layout.addStretch()
        top_layout.addWidget(self.button_second2)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.preview_image)

        bottom_layout = QHBoxLayout()
        self.button_second3 = QPushButton("Удалить")
        self.button_second3.resize(75, 75)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.button_second3)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        if folder_path:
            self.selected_folder = folder_path
            self.list_widget.clear()
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
            files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
            for file in files:
                self.list_widget.addItem(file)

    def preview_image(self, item):
        if not self.selected_folder:
            return
        image_path = os.path.join(self.selected_folder, item.text())
        if not self.preview_window:
            self.preview_window = PreviewWindow()
        self.preview_window.show_image(image_path)

    def Fourth_Window(self):
        self.fourth_window = Fourth_Window()
        self.fourth_window.show()

class ItemWindow(QWidget):
    """Окно, которое открывается при клике на элемент списка"""
    def __init__(self, item_text):
        super().__init__()
        self.item_text = item_text
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 350, 300, 200)
        self.setWindowTitle(f'Окно: {self.item_text}')
        
        layout = QVBoxLayout()
        
        label = QLabel(f'Вы открыли: {self.item_text}')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.close)
        
        layout.addWidget(label)
        layout.addWidget(close_button)
        
        self.setLayout(layout)


class Third_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 300, 300)
        self.setWindowTitle('Открыть свои фото')


class Fourth_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 350, 350, 200)
        self.setWindowTitle('Добавить в галерею')

        self.button_fourth = QPushButton(self)
        self.button_fourth.resize(150, 50)
        self.button_fourth.move(100, 130)
        self.button_fourth.setText('Добавить')

        self.label = QLabel(self)
        self.label.setText("Введите новые наименования файлов")
        self.label.move(40, 30)

        self.name_input = QLineEdit(self)
        self.name_input.move(80, 70)

        self.number_input = QLineEdit(self)
        self.number_input.resize(50, 26)
        self.number_input.move(222, 70)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = First_Window()
    ex.show()
    sys.exit(app.exec())