
import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QMessageBox, QDialog,
                             QListWidget, QVBoxLayout, QHBoxLayout)
from PIL import Image

import Photo_Comment_Window as Pcw
import Processing_Dialog as Pd
import Filter_Selection_Dialog as Fsd
import Filter_Preview_Dialog as Fpd

def grayscale_image(src_path, dst_path):
    img = Image.open(src_path)
    gray_img = img.convert('L')
    gray_img.save(dst_path)

class Gallery_Photo_Window(QWidget):
    def __init__(self, conn, cursor, GALLERY_DIR):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
        self.gallery_folder = GALLERY_DIR
        self.preview_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Заголовки и фотографии")
        self.setGeometry(350, 350, 600, 400)
        self.layout = QVBoxLayout(self)

        self.title_list = QListWidget()
        self.title_list.itemDoubleClicked.connect(self.on_title_double_clicked)
        self.layout.addWidget(self.title_list)

        self.photos_list = QListWidget()
        self.photos_list.itemDoubleClicked.connect(self.on_photo_double_clicked)
        self.layout.addWidget(self.photos_list)

        button_layout = QHBoxLayout()
        self.delete_photo_button = QPushButton("Удалить фотографию")
        self.delete_photo_button.clicked.connect(self.delete_selected_photo)
        self.delete_session_button = QPushButton("Удалить фотосессию")
        self.delete_session_button.clicked.connect(self.delete_selected_session)
        self.process_button = QPushButton("Обработать изображение")
        self.process_button.clicked.connect(self.open_processing_dialog)

        button_layout.addWidget(self.delete_photo_button)
        button_layout.addWidget(self.delete_session_button)
        button_layout.addWidget(self.process_button)
        self.layout.addLayout(button_layout)

        self.load_titles()

    def load_titles(self):
        self.title_list.clear()
        self.cursor.execute("SELECT title, description, title_date, title_location FROM titles ORDER BY title")
        titles = self.cursor.fetchall()
        for title, description, title_date, title_location in titles:
            display_text = f"{title} | {description} | {title_date} | {title_location}"
            self.title_list.addItem(display_text)

    def on_title_double_clicked(self, item):
        title = item.text().split(" | ")[0]
        self.photos_list.clear()
        self.cursor.execute("SELECT file_name FROM photos WHERE title_id = (SELECT id FROM titles WHERE title = ?) ORDER BY file_name", (title,))
        photos = self.cursor.fetchall()
        if not photos:
            self.photos_list.addItem("Фотографии с таким заголовком отсутствуют")
            return
        for (file_name,) in photos:
            self.photos_list.addItem(file_name)

    def on_photo_double_clicked(self, item):
        file_name = item.text()
        image_path = os.path.join(self.gallery_folder, file_name)
        self.cursor.execute("SELECT comment FROM photos WHERE file_name = ?", (file_name,))
        comment_row = self.cursor.fetchone()
        current_comment = comment_row[0] if comment_row and comment_row[0] else ""

        def save_callback(new_comment):
            self.cursor.execute("UPDATE photos SET comment = ? WHERE file_name = ?", (new_comment, file_name))
            self.conn.commit()

        if not hasattr(self, 'photo_comment_window') or not self.photo_comment_window.isVisible():
            self.photo_comment_window = Pcw.PhotoCommentWindow()
        self.photo_comment_window.update_photo(image_path, current_comment, file_name, save_callback)
        self.photo_comment_window.show()


    def delete_selected_photo(self):
        selected_item = self.photos_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите фотографию")
            return
        filename = selected_item.text()
        filepath = os.path.join(self.gallery_folder, filename)
        self.cursor.execute("DELETE FROM photos WHERE file_name=?", (filename,))
        self.conn.commit()
        if os.path.exists(filepath):
            os.remove(filepath)
        self.photos_list.takeItem(self.photos_list.row(selected_item))


    def delete_selected_session(self):
        selected_item = self.title_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите фотосессию для удаления")
            return
        title = selected_item.text().split(" | ")[0]
        self.cursor.execute("SELECT file_name FROM photos WHERE title_id = (SELECT id FROM titles WHERE title = ?)", (title,))
        photos = self.cursor.fetchall()
        for (file_name,) in photos:
            file_path = os.path.join(self.gallery_folder, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        self.cursor.execute("DELETE FROM photos WHERE title_id = (SELECT id FROM titles WHERE title = ?)", (title,))
        self.cursor.execute("DELETE FROM titles WHERE title = ?", (title,))
        self.conn.commit()
        self.load_titles()
        self.photos_list.clear()
    
    def open_processing_dialog(self):
        selected_item = self.photos_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите изображение")
            return
        filename = selected_item.text()
        src_path = os.path.join(self.gallery_folder, filename)
        if not os.path.exists(src_path):
            QMessageBox.warning(self, "Ошибка", "Файл не найден")
            return
        self.cursor.execute("SELECT photo_date, title_id, comment FROM photos WHERE file_name=?", (filename,))
        row = self.cursor.fetchone()
        if not row:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить данные")
            return
        photo_date, title_id, comment = row

        dialog = Pd.ProcessingDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = dialog.result
            if result[0] == "filters":
                filter_dialog = Fsd.FilterSelectionDialog(self)
                if filter_dialog.exec() == QDialog.DialogCode.Accepted:
                    filter_name = filter_dialog.filter_combo.currentText()
                    preview_dialog = Fpd.FilterPreviewDialog(src_path, filter_name, self)
                    if preview_dialog.exec() == QDialog.DialogCode.Accepted:
                        new_filename = preview_dialog.new_filename
                        dst_path = os.path.join(self.gallery_folder, new_filename)
                        self.cursor.execute("INSERT INTO photos (file_name, photo_date, title_id, comment) VALUES (?, ?, ?, ?)",
                                            (new_filename, photo_date, title_id, comment))
                        self.conn.commit()
                        QMessageBox.information(self, "Готово", f"Файл {new_filename} добавлен")
                        self.on_title_double_clicked(self.title_list.currentItem())
            else:
                new_filename, process_type = result
                dst_path = os.path.join(self.gallery_folder, new_filename)
                if process_type == 0: 
                    grayscale_image(src_path, dst_path)
                    self.cursor.execute("INSERT INTO photos (file_name, photo_date, title_id, comment) VALUES (?, ?, ?, ?)",
                                        (new_filename, photo_date, title_id, comment))
                    self.conn.commit()
                    QMessageBox.information(self, "Готово", f"Файл {new_filename} добавлен")
                    self.on_title_double_clicked(self.title_list.currentItem())
                else:
                    return