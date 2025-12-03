
import os
from PyQt6.QtWidgets import (QPushButton, QLabel, QInputDialog, QDialog,
                            QLineEdit, QVBoxLayout, QHBoxLayout, QScrollArea,)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageFilter


class FilterPreviewDialog(QDialog):
    def __init__(self, image_path, filter_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предпросмотр фильтра")
        self.resize(800, 600)
        self.image_path = image_path
        self.filter_name = filter_name
        self.original_image = Image.open(image_path)
        self.filtered_image = self.original_image.copy()
        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        self.param_layout = QHBoxLayout()
        self.param_label = QLabel("Параметр:")
        self.param_edit = QLineEdit("3")
        self.param_edit.textChanged.connect(self.update_preview)
        self.param_layout.addWidget(self.param_label)
        self.param_layout.addWidget(self.param_edit)
        layout.addLayout(self.param_layout)
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.update_preview()

    def update_preview(self):
        try:
            param = int(self.param_edit.text())
            if param < 1:
                param = 3
            elif param % 2 == 0:
                param += 1
            elif param > 31:
                param = 31
        except ValueError:
            param = 3
        if self.filter_name == "BLUR":
            self.filtered_image = self.original_image.filter(ImageFilter.BLUR)
        elif self.filter_name == "BoxBlur":
            self.filtered_image = self.original_image.filter(ImageFilter.BoxBlur(param))
        elif self.filter_name == "GaussianBlur":
            self.filtered_image = self.original_image.filter(ImageFilter.GaussianBlur(param))
        elif self.filter_name == "CONTOUR":
            self.filtered_image = self.original_image.filter(ImageFilter.CONTOUR)
        elif self.filter_name == "DETAIL":
            self.filtered_image = self.original_image.filter(ImageFilter.DETAIL)
        elif self.filter_name == "EDGE_ENHANCE":
            self.filtered_image = self.original_image.filter(ImageFilter.EDGE_ENHANCE)
        elif self.filter_name == "EDGE_ENHANCE_MORE":
            self.filtered_image = self.original_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif self.filter_name == "EMBOSS":
            self.filtered_image = self.original_image.filter(ImageFilter.EMBOSS)
        elif self.filter_name == "FIND_EDGES":
            self.filtered_image = self.original_image.filter(ImageFilter.FIND_EDGES)
        elif self.filter_name == "SMOOTH":
            self.filtered_image = self.original_image.filter(ImageFilter.SMOOTH)
        elif self.filter_name == "SMOOTH_MORE":
            self.filtered_image = self.original_image.filter(ImageFilter.SMOOTH_MORE)
        elif self.filter_name == "SHARPEN":
            self.filtered_image = self.original_image.filter(ImageFilter.SHARPEN)
        elif self.filter_name == "UnsharpMask":
            self.filtered_image = self.original_image.filter(ImageFilter.UnsharpMask(radius=param))
        elif self.filter_name == "RankFilter":
            self.filtered_image = self.original_image.filter(ImageFilter.RankFilter(param, rank=param))
        elif self.filter_name == "MedianFilter":
            self.filtered_image = self.original_image.filter(ImageFilter.MedianFilter(size=param))
        elif self.filter_name == "MinFilter":
            self.filtered_image = self.original_image.filter(ImageFilter.MinFilter(size=param))
        elif self.filter_name == "MaxFilter":
            self.filtered_image = self.original_image.filter(ImageFilter.MaxFilter(size=param))
        elif self.filter_name == "ModeFilter":
            self.filtered_image = self.original_image.filter(ImageFilter.ModeFilter(size=param))
        self.show_image(self.filtered_image)

    def show_image(self, img):
        pixmap = QPixmap()
        img.save("temp_preview.jpg", "JPEG")
        pixmap.load("temp_preview.jpg")
        self.label.setPixmap(pixmap.scaled(self.scroll_area.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def save_image(self):
        new_filename, ok = QInputDialog.getText(self, "Сохранить как", "Введите имя нового файла:")
        if ok and new_filename:
            new_filename = new_filename + ".jpg"
            self.filtered_image.save(os.path.join(self.parent().gallery_folder, new_filename))
            self.accept()
            self.new_filename = new_filename