import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import functions as fc
import random
import numpy as np
import time


table_values = fc.get_alphabet_reduced_en_np()


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 860, 600
        self.resize(width, height)


        # Create widgets
        self.keyword_label = QLabel("Keyword: ")
        self.keyword_lineEdit = QLineEdit()
        # self.keyword_lineEdit.setText("Kol!otoč")
        self.keyword_lineEdit.setText("ABC")
        self.cipher_mode_label = QLabel("Cipher mode: ")
        self.cipher_mode_comboBox = QComboBox()
        self.mode_label = QLabel("Mode: ")
        self.mode_comboBox = QComboBox()
        self.language_label = QLabel("Language: ")
        self.language_comboBox = QComboBox()
        self.input_textEdit = QTextEdit()
        self.output_textEdit = QTextEdit()
        self.main_button = QPushButton("Do Things")
        self.cipher_table = QTableWidget(5, 5)
        self.shuffle_button = QPushButton("Shuffle alphabet")
        self.clean_button = QPushButton("Clean alphabet")
        self.save_button = QPushButton("Save alphabet")
        self.vertical_spacer = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontal_spacer = QSpacerItem(50, 0, QSizePolicy.Maximum, QSizePolicy.Expanding)



        # Edit widgets
        self.main_button.clicked.connect(self.do_things)
        self.main_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_button.setMaximumSize(200, 70)
        self.shuffle_button.clicked.connect(self.on_shuffle_button_clicked)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.clean_button.clicked.connect(self.on_clean_button_clicked)
        self.cipher_mode_comboBox.addItem("ADFGX")
        self.cipher_mode_comboBox.addItem("ADFG(V)X")
        self.cipher_mode_comboBox.currentIndexChanged.connect(self.on_cipher_mode_change)
        self.mode_comboBox.addItem("Encode")
        self.mode_comboBox.addItem("Decode")
        self.language_comboBox.addItem("English")
        self.language_comboBox.addItem("Czech")
        self.language_comboBox.currentIndexChanged.connect(self.on_language_mode_change)
        self.input_textEdit.setPlaceholderText("Input ...")
        self.output_textEdit.setPlaceholderText("Output ...")
        self.output_textEdit.setReadOnly(True)

        self.cipher_table.setMaximumWidth(300)
        self.cipher_table.setMaximumHeight(300)
        for x in range(0, 5):
            self.cipher_table.setColumnWidth(x, 60)
            self.cipher_table.setRowHeight(x, 60)
        self.cipher_table.horizontalScrollBar().hide()
        self.cipher_table.verticalScrollBar().hide()
        self.cipher_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.itemChanged.connect(self.on_item_changed)

        # Create layouts
        self.h_layout_main = QHBoxLayout()
        self.v_layout_left = QVBoxLayout()
        self.v_layout_right = QVBoxLayout()
        self.keyword_layout = QHBoxLayout()
        self.mode_layout = QHBoxLayout()
        self.cipher_mode_layout = QHBoxLayout()
        self.language_mode_layout = QHBoxLayout()
        self.table_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.main_button_layout = QHBoxLayout()

        # Edit layouts
        self.v_layout_right.setAlignment(Qt.AlignRight)
        self.table_layout.setAlignment(Qt.AlignCenter)


        # Layout setup
        self.h_layout_main.addLayout(self.v_layout_left)
        self.h_layout_main.addLayout(self.v_layout_right)
        self.v_layout_left.addLayout(self.mode_layout)
        self.v_layout_left.addLayout(self.cipher_mode_layout)
        self.v_layout_left.addLayout(self.language_mode_layout)
        self.v_layout_left.addLayout(self.keyword_layout)
        self.v_layout_right.addLayout(self.main_button_layout)
        self.v_layout_right.addLayout(self.table_layout)
        self.v_layout_right.addLayout(self.button_layout)



        # Add widgets to layouts
        self.keyword_layout.addWidget(self.keyword_label)
        self.keyword_layout.addWidget(self.keyword_lineEdit)
        self.mode_layout.addWidget(self.mode_label)
        self.mode_layout.addWidget(self.mode_comboBox)
        self.cipher_mode_layout.addWidget(self.cipher_mode_label)
        self.cipher_mode_layout.addWidget(self.cipher_mode_comboBox)
        self.language_mode_layout.addWidget(self.language_label)
        self.language_mode_layout.addWidget(self.language_comboBox)
        self.main_button_layout.addWidget(self.main_button)
        self.table_layout.addWidget(self.cipher_table)
        self.button_layout.addWidget(self.shuffle_button)
        self.button_layout.addWidget(self.clean_button)
        self.button_layout.addWidget(self.save_button)
        self.v_layout_left.addWidget(self.input_textEdit)
        self.v_layout_left.addWidget(self.output_textEdit)

        # Main layout
        self.setLayout(self.h_layout_main)

        self.fill_default_table()


    def warning_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.exec()


    def warning_message_missing_letters(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.setWindowTitle("Warning")
        fill_button = msg.addButton("Fill Table", msg.ActionRole)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        fill_button.clicked.connect(self.fill_table)
        msg.exec()


    def on_item_changed(self):
        pass
        # print("ITEM CHANGED")
        # row = self.cipher_table.currentRow()
        # col = self.cipher_table.currentColumn()
        #
        # if
        #
        #
        # current_letter = self.cipher_table.item(row, col).text()
        # changed_letter = current_letter.upper()
        # item = QTableWidgetItem(str(changed_letter))
        # item.setTextAlignment(Qt.AlignCenter)
        #
        # self.cipher_table.setItem(row, col, item)


    def fill_table(self):
        cipher_mode = self.cipher_mode_comboBox.currentIndex()
        lang_mode = self.language_comboBox.currentIndex()

        if cipher_mode == 0:
            if lang_mode == 0:
                alphabet = fc.get_alphabet_reduced_en()
                random.shuffle(alphabet)
                alphabet = np.array(alphabet)
                self.create_english_alphabet(alphabet.reshape(5, 5))
            elif lang_mode == 1:
                alphabet = fc.get_alphabet_reduced_cz()
                random.shuffle(alphabet)
                alphabet = np.array(alphabet)
                self.create_czech_alphabet(alphabet.reshape(5, 5))

        elif cipher_mode == 1:
            alphabet = fc.get_alphabet_full()
            random.shuffle(alphabet)
            alphabet = np.array(alphabet)
            self.create_adfgvx_alphabet(alphabet.reshape(6, 6))


    def on_language_mode_change(self, value):

        if value == 0:
            self.create_english_alphabet(fc.get_alphabet_reduced_en_np())

        elif value == 1:
            self.create_czech_alphabet(fc.get_alphabet_reduced_cz_np())


    def on_cipher_mode_change(self, value):
        lang_value = self.language_comboBox.currentIndex()

        # ADFGX
        if value == 0:
            # print(value)
            self.language_comboBox.setEnabled(True)

            # english
            if lang_value == 0:
                self.create_english_alphabet(fc.get_alphabet_reduced_en_np())

            # czech
            elif lang_value == 1:
                self.create_czech_alphabet(fc.get_alphabet_reduced_cz_np())




        # ADFGVX
        elif value == 1:
            self.create_adfgvx_alphabet(fc.get_alphabet_full_np())


    def on_save_button_clicked(self):
        print("save button clicked")
        global table_values
        cipher_mode = self.cipher_mode_comboBox.currentIndex()
        alphabet_mode = self.language_comboBox.currentIndex()
        alphabet = self.get_table_values()
        print(alphabet)
        # alphabet_test = self.get_table_values()


        if cipher_mode == 0:
            if alphabet_mode == 0:

                if sorted(alphabet) == sorted(fc.get_alphabet_reduced_en()):
                    alphabet = np.array(alphabet).reshape(5, 5)
                    table_values = alphabet

                else:
                    self.warning_message_missing_letters("Table must contain only letters, numbers, and cannot contain "
                                                         "any duplicates")

            elif alphabet_mode == 1:
                if sorted(alphabet) == sorted(fc.get_alphabet_reduced_cz()):
                    alphabet = np.array(alphabet).reshape(5, 5)
                    table_values = alphabet

                else:
                    self.warning_message_missing_letters("Table must contain only letters, numbers, and cannot contain "
                                                         "any duplicates")


        elif cipher_mode == 1:
            if sorted(alphabet) == sorted(fc.get_alphabet_full()):
                alphabet = np.array(alphabet).reshape(6, 6)
                table_values = alphabet

            else:
                self.warning_message_missing_letters("Table must contain only letters, numbers, and cannot contain "
                                                     "any duplicates")


    def on_shuffle_button_clicked(self):
        print("shuffle button clicked")
        alphabet = self.get_table_values()
        random.shuffle(alphabet)
        alphabet = np.array(alphabet)
        cipher_mode = self.cipher_mode_comboBox.currentIndex()
        alphabet_mode = self.language_comboBox.currentIndex()

        # noinspection PyBroadException
        try:
            if cipher_mode == 0:
                if alphabet_mode == 0:
                    self.create_english_alphabet(alphabet.reshape(5, 5))
                elif alphabet_mode == 1:
                    self.create_czech_alphabet(alphabet.reshape(5, 5))

            elif cipher_mode == 1:
                self.create_adfgvx_alphabet(alphabet.reshape(6, 6))

        except:
            pass


    def on_clean_button_clicked(self):
        print("clean button clicked")
        self.cipher_table.clear()


    def fill_default_table(self):
        alphabet = fc.get_alphabet_reduced_en_np()
        header = fc.get_adfgx_list()
        for x in range(0, 5):
            for y in range(0, 5):
                table_item = QTableWidgetItem(str(alphabet[x][y]))
                table_item.setTextAlignment(Qt.AlignCenter)
                self.cipher_table.setItem(x, y, table_item)

        self.cipher_table.setHorizontalHeaderLabels(header)
        self.cipher_table.setVerticalHeaderLabels(header)


    def create_english_alphabet(self, alphabet):
        # alphabet = fc.get_alphabet_reduced_en_np()
        header = fc.get_adfgx_list()
        self.cipher_table.setMaximumWidth(300)
        self.cipher_table.setMaximumHeight(300)
        self.cipher_table.setRowCount(5)
        self.cipher_table.setColumnCount(5)
        self.cipher_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.setHorizontalHeaderLabels(header)
        self.cipher_table.setVerticalHeaderLabels(header)

        for x in range(0, 5):
            for y in range(0, 5):
                table_item = QTableWidgetItem(str(alphabet[x][y]))
                table_item.setTextAlignment(Qt.AlignCenter)
                self.cipher_table.setItem(x, y, table_item)


    def create_czech_alphabet(self, alphabet):
        # alphabet = fc.get_alphabet_reduced_cz_np()
        header = fc.get_adfgx_list()
        self.cipher_table.setMaximumWidth(300)
        self.cipher_table.setMaximumHeight(300)
        self.cipher_table.setRowCount(5)
        self.cipher_table.setColumnCount(5)
        self.cipher_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cipher_table.setHorizontalHeaderLabels(header)
        self.cipher_table.setVerticalHeaderLabels(header)

        for x in range(0, 5):
            for y in range(0, 5):
                table_item = QTableWidgetItem(str(alphabet[x][y]))
                table_item.setTextAlignment(Qt.AlignCenter)
                self.cipher_table.setItem(x, y, table_item)


    def create_adfgvx_alphabet(self, alphabet):
        # alphabet = fc.get_alphabet_full_np()
        header = fc.get_adfgvx_list()
        self.language_comboBox.setEnabled(False)

        self.cipher_table.setMaximumWidth(380)
        self.cipher_table.setMaximumHeight(380)
        self.cipher_table.setRowCount(6)
        self.cipher_table.setColumnCount(6)
        self.cipher_table.setColumnWidth(5, 60)
        self.cipher_table.setRowHeight(5, 60)
        self.cipher_table.setHorizontalHeaderLabels(header)
        self.cipher_table.setVerticalHeaderLabels(header)

        for x in range(0, 6):
            for y in range(0, 6):
                table_item = QTableWidgetItem(str(alphabet[x][y]))
                table_item.setTextAlignment(Qt.AlignCenter)
                self.cipher_table.setItem(x, y, table_item)


    def get_table_values(self):
        values = []

        try:
            for row in range(0, self.cipher_table.rowCount()):
                for col in range(0, self.cipher_table.columnCount()):
                    values.append(self.cipher_table.item(row, col).text())

        except:
            pass
            # self.warning_message_missing_letters("You need to fill whole table!")

        return values


    def do_things(self):
        print("Doing things")
        lang = self.language_comboBox.currentIndex()
        cipher_mode = self.cipher_mode_comboBox.currentIndex()
        mode = self.mode_comboBox.currentIndex()
        input_ = self.input_textEdit.toPlainText()
        alphabet = self.get_table_values()
        keyword_ = self.keyword_lineEdit.text()
        keyword_ = fc.parse_keyword(keyword_, lang)

        # encode
        if mode == 0:
            input_ = fc.parse_input(input_, cipher_mode, lang)
            encoded_text = fc.encode(input_, keyword_, alphabet, cipher_mode)
            self.output_textEdit.setText(encoded_text)



        # decode
        elif mode == 1:
            input_ = fc.remove_spaces(input_)
            fc.decode(input_, keyword_, cipher_mode, lang, alphabet)
            # decoded_text = fc.decode(input_, keyword_, alphabet, cipher_mode)
            # print(f"Decoded text: {decoded_text}")
            # self.output_textEdit.setText(decoded_text)























if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle("ADFGVX Cipher")
    sys.exit(app.exec())