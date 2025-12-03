import sys
import os
import sqlite3
from PyQt6.QtWidgets import QApplication


import Main_Window as MW


def init_database(db_filename='photos_app.db'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
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
            title_id INTEGER,
            comment TEXT,
            FOREIGN KEY (title_id) REFERENCES titles(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    return conn, cursor, base_dir

conn, cursor, BASE_DIR = init_database()
GALLERY_DIR = os.path.join(BASE_DIR, "Gallery")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MW.Main_Window(conn, cursor, GALLERY_DIR)
    ex.show()
    sys.exit(app.exec())
