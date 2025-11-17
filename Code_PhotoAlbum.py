
import sys

from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit


class First_Window(QWidget):
    def __init__(self):
        super().__init__()
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
        self.third_window = Third_Window()  
        self.third_window.show()



class Second_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Добавить фото')

        self.button_second = QPushButton(self)
        self.button_second.resize(160, 50)
        self.button_second.move(30, 15)
        self.button_second.setText('Открыть папку')

        self.button_second2 = QPushButton(self)
        self.button_second2.resize(160, 50)
        self.button_second2.move(310, 15)
        self.button_second2.setText('Добавить в галерею')
        self.button_second2.clicked.connect(self.Fourth_Window)

        self.button_second3 = QPushButton(self)
        self.button_second3.resize(75, 75)
        self.button_second3.move(410, 310)
        self.button_second3.setText('Удалить')

    def Fourth_Window(self):
        self.fourth_window = Fourth_Window()  
        self.fourth_window.show()


class Third_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 300, 300)
        self.setWindowTitle('Открыть свои фото')



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
    app = QApplication(sys.argv)
    ex = First_Window()
    ex.show()
    sys.exit(app.exec())
