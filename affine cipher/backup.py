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


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Affine Cipher")
        self.resize(800, 500)

        # Widgets here
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Input here ...")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.mode = QComboBox()
        button_start = QPushButton("Do Things")
        button_start.clicked.connect(self.do_things)
        self.mode.addItem("encrypt")
        self.mode.addItem("decrypt")
        label_a = QLabel("A: ")
        label_b = QLabel("B: ")
        self.input_a = QLineEdit()
        self.input_b = QLineEdit()

        # Layouts
        v_layout = QVBoxLayout()
        v2_layout = QVBoxLayout()
        r1_a_layout = QHBoxLayout()
        r1_b_layout = QHBoxLayout()
        r2_layout = QHBoxLayout()

        v2_layout.addWidget(self.mode)
        r1_a_layout.addWidget(label_a)
        r1_a_layout.addWidget(self.input_a)
        r1_b_layout.addWidget(label_b)
        r1_b_layout.addWidget(self.input_b)
        r2_layout.addWidget(self.output_text)

        r1_layout = QHBoxLayout()
        r1_layout.addWidget(self.input_text, 2)
        r1_layout.addLayout(v2_layout)
        v2_layout.addLayout(r1_a_layout)
        v2_layout.addLayout(r1_b_layout)
        v2_layout.addWidget(button_start)
        v2_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        v_layout.addLayout(r1_layout)  # add r1 to v_layout
        v_layout.addLayout(r2_layout)

        # set layout on the application window
        self.setLayout(v_layout)

    def do_things(self):
        text = self.parse_text()
        cipher_text_5chars = ""
        cipher_text = ""
        output_text = ""
        a, b = self.get_parameters()
        current_mode = self.mode.currentIndex()
        print("current mode: ", current_mode)
        print(a, b)
        tmp = 0

        if current_mode == 0:
            cipher_text = self.encode(text, a, b)
            print("ENCODING")

            cipher_text = self.add_spaces(cipher_text, 5)
            output_text = cipher_text

        if current_mode == 1:
            cipher_text = self.decode(text, a, b)
            output_text = cipher_text
            print("DECODING")

        self.output_text.setText(output_text)

    def add_spaces(self, string, length):
        return " ".join(string[i:i + length] for i in range(0, len(string), length))

    def get_input_text(self):
        mytext = self.input_text.toPlainText()
        mytext = mytext.upper()
        mytext = unidecode.unidecode(mytext)
        return mytext

    def parse_text(self):
        mytext = self.get_input_text()
        parsed_text = ""

        # dictionary of allowed characters
        # modulo should be 36

        # iterate through plain text, and get only allowed characters
        for char in mytext:
            if char in main_dict:
                parsed_text = parsed_text + char

        return parsed_text

    def get_parameters(self):
        a = int(self.input_a.text())
        b = int(self.input_b.text())
        gcd = math.gcd(a, mod_num)
        print("GCD VALUE: ", gcd)

        if gcd == 1:
            print("GCD OKAY")
        else:
            print("GCD NOT OKAY")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("                        Invalid \"A\" value!                        ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        return a, b

    def encode(self, text, a, b):
        text_in_numbers = []
        changed_numbers = []
        changed_letters = []
        cipher_text = ""
        text = text

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

        print("*" * 20)
        print(text)
        print(text_in_numbers)
        print(changed_numbers)
        print(changed_letters)
        print(cipher_text)
        print("*" * 20)

        return cipher_text

    def decode(self, text, a, b):
        plaintext = ""
        input_text = text
        input_text = input_text.replace(" ", "")
        text_in_numbers = []
        decoded_letters = []
        changed_numbers = []
        mod_inv = self.inverse_modulo(a)
        print("mod inv: ", mod_inv)

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

        print("*" * 20)
        print(text)
        print(text_in_numbers)
        print(decoded_letters)
        print(changed_numbers)
        print(plaintext)
        print("*" * 20)

        return plaintext

    def inverse_modulo(self, a):
        for x in range(1, mod_num):
            if ((a % mod_num) * (x % mod_num)) % mod_num == 1:
                return x

        print("BAAAD!!!!")
        return -1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.setStyleSheet(open("style.css").read())
    window.show()
    sys.exit(app.exec())
