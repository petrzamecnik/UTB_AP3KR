from os import error
from posixpath import split
import random
import Cryptodome.Util.number as cn
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import re



class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 860, 600
        self.resize(width, height)

        # crete widgets
        self.p_label = QLabel("p value     --> ")
        self.q_label = QLabel("q value     --> ")
        self.n_label = QLabel("n value     --> ")
        self.phi_label = QLabel("phi value --> ")
        self.e_label = QLabel("e value     --> ")
        self.d_label = QLabel("d value     --> ")
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


        self.p_lineEdit.setReadOnly(True)
        self.q_lineEdit.setReadOnly(True)
        self.n_lineEdit.setReadOnly(True)
        self.phi_lineEdit.setReadOnly(True)
        self.e_lineEdit.setReadOnly(True)
        self.d_lineEdit.setReadOnly(True)
        self.generate_values_button.clicked.connect(self.generate_values)
        # self.enter_values_button.clicked.connect(self.enter_values_button_clicked)
        self.load_values_button.clicked.connect(self.load_values)
        self.save_values_button.clicked.connect(self.save_values)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)

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
        # self.p_layout.addWidget(self.p_label)
        # self.p_layout.addWidget(self.p_lineEdit)
        # self.q_layout.addWidget(self.q_label)
        # self.q_layout.addWidget(self.q_lineEdit)
        self.n_layout.addWidget(self.n_label)
        self.n_layout.addWidget(self.n_lineEdit)
        # self.phi_layout.addWidget(self.phi_label)
        # self.phi_layout.addWidget(self.phi_lineEdit)
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

    def error_message(self, text, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def generate_values(self):
        p = cn.getPrime(60)
        q = cn.getPrime(60)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = cn.getPrime(random.randint(40, 59))
        d = pow(e, -1, phi)

        self.p_lineEdit.setText(str(p))
        self.q_lineEdit.setText(str(q))
        self.n_lineEdit.setText(str(n))
        self.phi_lineEdit.setText(str(phi))
        self.e_lineEdit.setText(str(e))
        self.d_lineEdit.setText(str(d))

        # check if e value is okay
        if cn.GCD(e, phi) == 1 and 1 < e < phi:
            print("Generation OK")

        else:
            print("Unable to generate valid values, try again.")

    def get_all_values(self):
        try:
            p = int(self.p_lineEdit.text())
            q = int(self.q_lineEdit.text())
            n = int(self.n_lineEdit.text())
            phi = int(self.phi_lineEdit.text())
            e = int(self.e_lineEdit.text())
            d = int(self.d_lineEdit.text())

            return p, q, n, phi, e, d

        except:
            # self.error_message("Unable to load values.", "Error.")
            pass

    def save_values(self):
        print("save values button clicked")

        try:
            p, q, n, phi, e, d = self.get_all_values()
            data = [
                str(p),
                ",",
                str(q),
                ",",
                str(n),
                ",",
                str(phi),
                ",",
                str(e),
                ",",
                str(d),
            ]

            # save file
            filename, _ = QFileDialog.getSaveFileName()
            if filename:
                with open(filename, "w") as f:
                    f.writelines(data)

        except:
            self.error_message("You cannot save empty values!", "Warning")

    def load_values(self):
        print("load values button clicked")
        data = ""

        try:
            # read file
            filename, _ = QFileDialog.getOpenFileName()
            if filename:
                with open(filename, "r") as f:
                    data = f.readline()

            data = data.split(",")
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

    def encrypt(self):
        try:
            _, _, n, _, e, _ = self.get_all_values()
            ot = self.input_textEdit.toPlainText()
            block_size = 5
            bin_block_large_size = 50


            # split input string into blocks of size 5
            ot_blocks = [ot[i : i + block_size] for i in range(0, len(ot), block_size)]
            ot_nums = []
            ot_bin_blocks = []
            bin_string_50 = ""
            ot_bin_blocks_large = []
            ct = ""

            # for each block of open text, change characters to numbers and append to array
            for block in ot_blocks:
                for char in block:
                    ot_nums.append(ord(char))

            # for each num, generate binary number with pre-pended zeros to match blocks of 10bits
            for num in ot_nums:
                bin_num = ""
                bin_num = "0" * (10 - len(bin(num)[2:])) + bin(num)[2:]
                ot_bin_blocks.append(bin_num)

            ot_bin_blocks = [ot_bin_blocks[i:i + block_size] for i in range(0, len(ot_bin_blocks), block_size)]

            # for each character in ot_bin_blocks blocks, concat into single string
            for block in ot_bin_blocks:
                bin_string_50 = ""
                for bin_string_10 in block:
                    bin_string_50 += bin_string_10
    
                ot_bin_blocks_large.append(str("0" * (50 - len(bin_string_50)) + bin_string_50))
                

            
            for block in ot_bin_blocks_large:
                ct += str(pow(int(block, 2), e, n)) + " "


            self.output_textEdit.setText(ct)

            
            # TBBDC --> The Big Bag Debugging Code

            # print(f"n --> {n} \n" f"e --> {e}")
            # print(f"ot: {ot}")
            # print(f"ot blocks = {ot_blocks}")
            # print(f"ot nums = {ot_nums}")
            # print(f"ot bin blocks = {ot_bin_blocks}")
            # print(f"ot bin blocks large = {ot_bin_blocks_large}")
            # print(f"ct = {ct}")


        except:
            self.error_message("Was not able to encrypt message.", "Error !")
            pass

    def decrypt(self):
        ct = self.input_textEdit.toPlainText()
        p = q = n = phi = e = d = 0

        
        try:
            _, _, n, _, _, d = self.get_all_values()
            ct = self.input_textEdit.toPlainText()
            ct = ct.strip()
            ct_blocks = ct.split(" ")
            ct_blocks_encrypted = []
            ct_blocks_binary_large = []
            ct_blocks_binary = []
            ct_nums = []
            ot = ""

                # decrypt values
            for block in ct_blocks:
                ct_blocks_encrypted.append(pow(int(block), d, n))

            # change numbers to binary blocks
            for block in ct_blocks_encrypted:
                ct_bin_large = ""
                ct_blocks_binary_large.append(str("0" * (50 - len(bin(block)[2:])) + bin(block)[2:]))
                

            # ct_blocks_binary = [ot[i : i + block_size] for i in range(0, len(ot), block_size)]
            for block in ct_blocks_binary_large:
                ct_blocks_binary.append([block[i : i + 10] for i in range(0, len(block), 10)])
                
            # change binary number into integer
            for block in ct_blocks_binary:
                for bin_num in block:
                    ct_nums.append(int(bin_num, 2))

            # change integers to characters, then append to open text
            for num in ct_nums:
                if num != 0:
                    ot += chr(num)

            self.output_textEdit.setText(str(ot))

        except:
            self.error_message("Unable to load cipher text or values for decryption.", "Error.")
            pass


        # print(f"ct = {ct}")
        # print(f"ct blocks = {ct_blocks}")
        # print(f"ct blocks encrypted = {ct_blocks_encrypted}")
        # print(f"ct blocks binary large = {ct_blocks_binary_large}")
        # print(f"ct blocks binary = {ct_blocks_binary}")
        # print(f"ct numbs = {ct_nums}")
        # print(f"ot = {ot}")

    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = App()
    window.show()
    window.setWindowTitle("RSA")
    sys.exit(app.exec())

