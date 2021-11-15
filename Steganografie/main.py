from os import path
import sys
import pathlib
import re
from PyQt5 import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QDragEnterEvent, QPixmap
from PyQt5.QtWidgets import *
from PIL import Image
from PIL.ImageQt import ImageQt


stylesheet_global = ""


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPixmap(QPixmap(400, 400))
        self.setMaximumSize(400, 400)
        self.setScaledContents(True)
        self.setStyleSheet("""
            QLabel{
                border: 3px solid #2ab9ff;
                margin: 5px;
                margin-left: 15%;
                color: #2ab9ff;
            }
        """)


    def setPixmap(self, image):
        super().setPixmap(image)



class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        width, height = 1080, 860
        self.resize(width, height)
        self.setObjectName("mainWidget")
        self.setAcceptDrops(True)
        # empty_img = Image.new(mode="RGB", size=(100, 100), color=(255, 255, 255))
        # empty_img.save("white_image.png")
        # empty_img = ImageQt(empty_img)

        # create widgets
        self.tedit_input = QTextEdit()
        # self.img_input = QLabel()
        self.lbl_image_input = ImageLabel()
        self.img_output = QLabel()
        self.lbl_prop = QLabel("Image Properties")
        self.lbl_px1 = QLabel("Pixels")
        self.lbl_ext1 = QLabel("Extension")
        self.lbl_path1 = QLabel("Path")
        self.lbl_size1 = QLabel("Size")
        self.lbl_px2 = QLabel("Pixels")
        self.lbl_ext2 = QLabel("Extension")
        self.lbl_path2 = QLabel("Path")
        self.lbl_size2 = QLabel("Size")
        self.wid_container1 = QWidget()
        self.wid_container2 = QWidget()

        self.ledit_px1 = QLineEdit()
        self.ledit_px2 = QLineEdit()
        self.ledit_ext1 = QLineEdit()
        self.ledit_ext2 = QLineEdit()
        self.ledit_path1 = QLineEdit()
        self.ledit_path2 = QLineEdit()
        self.ledit_size1 = QLineEdit()
        self.ledit_size2 = QLineEdit()

        self.btn_load = QPushButton("Load Image")
        self.btn_save = QPushButton("Save Image")
        self.btn_encrypt = QPushButton("Encrypt")
        self.btn_decrypt = QPushButton("Decrypt")

        # self.pixmap_input = QPixmap("test_image.png")
        self.pixmap_output = QPixmap(400, 400)

        # edit widgets
        self.lbl_prop.setObjectName("proplabel")

        self.tedit_input.setPlaceholderText("Input ...")

        # self.img_input.setPixmap(self.pixmap_input)
        # self.img_input.setMaximumSize(400, 400)
        # self.img_input.setScaledContents(True)
        # self.img_input.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # self.img_input.setObjectName("image")
        self.img_output.setPixmap(self.pixmap_output)
        self.img_output.setMaximumSize(400, 400)
        self.img_output.setScaledContents(True)
        # self.img_output.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.img_output.setObjectName("image")
        self.tedit_input.setMaximumWidth(400)
        self.tedit_input.setMinimumWidth(300)
        self.btn_load.clicked.connect(self.load_img)
        self.btn_save.clicked.connect(self.save_img)
        self.btn_encrypt.clicked.connect(self.encrypt)
        self.btn_decrypt.clicked.connect(self.decrypt)
        self.wid_container1.setMinimumWidth(350)
        self.wid_container1.setMaximumWidth(450)
        self.wid_container2.setMinimumWidth(350)
        self.wid_container2.setMaximumWidth(450)

        # create layouts
        self.h_layout_main = QHBoxLayout()
        self.col0 = QVBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        self.col2_v1 = QVBoxLayout()
        self.col2_v2 = QVBoxLayout()
        self.layout_save_load = QHBoxLayout()
        self.layout_ecnrypt_decrypt = QHBoxLayout()
        self.layout_input_tedit = QHBoxLayout()
        self.layout_img = QVBoxLayout()
        self.layout_info_px_1 = QHBoxLayout()
        self.layout_info_ext_1 = QHBoxLayout()
        self.layout_info_path_1 = QHBoxLayout()
        self.layout_info_size1 = QHBoxLayout()
        self.layout_info_px_2 = QHBoxLayout()
        self.layout_info_ext_2 = QHBoxLayout()
        self.layout_info_path_2 = QHBoxLayout()
        self.layout_info_size2 = QHBoxLayout()
        # self.col2.addWidget(
        #     self.lbl_prop,
        #     alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        # )

        # edit layouts
        self.wid_container1.setLayout(self.col2_v1)
        self.wid_container2.setLayout(self.col2_v2)

        # setup layouts
        self.h_layout_main.addLayout(self.col0)
        self.h_layout_main.addLayout(self.col1)
        self.h_layout_main.addLayout(self.col2)
        self.col0.addLayout(self.layout_save_load)
        self.col0.addLayout(self.layout_ecnrypt_decrypt)
        self.col0.addLayout(self.layout_input_tedit)
        self.col1.addLayout(self.layout_img)
        self.col2.addLayout(self.col2_v1)
        self.col2.addLayout(self.col2_v2)
        self.col2_v1.addLayout(self.layout_info_px_1)
        self.col2_v1.addLayout(self.layout_info_ext_1)
        self.col2_v1.addLayout(self.layout_info_path_1)
        self.col2_v1.addLayout(self.layout_info_size1)
        self.col2_v2.addLayout(self.layout_info_px_2)
        self.col2_v2.addLayout(self.layout_info_ext_2)
        self.col2_v2.addLayout(self.layout_info_path_2)
        self.col2_v2.addLayout(self.layout_info_size2)

        # add widgets to layouts
        self.layout_save_load.addWidget(self.btn_load)
        self.layout_save_load.addWidget(self.btn_save)
        self.layout_ecnrypt_decrypt.addWidget(self.btn_encrypt)
        self.layout_ecnrypt_decrypt.addWidget(self.btn_decrypt)
        self.layout_input_tedit.addWidget(self.tedit_input)

        self.layout_img.addWidget(
            self.lbl_image_input, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_img.addWidget(
            self.img_output, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout_info_px_1.addWidget(self.lbl_px1, Qt.AlignmentFlag.AlignCenter)
        self.layout_info_px_1.addWidget(self.ledit_px1)
        self.layout_info_ext_1.addWidget(self.lbl_ext1, Qt.AlignmentFlag.AlignCenter)
        self.layout_info_ext_1.addWidget(self.ledit_ext1)
        self.layout_info_path_1.addWidget(self.lbl_path1, Qt.AlignmentFlag.AlignCenter)
        self.layout_info_path_1.addWidget(self.ledit_path1)
        self.layout_info_size1.addWidget(self.lbl_size1, Qt.AlignmentFlag.AlignCenter)
        self.layout_info_size1.addWidget(self.ledit_size1)

        self.layout_info_px_2.addWidget(self.lbl_px2)
        self.layout_info_px_2.addWidget(self.ledit_px2)
        self.layout_info_ext_2.addWidget(self.lbl_ext2)
        self.layout_info_ext_2.addWidget(self.ledit_ext2)
        self.layout_info_path_2.addWidget(self.lbl_path2)
        self.layout_info_path_2.addWidget(self.ledit_path2)
        self.layout_info_size2.addWidget(self.lbl_size2)
        self.layout_info_size2.addWidget(self.ledit_size2)

        self.col2.addWidget(
            self.wid_container1,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        self.col2.addWidget(
            self.wid_container2,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )

        self.setLayout(self.h_layout_main)


    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()
        

    def dragMoveEvent(self, e):
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasImage:
            viable_extensions = [".png", ".bmp", ".tif", ".tiff", ".raw", ".cr2"]

            e.setDropAction(Qt.CopyAction)
            file_path = e.mimeData().urls()[0].toLocalFile()
            print(f"FILE PATH: {file_path}")

            if file_path:
                path = str(pathlib.PurePath(file_path))

                for ext in viable_extensions:
                    if not (path.endswith(ext)):
                        self.error_msg(
                            f"Unsupported image type. \n"
                            + f"Try one of these {viable_extensions}",
                            "Warning!",
                        )
                        break
                    elif path.endswith(ext):
                        self.set_image(file_path)
                        self.img_output.setPixmap(QPixmap(file_path))
                        e.accept()
                        break
            
            

        else:
            e.ignore()



    def set_image(self, file_path):
        self.lbl_image_input.setPixmap(QPixmap(file_path))


    def error_msg(self, text, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def load_img(self):
        file_path, _ = QFileDialog.getOpenFileName()
        viable_extensions = [".png", ".bmp", ".tif", ".tiff", ".raw", ".cr2"]

        if file_path:
            path = str(pathlib.PurePath(file_path))

            for ext in viable_extensions:
                if not (path.endswith(ext)):
                    self.error_msg(
                        f"Unsupported image type. \n"
                        + f"Try one of these {viable_extensions}",
                        "Warning!",
                    )
                    break
                elif path.endswith(ext):
                    self.img_input.setPixmap(QPixmap(path))
                    break

    def save_img(self):
        pass

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def get_img_props(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dir = pathlib.Path.cwd()
    files = list(dir.glob("**/*"))
    stylesheet_path = ""

    # check files in project
    for file in files:
        file_name = str(file)

        # if qss file is found, then try to load it
        if file_name.endswith(".qss"):
            stylesheet_path = file
            print(file)

        # if qss is not found, look for css and try to load it
        elif file_name.endswith(".css"):
            stylesheet_path = file
            print("Unable to locate PyQt Stylesheet, trying to load css")

    # try to load found file as stylesheet, else load the default style
    try:
        with open(stylesheet_path, "r") as file_:
            print(stylesheet_path)
            app.setStyleSheet(file_.read())
            stylesheet_global = stylesheet_path
        print("Stylesheet loaded successfuly!")

    except:
        print("Unable to load stylesheet, loading default.")
        pass

    window = App()
    window.show()
    window.setWindowTitle("RSA")
    sys.exit(app.exec())
