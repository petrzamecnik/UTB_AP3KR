import re
import sys
import numpy as np
import unidecode
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

alphabet_english = ["A", "B", "C", "D", "E",
                    "F", "G", "H", "I", "K",
                    "L", "M", "N", "O", "P",
                    "Q", "R", "S", "T", "U",
                    "V", "W", "X", "Y", "Z"]

alphabet_czech = ["A", "B", "C", "D", "E",
                  "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O",
                  "P", "Q", "R", "S", "T",
                  "U", "V", "X", "Y", "Z"]

alphabet_eng = np.array([
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"]])

alphabet_cz = np.array([
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O"],
    ["P", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"]])

repl_english = [("J", "I")]
repl_czech = [("W", "V")]
repl_czech_specials = [("Č", "C"), ("Ď", "D"), ("Ě", "E"), ("Ň", "N"), ("Ř", "R"), ("Š", "S"), ("Ť", "T"), ("Ž", "Z"),
                       ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"), ("Ů", "U"), ("Ý", "Y")]


class App(QWidget):
    def __init__(self):
        super().__init__()
        width, height = 980, 600
        # half_width = int(width / 2)
        # self.resize(width, height)
        self.setFixedSize(width, height)

        # Create Widgets
        self.alphabet_label = QLabel("Alphabet: ")
        self.alphabet_combobox = QComboBox()
        self.keyword_label = QLabel("Keyword: ")
        self.keyword_lineEdit = QLineEdit()
        self.mode_label = QLabel("Mode: ")
        self.mode_combobox = QComboBox()
        self.input_textEdit = QTextEdit()
        self.output_textEdit = QTextEdit()
        self.wildcard_label = QLabel("Wildcard characters: ")
        self.wildcard_lineEdit = QLineEdit()
        self.main_button = QPushButton("Do Things")
        self.array_table = QTableWidget(5, 5)

        # Edit widgets
        self.alphabet_combobox.addItem("English")
        self.alphabet_combobox.addItem("Czech")
        self.alphabet_combobox.currentIndexChanged.connect(self.change_default_alphabet)
        self.mode_combobox.addItem("Encrypt")
        self.mode_combobox.addItem("Decrypt")
        self.input_textEdit.setPlaceholderText("Input")
        self.output_textEdit.setPlaceholderText("Output")
        # self.wildcard_lineEdit.setReadOnly(True)
        self.keyword_lineEdit.setText("Kolo!TOČ")
        self.wildcard_lineEdit.setText("X, W")
        self.main_button.setMinimumHeight(70)
        self.main_button.clicked.connect(self.do_things)
        self.array_table.setMaximumWidth(300)
        self.array_table.setMaximumHeight(300)
        self.array_table.setColumnWidth(0, 60)
        self.array_table.setRowHeight(0, 60)
        self.array_table.setColumnWidth(1, 60)
        self.array_table.setRowHeight(1, 60)
        self.array_table.setColumnWidth(2, 60)
        self.array_table.setRowHeight(2, 60)
        self.array_table.setColumnWidth(3, 60)
        self.array_table.setRowHeight(3, 60)
        self.array_table.setColumnWidth(4, 60)
        self.array_table.setRowHeight(4, 60)
        self.array_table.horizontalHeader().hide()
        self.array_table.verticalHeader().hide()
        self.array_table.horizontalScrollBar().hide()
        self.array_table.verticalScrollBar().hide()

        # Create Layouts
        self.h_layout_main = QHBoxLayout()
        self.v_layout_left = QVBoxLayout()
        self.v_layout_right = QVBoxLayout()
        self.first_row = QHBoxLayout()
        self.alphabet_layout = QHBoxLayout()
        self.keyword_layout = QHBoxLayout()
        self.mode_layout = QHBoxLayout()
        self.wildcard_layout = QHBoxLayout()

        # Setup layouts
        self.h_layout_main.addLayout(self.v_layout_left, 1)
        self.h_layout_main.addLayout(self.v_layout_right, 1)
        self.v_layout_left.addLayout(self.first_row)
        self.v_layout_left.addLayout(self.keyword_layout)
        self.first_row.addLayout(self.alphabet_layout)
        self.first_row.addLayout(self.mode_layout)
        self.v_layout_left.addLayout(self.wildcard_layout)

        # Edit Layouts
        self.v_layout_left.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.v_layout_left.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.v_layout_right.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.first_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mode_layout.setContentsMargins(80, 00, 00, 00)

        # Add widgets to layouts
        self.alphabet_layout.addWidget(self.alphabet_label)
        self.alphabet_layout.addWidget(self.alphabet_combobox)
        self.mode_layout.addWidget(self.mode_label)
        self.mode_layout.addWidget(self.mode_combobox)
        self.keyword_layout.addWidget(self.keyword_label)
        self.keyword_layout.addWidget(self.keyword_lineEdit)
        self.v_layout_left.addWidget(self.input_textEdit)
        self.v_layout_left.addWidget(self.output_textEdit)
        self.wildcard_layout.addWidget(self.wildcard_label)
        self.wildcard_layout.addWidget(self.wildcard_lineEdit)
        self.v_layout_right.addWidget(self.main_button)
        self.v_layout_right.addWidget(self.array_table)

        self.setLayout(self.h_layout_main)

        for x in range(0, 5):
            for y in range(0, 5):
                table_item = QTableWidgetItem(str(alphabet_eng[x][y]))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.array_table.setItem(x, y, table_item)

    def change_default_alphabet(self):
        index = self.alphabet_combobox.currentIndex()

        if index == 0:
            for x in range(0, 5):
                for y in range(0, 5):
                    table_item = QTableWidgetItem(str(alphabet_eng[x][y]))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.array_table.setItem(x, y, table_item)

        elif index == 1:
            for x in range(0, 5):
                for y in range(0, 5):
                    table_item = QTableWidgetItem(str(alphabet_cz[x][y]))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.array_table.setItem(x, y, table_item)

    def do_things(self):
        print("Doing things")
        alphabet_choice, mode, keyword, wildcard_characters = self.parse_input()
        text_input = self.input_textEdit.toPlainText()

        if alphabet_choice == 0:
            cipher_alphabet = self.generate_cipher_alphabet(keyword, alphabet_english)

        elif alphabet_choice == 1:
            cipher_alphabet = self.generate_cipher_alphabet(keyword, alphabet_czech)

        try:
            self.fill_table(cipher_alphabet)
        except:
            self.warning_message("Something went wrong.")
            pass

        if mode == 0:
            print("ENCRYPT")
            text_input = self.parse_text_to_encrypt(text_input, wildcard_characters, alphabet_choice)
            bigrams = self.text_to_bigram(text_input)
            cipher_text = self.encrypt(bigrams, cipher_alphabet)
            print(text_input)
            print(cipher_text)
            self.output_textEdit.setText(self.add_spaces(cipher_text, 5))

        elif mode == 1:
            print("DECRYPT")
            self.output_textEdit.setText(self.decrypt(text_input, cipher_alphabet))

        # print(f"***********************\n",
        #       f"Alphabet: {cipher_alphabet}\n"
        #       f"Mode: {mode}\n"
        #       f"Keyword: {keyword}\n"
        #       f"Wildcard: {wildcard_characters}\n"
        #       f"Text: {text_input}\n"
        #       f"Bigrams: {bigrams}\n"
        #       f"***********************\n")

    def encrypt(self, input_, cipher_alphabet):
        # input_ = input_
        cipher_alphabet = np.array(cipher_alphabet)
        output = ""

        for x in input_:
            c1 = x[0]
            c2 = x[1]
            c1x = np.where(cipher_alphabet == c1)[1]
            c1y = np.where(cipher_alphabet == c1)[0]
            c2x = np.where(cipher_alphabet == c2)[1]
            c2y = np.where(cipher_alphabet == c2)[0]

            # same column
            if c1x == c2x:
                c1x_new = c1x
                c1y_new = (c1y + 1) % 5
                c2x_new = c2x
                c2y_new = (c2y + 1) % 5

                output += cipher_alphabet[int(c1y_new)][int(c1x_new)]
                output += cipher_alphabet[int(c2y_new)][int(c2x_new)]

            # same row
            if c1y == c2y:
                c1x_new = (c1x + 1) % 5
                c1y_new = c1y
                c2x_new = (c2x + 1) % 5
                c2y_new = c2y

                output += cipher_alphabet[int(c1y_new)][int(c1x_new)]
                output += cipher_alphabet[int(c2y_new)][int(c2x_new)]

            # cross rule
            if c1x != c2x and c1y != c2y:
                c1x_new = c1x
                c1y_new = c2y
                c2x_new = c2x
                c2y_new = c1y

                output += cipher_alphabet[int(c2y_new)][int(c2x_new)]
                output += cipher_alphabet[int(c1y_new)][int(c1x_new)]

        return output

    def decrypt(self, input_, cipher_alphabet):
        input_ = self.remove_spaces(input_)
        cipher_alphabet = np.array(cipher_alphabet)
        output = ""
        replacements = [(" ", "QSPACE"), ("0", "QZERO"), ("1", "QONE"), ("2", "QTWO"), ("3", "QTHRE"),
                        ("4", "QFOUR"), ("5", "QFIVE"), ("6", "QSIX"), ("7", "QSEVEN"), ("8", "QEIGHT"), ("9", "QNINE")]

        print(input_)

        # substitution back to normal character

        bigrams = self.text_to_bigram(input_)
        print(bigrams)
        try:
            for x in bigrams:
                c1 = x[0]
                c2 = x[1]
                c1x = np.where(cipher_alphabet == c1)[1]
                c1y = np.where(cipher_alphabet == c1)[0]
                c2x = np.where(cipher_alphabet == c2)[1]
                c2y = np.where(cipher_alphabet == c2)[0]

                # same column
                if c1x == c2x:
                    c1x_new = c1x
                    c1y_new = (c1y - 1) % 5
                    c2x_new = c2x
                    c2y_new = (c2y - 1) % 5

                    output += cipher_alphabet[int(c1y_new)][int(c1x_new)]
                    output += cipher_alphabet[int(c2y_new)][int(c2x_new)]

                # same row
                if c1y == c2y:
                    c1x_new = (c1x - 1) % 5
                    c1y_new = c1y
                    c2x_new = (c2x - 1) % 5
                    c2y_new = c2y

                    output += cipher_alphabet[int(c1y_new)][int(c1x_new)]
                    output += cipher_alphabet[int(c2y_new)][int(c2x_new)]

                # cross rule
                if c1x != c2x and c1y != c2y:
                    c1x_new = c1x
                    c1y_new = c2y
                    c2x_new = c2x
                    c2y_new = c1y

                    output += cipher_alphabet[int(c2y_new)][int(c2x_new)]
                    output += cipher_alphabet[int(c1y_new)][int(c1x_new)]

        except:
            self.warning_message("Input was not valid. Output might be corrupted.")


        for pattern, replacement in replacements:
            output = re.sub(replacement, pattern, output)

        print(output)

        return output

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

    def parse_input(self):
        alphabet_choice = self.alphabet_combobox.currentIndex()
        mode = self.mode_combobox.currentIndex()
        keyword = self.keyword_lineEdit.text()
        wildcard_characters = self.wildcard_lineEdit.text()

        # print(f"***********************\n",
        #       f"Alphabet: {alphabet_choice}\n"
        #       f"Mode: {mode}\n"
        #       f"Keyword: {keyword}\n"
        #       f"Wildcard: {wildcard_characters}\n"
        #       f"Text: {text_input}\n"
        #       f"***********************\n")

        return alphabet_choice, mode, self.parse_keyword(keyword), \
               self.parse_wildcard_characters(wildcard_characters)

    def parse_wildcard_characters(self, input_):
        input_ = input_.upper()
        input_ = re.sub(r"[^A-Z]", "", input_)
        output = []

        for x in input_:
            if x not in output:
                output.append(x)

        print(f"OUTPUT: {output}")

        return output

    def parse_keyword(self, input_):
        input_ = input_.upper()
        input_ = unidecode.unidecode(input_)
        replacements = [("[^A-Z]", ""), ("J", "I")]  # patterns for regex
        output = []

        # filtering only A-Z characters & changing J to I
        for pattern, replacement in replacements:
            input_ = re.sub(pattern, replacement, input_)

        for x in input_:
            if x not in output:
                output.append(x)

        return output


    def parse_text_to_encrypt(self, input_, wildcard_chars, alphabet_choice):
        input_ = input_.upper()
        output = ""
        prev_char = ""
        input_only_chars = ""

        for pattern, replacement in repl_czech_specials:
            input_ = re.sub(pattern, replacement, input_)

        print(f"length: {len(wildcard_chars)}")

        try:
            char_w1 = wildcard_chars[0]
            char_w2 = wildcard_chars[1]

        except:
            self.warning_message("Wildcards must contain alteast TWO characters. Preferably most uncommon characters "
                                 "(X, W, Q ...)")

        if alphabet_choice == 0:
            input_ = re.sub("J", "I", input_)
        elif alphabet_choice == 1:
            input_ = re.sub("Q", "O", input_)

        replacements = [(" ", "QSPACE"), ("0", "QZERO"), ("1", "QONE"), ("2", "QTWO"), ("3", "QTHRE"),
                        ("4", "QFOUR"), ("5", "QFIVE"), ("6", "QSIX"), ("7", "QSEVEN"), ("8", "QEIGHT"), ("9", "QNINE")]

        # substitution for unusable characters
        for pattern, replacement in replacements:
            input_ = re.sub(pattern, replacement, input_)

        # keep only characters that are in used alphabet
        if alphabet_choice == 0:
            for x in input_:
                if x in alphabet_english:
                    input_only_chars += x
        elif alphabet_choice == 1:
            for x in input_:
                if x in alphabet_czech:
                    input_only_chars += x

        # checking for duplicate characters
        try:
            for x in input_only_chars:
                if x != prev_char:
                    output += x
                    prev_char = x
                elif x == prev_char and prev_char != char_w1:
                    output += char_w1
                    output += x
                    prev_char = x

                elif x == prev_char and prev_char == char_w1:
                    output += char_w2
                    output += x
                    prev_char = x

            # count characters
            char_count = len(output)

            # check if output is even number, if not, then add according character and return
            if char_count % 2 == 0:
                return output

            elif char_count % 2 != 0 and prev_char != char_w1:
                output += char_w1
                return output

            elif char_count % 2 != 0 and prev_char == char_w1:
                output += char_w2
                return output

        except:
            return ""



    def text_to_bigram(self, input_):
        input_list = []
        bigram_list = []

        for x in input_:
            input_list.append(x)

        for x in range(0, len(input_list), 2):
            bigram_list.append(input_list[x: x + 2])

        return bigram_list

    def generate_cipher_alphabet(self, keyword, alphabet):
        cipher_alphabet = []

        diff_list = list(set(alphabet) - set(keyword))
        diff_list.sort()

        for x in keyword:
            cipher_alphabet.append(x)

        for x in diff_list:
            cipher_alphabet.append(x)

        cipher_alphabet_arr = np.array(cipher_alphabet)
        cipher_alphabet_arr = np.reshape(cipher_alphabet_arr, (5, 5))

        return cipher_alphabet_arr

    def fill_table(self, input_):
        matrix = input_

        for x in range(0, 5):
            for y in range(0, 5):
                table_item = QTableWidgetItem(str(matrix[x][y]))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.array_table.setItem(x, y, table_item)

        # for x in range(0, 5):
        #     for y in range(0, 5):
        #         print(f"column: {x}\n"
        #               f"row: {y}\n"
        #               f"character: {matrix[x][y]}")

    def warning_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle("Playfair Cipher")
    sys.exit(app.exec())
