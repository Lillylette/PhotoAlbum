
from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, 
                             QVBoxLayout, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap



class PhotoCommentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Предпросмотр и комментарий")
        self.resize(600, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.text_edit = QTextEdit()
        self.layout.addWidget(QLabel("Комментарий:"))
        self.layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Записать комментарий")
        self.save_button.clicked.connect(self.save_comment)
        self.layout.addWidget(self.save_button)

        self.current_file = None
        self.save_callback = None

    def update_photo(self, image_path, comment, file_name, save_callback):
        self.current_file = file_name
        self.save_callback = save_callback
        self.text_edit.setPlainText(comment)
        self.show_image(image_path)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap.scaled(self.scroll_area.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.label.setText("Не удалось загрузить изображение")

    def save_comment(self):
        if self.current_file and self.save_callback:
            new_comment = self.text_edit.toPlainText()
            self.save_callback(new_comment)