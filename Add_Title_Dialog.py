
from PyQt6.QtWidgets import (QPushButton, QLabel, QDialog, 
                             QDateEdit, QLineEdit,  QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import QDate


class AddTitleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить заголовок")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Заголовок:"))
        self.title_edit = QLineEdit()
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)

        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Описание:"))
        self.desc_edit = QLineEdit()
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Дата фотосессии:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Место фотосессии:"))
        self.location_edit = QLineEdit()
        location_layout.addWidget(self.location_edit)
        layout.addLayout(location_layout)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("ОК")
        self.cancel_button = QPushButton("Отмена")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {
            "title": self.title_edit.text().strip(),
            "description": self.desc_edit.text().strip(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "location": self.location_edit.text().strip()
        }
