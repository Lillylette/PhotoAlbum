
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton


class FilterSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор фильтра")
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "BLUR", "BoxBlur", "GaussianBlur", "CONTOUR", "DETAIL", "EDGE_ENHANCE",
            "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "SMOOTH", "SMOOTH_MORE",
            "SHARPEN", "UnsharpMask", "RankFilter", "MedianFilter",
            "MinFilter", "MaxFilter", "ModeFilter"
        ])
        layout.addWidget(QLabel("Фильтр:"))
        layout.addWidget(self.filter_combo)
        self.select_button = QPushButton("Выбрать")
        self.select_button.clicked.connect(self.accept)
        layout.addWidget(self.select_button)
        self.setLayout(layout)