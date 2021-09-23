from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys
import os


def writePath(path):
    file = open("music_library.txt", "w")
    file.write(path)
    file.close()
    
    print("Successfully set library path.")

    sys.exit()

def setLibrary():
    app = QApplication(sys.argv)
    windows = QWidget()

    windows.resize(300,100)
    windows.move(200,200)

    windows.setWindowTitle("Set Library Path")
    
    layout = QVBoxLayout()

    label = QLabel()
    label.setText("Please enter your library path:")
    layout.addWidget(label)

    text = QLineEdit()
    layout.addWidget(text)

    btn = QPushButton("Set Library and Close")
    btn.clicked.connect(lambda: writePath(text.text()))
    layout.addWidget(btn)
    
    windows.setLayout(layout)

    windows.show()
    sys.exit(app.exec_())