
from PyQt6.QtWidgets import (QWidget, QLabel,
                              QVBoxLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


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
