import random
import Cryptodome.Util.number
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import json


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 860, 600
        self.resize(width, height)

        # crete widgets
        self.p_label = QLabel("p value --> ")
        self.q_label = QLabel("q value --> ")
        self.n_label = QLabel("n value --> ")
        self.phi_label = QLabel("phi value --> ")
        self.e_label = QLabel("e value --> ")
        self.d_label = QLabel("d value --> ")
        self.p_lineEdit = QLineEdit()
        self.q_lineEdit = QLineEdit()
        self.n_lineEdit = QLineEdit()
        self.phi_lineEdit = QLineEdit()
        self.e_lineEdit = QLineEdit()
        self.d_lineEdit = QLineEdit()
        self.input_textEdit = QTextEdit()
        self.output_textEdit = QTextEdit()
        self.generate_values_button = QPushButton("Generate Values")
        self.enter_values_button = QPushButton("Enter Values")
        self.load_values_button = QPushButton("Load Values")
        self.save_values_button = QPushButton("Save Values")
        self.encrypt_button = QPushButton("Encrypt")
        self.decrypt_button = QPushButton("Decrypt")

        # edit widgets
        self.input_textEdit.setPlaceholderText("Input ...")
        self.output_textEdit.setPlaceholderText("Output ...")
        self.input_textEdit.setText("Ahoj Pepo")
        self.p_lineEdit.setReadOnly(True)
        self.q_lineEdit.setReadOnly(True)
        self.n_lineEdit.setReadOnly(True)
        self.phi_lineEdit.setReadOnly(True)
        self.e_lineEdit.setReadOnly(True)
        self.d_lineEdit.setReadOnly(True)
        self.generate_values_button.clicked.connect(self.generate_values_button_clicked)
        self.enter_values_button.clicked.connect(self.enter_values_button_clicked)
        self.load_values_button.clicked.connect(self.load_values_button_clicked)
        self.save_values_button.clicked.connect(self.save_values_button_clicked)
        self.encrypt_button.clicked.connect(self.encrypt_button_clicked)
        self.decrypt_button.clicked.connect(self.decrypt_button_clicked)

        # create layouts
        self.h_layout_main = QHBoxLayout()
        self.v_layout_left = QVBoxLayout()
        self.v_layout_right = QVBoxLayout()
        self.p_layout = QHBoxLayout()
        self.q_layout = QHBoxLayout()
        self.n_layout = QHBoxLayout()
        self.phi_layout = QHBoxLayout()
        self.e_layout = QHBoxLayout()
        self.d_layout = QHBoxLayout()
        self.buttons_layout = QVBoxLayout()
        self.encrypt_decrypt_layout = QHBoxLayout()

        # setup layouts
        self.h_layout_main.addLayout(self.v_layout_left)
        self.h_layout_main.addLayout(self.v_layout_right)
        self.v_layout_right.addLayout(self.p_layout)
        self.v_layout_right.addLayout(self.q_layout)
        self.v_layout_right.addLayout(self.n_layout)
        self.v_layout_right.addLayout(self.phi_layout)
        self.v_layout_right.addLayout(self.e_layout)
        self.v_layout_right.addLayout(self.d_layout)
        self.v_layout_right.addLayout(self.buttons_layout)
        self.v_layout_right.addLayout(self.encrypt_decrypt_layout)

        # add widgets to layouts
        self.v_layout_left.addWidget(self.input_textEdit)
        self.v_layout_left.addWidget(self.output_textEdit)
        self.p_layout.addWidget(self.p_label)
        self.p_layout.addWidget(self.p_lineEdit)
        self.q_layout.addWidget(self.q_label)
        self.q_layout.addWidget(self.q_lineEdit)
        self.n_layout.addWidget(self.n_label)
        self.n_layout.addWidget(self.n_lineEdit)
        self.phi_layout.addWidget(self.phi_label)
        self.phi_layout.addWidget(self.phi_lineEdit)
        self.e_layout.addWidget(self.e_label)
        self.e_layout.addWidget(self.e_lineEdit)
        self.d_layout.addWidget(self.d_label)
        self.d_layout.addWidget(self.d_lineEdit)
        self.buttons_layout.addWidget(self.generate_values_button)
        self.buttons_layout.addWidget(self.enter_values_button)
        self.buttons_layout.addWidget(self.load_values_button)
        self.buttons_layout.addWidget(self.save_values_button)
        self.encrypt_decrypt_layout.addWidget(self.encrypt_button)
        self.encrypt_decrypt_layout.addWidget(self.decrypt_button)

        self.setLayout(self.h_layout_main)



    @staticmethod
    def generate_pq_values():
        p = Cryptodome.Util.number.getPrime(60)
        q = Cryptodome.Util.number.getPrime(60)
        return p, q


    @staticmethod
    def calculate_n_value(p, q):
        return p * q


    @staticmethod
    def calculate_phi_n(p, q):
        return (p - 1) * (q - 1)


    @staticmethod
    def calculate_e(phi):
        e = Cryptodome.Util.number.getPrime(random.randint(30, 50))

        if Cryptodome.Util.number.GCD(e, phi) == 1 and 1 < e < phi:
            return e
        else:
            print("Something went terribly wrong !!!")


    @staticmethod
    def calculate_d(e, phi):
        return pow(e, -1, phi)


    @staticmethod
    def input_to_blocks(input_):
        block_len = 5
        input_len = len(input_)
        # default matrix length
        matrix_n = input_len // block_len

        # if characters cannot fit in, add one more list
        if input_len % block_len > 0:
            matrix_n = matrix_n + 1

        # create 2D list
        ot_blocks = []
        for x in range(0, matrix_n):
            ot_blocks.append([])

        # split string by 5
        split_input = []
        for x in range(0, input_len, block_len):
            split_input.append(input_[x:x+block_len])


        # fill matrix with characters
        list_index_count = 0
        for word in split_input:
            for character in word:
                ot_blocks[list_index_count].append(character)
            list_index_count += 1


        # print(f"ot_blocks --> {ot_blocks}")
        # print(f"split string --> {split_input}")
        # print(f"matrix n --> {matrix_n}")
        # print(f"ot_blocks --> {ot_blocks}")

        return ot_blocks, matrix_n


    @staticmethod
    def characters_to_numbers(ot_blocks, matrix_n):
        # create matrix
        ot_blocks_numbers = []
        for x in range(0, matrix_n):
            ot_blocks_numbers.append([])

        # fill matrix with characters as numbers
        list_index_count = 0
        for word in ot_blocks:
            for character in word:
                ot_blocks_numbers[list_index_count].append(ord(character))
            list_index_count += 1

        return ot_blocks_numbers


    @staticmethod
    def numbers_to_binary(ot_blocks_numbers, matrix_n):
        # create matrix
        ot_blocks_binary = []
        for x in range(0, matrix_n):
            ot_blocks_binary.append([])

        # fill matrix with binary
        list_index_count = 0
        for block in ot_blocks_numbers:
            for num in block:
                ot_blocks_binary[list_index_count].append(f"{num:010b}")
            list_index_count += 1

        return ot_blocks_binary


    @staticmethod
    def binary_blocks_to_binary_string(ot_blocks_binary):
        binary_string = ""

        for block in ot_blocks_binary:
            for x in block:
                binary_string += x

        return binary_string


    def encrypt(self, binary_string):
        _, _, n, _, e, _ = self.get_all_values()  # p q n phi e d
        ot_int = int(binary_string, 2)
        ct = pow(ot_int, e, n)
        return ct


    def get_all_values(self):
        # p, q = self.generate_pq_values()
        # n = self.calculate_n_value(p, q)
        # phi = self.calculate_phi_n(p, q)
        # e = self.calculate_e(phi)
        # d = self.calculate_d(e, phi)

        p = int(self.p_lineEdit.text())
        q = int(self.q_lineEdit.text())
        n = int(self.n_lineEdit.text())
        phi = int(self.phi_lineEdit.text())
        e = int(self.e_lineEdit.text())
        d = int(self.d_lineEdit.text())

        return p, q, n, phi, e, d


    def generate_values_button_clicked(self):
        print("generate values button clicked")

        # fill line edits with values
        p, q = self.generate_pq_values()
        n = self.calculate_n_value(p, q)
        phi = self.calculate_phi_n(p, q)
        e = self.calculate_e(phi)
        d = self.calculate_d(e, phi)


        # fill line edits with values
        self.p_lineEdit.setText(str(p))
        self.q_lineEdit.setText(str(q))
        self.n_lineEdit.setText(str(n))
        self.phi_lineEdit.setText(str(phi))
        self.e_lineEdit.setText(str(e))
        self.d_lineEdit.setText(str(d))


    def enter_values_button_clicked(self):
        print("enter values button clicked")
        pass


    def load_values_button_clicked(self):
        print("load values button clicked")
        data = ""

        try:
            # read file
            filename, _ = QFileDialog.getOpenFileName()
            if filename:
                with open(filename, "r") as f:
                    data = f.readline()

            data = data.split(",")
            print(data)
            p = int(data[0])
            q = int(data[1])
            n = int(data[2])
            phi = int(data[3])
            e = int(data[4])
            d = int(data[5])

            self.p_lineEdit.setText(str(p))
            self.q_lineEdit.setText(str(q))
            self.n_lineEdit.setText(str(n))
            self.phi_lineEdit.setText(str(phi))
            self.e_lineEdit.setText(str(e))
            self.d_lineEdit.setText(str(d))

        except:
            self.error_message("Unable to load file!", "Warning")





    def save_values_button_clicked(self):
        print("save values button clicked")



        try:
            p, q, n, phi, e, d = self.get_all_values()
            data = [str(p), ",", str(q), ",", str(n), ",", str(phi), ",", str(e), ",", str(d)]

            # save file
            filename, _ = QFileDialog.getSaveFileName()
            if filename:
                with open(filename, "w") as f:
                    f.writelines(data)

        except:
            self.error_message("You cannot save empty values!", "Warning")




    def error_message(self, text, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()


    def encrypt_button_clicked(self):
        print("Encrypt button clicked")

        try:
            ot = self.input_textEdit.toPlainText()
            ot_blocks, matrix_n = self.input_to_blocks(ot)  # change input string to list of characters in blocks of 5
            ot_blocks_num = self.characters_to_numbers(ot_blocks, matrix_n)  # change letters to numbers
            ot_blocks_binary = self.numbers_to_binary(ot_blocks_num, matrix_n)  # change numbers to binary
            ot_binary_string = self.binary_blocks_to_binary_string(ot_blocks_binary)  # concatenate to one string
            encrypted = self.encrypt(ot_binary_string)  # encrypt binary string to big, bad integer

            self.output_textEdit.setText(str(encrypted))  # set value to output lineEdit


        except:
            self.error_message("You need to generate, load or enter valid values!", "Warning --> wrong values")





    def decrypt_button_clicked(self):
        print("Decrypt button clicked")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle("RSA masterpiece")
    sys.exit(app.exec())
