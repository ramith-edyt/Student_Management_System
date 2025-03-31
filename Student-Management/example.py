from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QGridLayout, QWidget, QLineEdit
import sys
from datetime import datetime


class CalculateAge(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()
        #width = 700
        #height = 500
        #self.setFixedWidth(width)
        #self.setFixedHeight(height)

        name_label = QLabel("Name ")
        self.name_label_edit = QLineEdit()

        date_of_birth = QLabel("Date Of Birth DD/MM/YYYY ")
        self.date_of_birth_name_label_edit = QLineEdit()

        calculate_age_button = QPushButton("Calculate Age")
        calculate_age_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel()

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_label_edit, 0, 1)
        grid.addWidget(date_of_birth, 1, 0)
        grid.addWidget(self.date_of_birth_name_label_edit, 1, 1)
        grid.addWidget(calculate_age_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        try:
            current_year = datetime.now().year
            date_of_birth = self.date_of_birth_name_label_edit.text()
            year = datetime.strptime(date_of_birth, "%d/%m/%Y").date().year
            if year > current_year:
                self.output_label.setText("The date is invalid. Enter a valid one")
            else:
                age = current_year - year
                self.output_label.setText(f"The age of {self.name_label_edit.text()} is {age} ")
        except ValueError:
            self.output_label.setText("The input date format is incorrect. Type it in DD/MM/YYYY")


app = QApplication(sys.argv)
age_calculator = CalculateAge()
age_calculator.show()
sys.exit(app.exec())
