import math
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import numpy as np


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 860, 600
        self.resize(width, height)

        # crete widgets
        self.public_key_label = QLabel("Public Key --> ")
        self.private_key_label = QLabel("Private Key --> ")
        self.public_key_label_n = QLabel("( n )")
        self.public_key_label_e = QLabel("( e )")
        self.private_key_label_n = QLabel("( n )")
        self.private_key_label_d = QLabel("( d )")
        self.value_n_label = QLabel("Value n: ")
        self.value_e_label = QLabel("Value e:")
        self.value_d_label = QLabel("Value d:")
        self.value_n_lineEdit = QLineEdit()
        self.value_e_lineEdit = QLineEdit()
        self.value_d_lineEdit = QLineEdit()
        self.input_textEdit = QTextEdit()
        self.output_textEdit = QTextEdit()

        self.public_key_label_n_lineEdit = QLineEdit()
        self.public_key_label_e_lineEdit = QLineEdit()
        self.private_key_label_n_lineEdit = QLineEdit()
        self.private_key_label_d_lineEdit = QLineEdit()

        self.encrypt_button = QPushButton()
        self.decrypt_button = QPushButton()
        self.generate_keys_button = QPushButton()



        # edit widgets
        self.input_textEdit.setPlaceholderText("Input ...")
        self.output_textEdit.setPlaceholderText("Output ...")
        self.public_key_label_n_lineEdit.setPlaceholderText("n value")
        self.public_key_label_e_lineEdit.setPlaceholderText("e value")
        self.private_key_label_n_lineEdit.setPlaceholderText("n value")
        self.private_key_label_d_lineEdit.setPlaceholderText("d value")
        self.encrypt_button.setText("Encrypt")
        self.decrypt_button.setText("Decrypt")
        self.generate_keys_button.setText("Generate Keys")

        # create layouts
        self.h_layout_main = QHBoxLayout()
        self.v_layout_left = QVBoxLayout()
        self.v_layout_right = QVBoxLayout()

        self.private_key_layout = QHBoxLayout()
        self.public_key_layout = QHBoxLayout()
        self.values_layout = QHBoxLayout()
        self.io_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()



        # setup layouts
        self.h_layout_main.addLayout(self.v_layout_left)
        self.h_layout_main.addLayout(self.v_layout_right)
        self.v_layout_right.addLayout(self.public_key_layout)
        self.v_layout_right.addLayout(self.private_key_layout)
        self.v_layout_right.addLayout(self.values_layout)
        self.v_layout_left.addLayout(self.io_layout)   
        self.v_layout_left.addLayout(self.io_layout)
        self.v_layout_right.addLayout(self.button_layout)
        


        # add widgets to layouts
        self.public_key_layout.addWidget(self.public_key_label)
        self.public_key_layout.addWidget(self.public_key_label_n)
        self.public_key_layout.addWidget(self.public_key_label_n_lineEdit)
        self.public_key_layout.addWidget(self.public_key_label_e)
        self.public_key_layout.addWidget(self.public_key_label_e_lineEdit)
        self.private_key_layout.addWidget(self.private_key_label)
        self.private_key_layout.addWidget(self.private_key_label_n)
        self.private_key_layout.addWidget(self.private_key_label_n_lineEdit)
        self.private_key_layout.addWidget(self.private_key_label_d)
        self.private_key_layout.addWidget(self.private_key_label_d_lineEdit)
        

        self.values_layout.addWidget(self.value_n_label)
        self.values_layout.addWidget(self.value_n_lineEdit)
        self.values_layout.addWidget(self.value_e_label)
        self.values_layout.addWidget(self.value_e_lineEdit)
        self.values_layout.addWidget(self.value_d_label)
        self.values_layout.addWidget(self.value_d_lineEdit)
        self.io_layout.addWidget(self.input_textEdit)
        self.io_layout.addWidget(self.output_textEdit)
        self.button_layout.addWidget(self.encrypt_button)
        self.button_layout.addWidget(self.decrypt_button)
        self.button_layout.addWidget(self.generate_keys_button)


        self.setLayout(self.h_layout_main)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle("RSA masterpiece")
    sys.exit(app.exec())