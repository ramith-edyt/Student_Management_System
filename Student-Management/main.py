from PyQt6.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QGridLayout, QWidget, QLineEdit,
                             QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar,
                             QMessageBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3

class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connection(self):
        connect = sqlite3.connect(self.database_file)
        return connect



class MainWinodow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        self.setMinimumSize(900, 700)

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Adding toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        #Create a status bar adding elements into it
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        #Detect a click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_record(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        about_message = QMessageBox()
        about_message.setWindowTitle("About Us")
        content = """
        This is a simple web app created to manage student details. 
        Its been implemented using the PYQT6 python library,
        which is really efficient and easy to use.
        
        """
        about_message.setText(content)
        about_message.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Data")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        # Getting student name from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        #Getting student id
        self.student_id = main_window.table.item(index, 0).text()

        #Adding name box
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #Adding a dropdown/combobox for courses
        self.course_name = QComboBox()
        course_name = main_window.table.item(index, 2).text()
        courses = ["Biology", "OOP in Python", "Java", "SoftSkills", "English"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Adding mobile number box
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        #Adding a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE students set name=?, course=?, mobile=? WHERE id=? ",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete student record")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_record)

    def delete_record(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connect = DatabaseConnection().connection()
        cursor = connect.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        connect.commit()
        cursor.close()
        connect.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record successfully deleted")
        confirmation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Data")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        #Adding name box
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #Adding a dropdown/combobox for courses
        self.course_name = QComboBox()
        courses = ["Biology", "OOP in Python", "Java", "SoftSkills", "English"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Adding mobile number box
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        #Adding a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connect = DatabaseConnection().connection()
        cursor = connect.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)",
                       (name, course, mobile))

        connect.commit()
        cursor.close()
        connect.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = DatabaseConnection().connection()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = list(result)[0]
        print(row)
        items = main_window.table.findItems("John Smith", Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWinodow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
