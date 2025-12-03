
import os
import shutil
from PyQt6.QtWidgets import (QWidget, QPushButton, QMessageBox, QDialog,
                              QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog)


import Preview_Window as Pw
import Add_Title_Dialog as Atd


class Open_Folders_Photo_Window(QWidget):
    def __init__(self, conn, cursor, GALLERY_DIR):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
        self.GALLERY_DIR = GALLERY_DIR
        self.preview_window = None
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Добавить фото')
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.button_open_folder = QPushButton("Открыть папку")
        self.button_open_folder.clicked.connect(self.open_folder)
        self.button_add_gallery = QPushButton("Добавить в галерею")
        self.button_add_gallery.clicked.connect(self.add_to_gallery)
        top_layout.addWidget(self.button_open_folder)
        top_layout.addStretch()
        top_layout.addWidget(self.button_add_gallery)
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.preview_image)
        bottom_layout = QHBoxLayout()
        self.button_delete = QPushButton("Удалить")
        self.button_delete.clicked.connect(self.delete_selected_photo)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.button_delete)
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
            self.preview_window = Pw.PreviewWindow()
        self.preview_window.show_image(image_path)
    
    def delete_selected_photo(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите фотографию для удаления")
            return
        self.list_widget.takeItem(self.list_widget.row(selected_item))


    def add_to_gallery(self):
        if not self.selected_folder or self.list_widget.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите папку с фотографиями")
            return

        dialog = Atd.AddTitleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            title, description, title_date, title_location = data["title"], data["description"], data["date"], data["location"]

            if not title or not title_date:
                QMessageBox.warning(self, "Ошибка", "Заголовок и дата обязательны")
                return

            self.cursor.execute('PRAGMA foreign_keys = ON;')

            self.cursor.execute("""
                INSERT OR REPLACE INTO titles (title, description, title_date, title_location)
                VALUES (?, ?, ?, ?)
            """, (title, description, title_date, title_location))
            self.conn.commit()

            self.cursor.execute("SELECT id FROM titles WHERE title = ?", (title,))
            row = self.cursor.fetchone()
            if not row:
                QMessageBox.critical(self, "Ошибка", "Не удалось получить ID заголовка")
                return
            title_id = row[0]

            if not os.path.exists(self.GALLERY_DIR):
                os.makedirs(self.GALLERY_DIR)

            for i in range(self.list_widget.count()):
                file_name = self.list_widget.item(i).text()
                src_path = os.path.join(self.selected_folder, file_name)
                dst_path = os.path.join(self.GALLERY_DIR, file_name)

                try:
                    shutil.copy2(src_path, dst_path)
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO photos (file_name, photo_date, title_id, comment)
                        VALUES (?, ?, ?, ?)
                    """, (file_name, title_date, title_id, ""))
                except Exception as e:
                    print(f"Ошибка копирования или записи для файла {file_name}: {e}")

            self.conn.commit()
            QMessageBox.information(self, "Успех", f"Фотографии добавлены с заголовком '{title}'")