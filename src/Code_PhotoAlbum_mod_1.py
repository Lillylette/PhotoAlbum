import sys
import os
import sqlite3
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLabel, QMessageBox, QInputDialog,
                             QLineEdit, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap





def init_database(db_filename='photos_app.db'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS titles (
            title TEXT PRIMARY KEY,
            description TEXT,
            title_date TEXT,
            title_location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE,
            photo_date TEXT,
            title_id TEXT,
            comment TEXT,
            FOREIGN KEY (title_id) REFERENCES titles(title) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    return conn, cursor, base_dir

conn, cursor, BASE_DIR = init_database()
GALLERY_DIR = os.path.join(BASE_DIR, "Gallery")

class First_Window(QWidget):
    def __init__(self, conn, cursor):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
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
        self.third_window = Third_Window(self.conn, self.cursor, GALLERY_DIR)  
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
            self.preview_window = PreviewWindow()
        self.preview_window.show_image(image_path)

    def add_to_gallery(self):
        if not self.selected_folder or self.list_widget.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите папку с фотографиями")
            return

        title, ok = QInputDialog.getText(self, "Введите заголовок", "Заголовок для всех фотографий:")
        if not ok or not title.strip():
            QMessageBox.warning(self, "Ошибка", "Заголовок обязателен для записи")
            return
        title = title.strip()

        # Добавляем или обновляем заголовок в таблице titles
        title_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT OR IGNORE INTO titles (title, description, title_date, title_location)
            VALUES (?, ?, ?, ?)
        """, (title, "", title_date, ""))

        conn.commit()

        if not os.path.exists(GALLERY_DIR):
            os.makedirs(GALLERY_DIR)

        for i in range(self.list_widget.count()):
            file_name = self.list_widget.item(i).text()
            src_path = os.path.join(self.selected_folder, file_name)
            dst_path = os.path.join(GALLERY_DIR, file_name)

            try:
                shutil.copy2(src_path, dst_path)  # копируем файл с метаданными
                photo_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("""
                    INSERT OR IGNORE INTO photos (file_name, photo_date, title_id, comment)
                    VALUES (?, ?, ?, ?)
                """, (file_name, photo_date, title, ""))
            except Exception as e:
                print(f"Ошибка копирования или записи для файла {file_name}: {e}")

        conn.commit()
        QMessageBox.information(self, "Успех", f"Фотографии успешно добавлены в галерею с заголовком '{title}'")

    

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

        self.photos_list = QListWidget()
        self.photos_list.itemDoubleClicked.connect(self.on_photo_double_clicked)

        self.layout.addWidget(self.title_list)
        self.layout.addWidget(self.photos_list)

        self.load_titles()

    def load_titles(self):
        self.title_list.clear()
        self.cursor.execute("SELECT title FROM titles ORDER BY title")
        titles = self.cursor.fetchall()
        for (title,) in titles:
            self.title_list.addItem(title)

    def on_title_double_clicked(self, item):
        title = item.text()
        self.photos_list.clear()
        self.cursor.execute("SELECT file_name FROM photos WHERE title_id = (SELECT title FROM titles WHERE title = ?) ORDER BY file_name", (title,))
        photos = self.cursor.fetchall()
        if not photos:
            self.photos_list.addItem("Фотографии с таким заголовком отсутствуют")
            return
        for (file_name,) in photos:
            self.photos_list.addItem(file_name)

    def on_photo_double_clicked(self, item):
        file_name = item.text()
        image_path = os.path.join(self.gallery_folder, file_name)
        if not self.preview_window:
            self.preview_window = PreviewWindow()
        self.preview_window.show_image(image_path)


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
    conn, cursor, BASE_DIR = init_database()
    app = QApplication(sys.argv)
    ex = First_Window(conn, cursor)
    ex.show()
    sys.exit(app.exec())