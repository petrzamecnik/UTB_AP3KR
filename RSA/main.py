import math

import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys



class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 860, 600
        self.resize(width, height)

        # crete widgets
        self.public_key_label = QLabel("Public Key: ")
        self.private_key_label = QLabel("Private Key: ")
        self.value_n_label = QLabel("Value n: ")
        self.value_e_label = QLabel("Value e:")
        self.value_d_label = QLabel("Value d:")
        self.public_key_lineEdit = QLineEdit()
        self.private_key_lineEdit = QLineEdit()
        self.value_n_lineEdit = QLineEdit()
        self.value_e_lineEdit = QLineEdit()
        self.value_d_lineEdit = QLineEdit()



        # edit widgets


        # create layouts
        self.h_layout_main = QHBoxLayout()
        self.v_layout_left = QVBoxLayout()
        self.v_layout_right = QVBoxLayout()

        self.private_key_layout = QHBoxLayout()
        self.public_key_layout = QHBoxLayout()
        self.values_layout = QHBoxLayout()


        # setup layouts
        self.h_layout_main.addLayout(self.v_layout_left)
        self.h_layout_main.addLayout(self.v_layout_right)
        self.v_layout_left.addLayout(self.public_key_layout)
        self.v_layout_left.addLayout(self.private_key_layout)
        self.v_layout_left.addLayout(self.values_layout)

        # add widgets to layouts
        self.public_key_layout.addWidget(self.public_key_label)
        self.public_key_layout.addWidget(self.public_key_lineEdit)
        self.private_key_layout.addWidget(self.private_key_label)
        self.private_key_layout.addWidget(self.private_key_lineEdit)
        self.values_layout.addWidget(self.value_n_label)
        self.values_layout.addWidget(self.value_n_lineEdit)
        self.values_layout.addWidget(self.value_e_label)
        self.values_layout.addWidget(self.value_e_lineEdit)
        self.values_layout.addWidget(self.value_d_label)
        self.values_layout.addWidget(self.value_d_lineEdit)


        self.setLayout(self.h_layout_main)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle("RSA masterpiece")
    sys.exit(app.exec())