import math
import sys
import unidecode  # package to get rid of diacritics ( normalize string )
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


mod_num = 36
main_dict = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5,
    "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11,
    "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17,
    "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23,
    "Y": 24, "Z": 25, " ": 26, "0": 27, "1": 28, "2": 29,
    "3": 30, "4": 31, "5": 32, "6": 33, "7": 34, "8": 35,
    "9": 36
}

key_list = list(main_dict.keys())
value_list = list(main_dict.values())


# noinspection DuplicatedCode
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Affine Cipher")
        self.resize(980, 600)

        # Widgets here
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Input here ...")
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Output here ...")
        self.output_text.setReadOnly(True)
        self.mode = QComboBox()
        button_start = QPushButton("Do Things")
        button_start.clicked.connect(self.do_things)
        self.mode.addItem("encode")
        self.mode.addItem("decode")
        label_a = QLabel("value A: ")
        label_b = QLabel("value B: ")
        self.input_a = QLineEdit()
        self.input_a.setText("0")
        self.input_b = QLineEdit()
        self.input_b.setText("0")
        label_removed_characters = QLabel("          Removed Characters: ")
        self.removed_characters = QTextEdit()
        self.removed_characters.setReadOnly(True)
        self.removed_characters.setMaximumWidth(220)
        self.label_alphabet = QLabel("Alphabet:")
        self.label_cipher_alphabet = QLabel("Cipher Alphabet:")
        self.line_alphabet = QLineEdit()
        self.line_alphabet.setText("ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789")
        self.line_alphabet.setReadOnly(True)
        self.line_cipher_alphabet = QLineEdit()
        self.line_cipher_alphabet.setReadOnly(True)

        # Create Layouts
        v_layout = QVBoxLayout()
        v2_layout = QVBoxLayout()
        r1_a_layout = QHBoxLayout()
        r1_b_layout = QHBoxLayout()
        r2_layout = QHBoxLayout()
        r1_layout = QHBoxLayout()
        r2_removed_characters_layout = QVBoxLayout()
        r_top_layout = QHBoxLayout()

        # Add widgets to layouts
        v2_layout.addWidget(self.mode)
        r1_a_layout.addWidget(label_a)
        r1_a_layout.addWidget(self.input_a)
        r1_b_layout.addWidget(label_b)
        r1_b_layout.addWidget(self.input_b)
        r2_layout.addWidget(self.output_text)
        r1_layout.addWidget(self.input_text, 2)
        r2_removed_characters_layout.addWidget(label_removed_characters)
        r2_removed_characters_layout.addWidget(self.removed_characters)
        r_top_layout.addWidget(self.label_alphabet)
        r_top_layout.addWidget(self.line_alphabet)
        r_top_layout.addWidget(self.label_cipher_alphabet)
        r_top_layout.addWidget(self.line_cipher_alphabet)
        r1_layout.addLayout(v2_layout)
        v2_layout.addLayout(r1_a_layout)
        v2_layout.addLayout(r1_b_layout)
        v2_layout.addWidget(button_start)
        v2_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        r2_layout.addLayout(r2_removed_characters_layout)

        v_layout.addLayout(r1_layout)
        v_layout.addLayout(r2_layout)
        v_layout.addLayout(r_top_layout)

        # set layout on the application window
        self.setLayout(v_layout)

    def do_things(self):
        check_A = False
        text = self.parse_text()
        a, b, check_A = self.get_parameters(check_A)
        current_mode = self.mode.currentIndex()
        output_text = ""
        alphabet = ""
        cipher_alphabet = ""
        removed_characters = ""

        # generate base alphabet
        for x in key_list:
            alphabet += x

        # assign data to GUI
        self.line_alphabet.setText(alphabet)

        # check if "a" value is valid
        if check_A:
            # check if mode is encode(0) or decode (1)
            if current_mode == 0:
                cipher_text = self.encode(text, a, b)
                cipher_text = self.add_spaces(cipher_text, 5)
                cipher_alphabet = self.encode(alphabet, a, b)  # assign cipher alphabet
                output_text = cipher_text

            if current_mode == 1:
                cipher_text = self.decode(text, a, b)
                cipher_alphabet = self.encode(alphabet, a, b)  # assign cipher alphabet
                output_text = cipher_text

            removed_characters = self.get_removed_characters()

        # assign data to GUI
        self.output_text.setText(output_text)
        self.removed_characters.setText(removed_characters)
        self.line_cipher_alphabet.setText(cipher_alphabet)

    def add_spaces(self, string, length):
        return " ".join(string[i:i + length] for i in range(0, len(string), length))

    def remove_spaces(self, string):
        index = 0
        new_string = ""

        # check if there is space at correct position, if true then remove it
        for x in string:
            if (index % 5 == 0) and index != 0:
                new_string = new_string + ""
                index = 0
            else:
                new_string = new_string + x
                index += 1

        return new_string

    def get_input_text(self):
        mytext = self.input_text.toPlainText()
        return mytext

    def parse_text(self):
        parsed_text = ""
        mytext = self.get_input_text()
        mytext = mytext.upper()
        mytext = unidecode.unidecode(mytext)

        # iterate through plain text, and get only allowed characters
        for char in mytext:
            if char in main_dict:
                parsed_text = parsed_text + char

        return parsed_text

    def get_parameters(self, check_A):
        try:
            a = int(self.input_a.text())
            b = int(self.input_b.text())

            gcd = math.gcd(a, mod_num)
            check_A = check_A
            viable_A_values = []

            # check gcd for number in range...
            for x in range(a, mod_num - 1):
                if math.gcd(x, mod_num) == 1:
                    viable_A_values.append(x)

            if gcd == 1:
                check_A = True
            else:
                print("GCD NOT OKAY")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("                        Invalid \"A\" value!                        "
                            "Viable values: " + str(viable_A_values))
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.setDefaultButton(QMessageBox.StandardButton.Ok)
                msg.exec()


            return a, b, check_A


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("                        Invalid \"A or B\" value!                        "
                        "Values must be of type integer! ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg.exec()

        return 0, 0, 0

    def encode(self, text, a, b):
        text_in_numbers = []  # represents parsed text as numbers according to main_dict
        changed_numbers = []  # represents numbers after using encoding algorithm
        changed_letters = []  # represents ecnoded text
        cipher_text = ""
        text = text
        text = " ".join(text.split())

        for letter in text:
            if letter in main_dict.keys():
                text_in_numbers.append(main_dict[letter])

        for word in text_in_numbers:
            word = ((a * word + b) % mod_num)
            changed_numbers.append(word)

        for value in changed_numbers:
            if value in main_dict.values():
                changed_letters.append(key_list[value])

        for x in changed_letters:
            cipher_text = cipher_text + x

        return cipher_text

    def decode(self, text, a, b):
        plaintext = ""
        input_text = text
        input_text = self.remove_spaces(input_text)
        text_in_numbers = []  # represents text as number, before decoding
        decoded_letters = []  # represents text as numbers, after decoding
        changed_numbers = []  # represents text, that we get from numbers after decoding
        mod_inv = self.inverse_modulo(a)

        for letter in input_text:
            if letter in main_dict.keys():
                text_in_numbers.append(main_dict[letter])

        for word in text_in_numbers:
            word = (mod_inv * (word - b) % mod_num)
            decoded_letters.append(word)

        for value1 in decoded_letters:
            if value1 in main_dict.values():
                changed_numbers.append(key_list[value1])

        for x in changed_numbers:
            plaintext = plaintext + x

        return plaintext

    def inverse_modulo(self, a):
        for x in range(1, mod_num):
            if ((a % mod_num) * (x % mod_num)) % mod_num == 1:
                return x

        # print("BAAAD!!!!")
        return -1

    def get_removed_characters(self):
        text = self.get_input_text()
        text = text.upper()
        text = unidecode.unidecode(text)
        parsed_text = self.parse_text()
        unfiltered_text = []
        filtered_text = []
        filtered_chars = []
        filtered_chars_string = ""

        for x in text:
            unfiltered_text.append(x)

        for x in parsed_text:
            filtered_text.append(x)

        for x in unfiltered_text:
            if x not in filtered_text:
                filtered_chars.append(x)

        for x in filtered_chars:
            filtered_chars_string += x

        return filtered_chars_string


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.setStyleSheet(open("style.css").read())
    window.show()
    sys.exit(app.exec())
