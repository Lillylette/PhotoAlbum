
from PyQt6.QtWidgets import (QPushButton, QMessageBox, QInputDialog, QDialog,
                             QListWidget, QVBoxLayout)



class ProcessingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Обработка")
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.process_list = QListWidget()
        self.process_list.addItems(["Градации серого", "Фильтры"])
        layout.addWidget(self.process_list)
        self.execute_button = QPushButton("Выполнить")
        self.execute_button.clicked.connect(self.execute_processing)
        layout.addWidget(self.execute_button)
        self.setLayout(layout)

    def execute_processing(self):
        selected = self.process_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите обработку")
            return
        if selected == 1:
            self.accept()
            self.result = ("filters", None)
        else:
            new_filename, ok = QInputDialog.getText(self, "Сохранить как", "Введите имя нового файла:")
            if ok and new_filename:
                new_filename = new_filename + ".jpg"
                self.accept()
                self.result = (new_filename, selected)
            else:
                self.result = None