from ctypes import c_ushort

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QTimer

import sys
import os
import vlc

import setLibrary

if not os.path.isfile("music_library.txt"):
    setLibrary.setLibrary()

  
class Window(QMainWindow):

    def closeWindow(self):

        try:
            self.player      
        except AttributeError:
            pass
        else:
            if self.player.is_playing():
                msg = QMessageBox.warning(self, "Song is playing", "Would you like to quit anyway?", QMessageBox.Yes | QMessageBox.No)

                if msg == QMessageBox.Yes:
                    self.timer.stop()
                    self.player.stop
                    self.close()
                else:
                    msg.close()
            else:
                self.close()


    def updateProgressbar(self):
        self.percentage = self.player.get_time() / self.player.get_length() * 100

        self.progress.setValue(self.percentage)

    def refreshPathName(self, path):
        self.pathName.setText(path)

    def oneDirBack(self):
        splitted = self.path.split("/")

        self.path = "/".join(splitted[:-2])

        self.refreshPathName(self.path + "/")

        self.refreshList(self.path + "/")

        self.path = self.path + "/"

    def refreshList(self, path):

        self.list.clear()

        for filename in os.scandir(path):
            self.list.addItem(filename.name)

        self.refreshPathName(path)

    def playSong(self, path):
        if path.endswith(".mp3"):

            try:
                self.player      
            except AttributeError:
                pass
            else:
                self.player.pause()

            self.player = vlc.MediaPlayer(path)
            self.player.play()

            self.timer.start(1000)

            splitted = path.split("/")

            self.text.setText(splitted[-1])
        else:
            self.path = path + "/"

            self.refreshList(self.path)
            self.refreshPathName(path)

    def stopSong(self):
        self.player.pause()
        self.player.stop

        self.timer.stop()

    def __init__(self):
        super().__init__()
          
        # string value
        title = "Music Player"
  
        # set the title
        self.setWindowTitle(title)
  
        # setting  the geometry of window
        self.setGeometry(0, 0, 900, 540)

        self.setFixedSize(900, 540)

        self.setStyleSheet("background: #666;")

        # show all the widgets
        self.widgets()

        
    def widgets(self):

        self.stylelist = "QListWidget {background: #333; color: white;} QListWidget::item:selected:active {background: orange} QListWidget::item:selected:!active {background: orange;}"
        self.stylebutton = "QPushButton {background: #333; border: none; color: white;} QPushButton:hover {background: orange;}"
        self.stylebutton_close = "QPushButton {background: #333; border: none; color: white;} QPushButton:hover {background: red;}"
        self.styleprogress = "QProgressBar {background: #333; border: none; text-align: center; color: white;} QProgressBar::chunk {background: orange;}"
        self.styletitle = "color: orange;"
        self.stylepathname = "color: white;"

        self.list = QListWidget(self)
        self.list.resize(860, 300)
        self.list.move(20,50)
        self.list.setStyleSheet(self.stylelist)
        
        file = open("music_library.txt", "r")

        self.path = file.read()

        self.list.itemClicked.connect(lambda: self.playSong(self.path + self.list.currentItem().text()))


        for filename in os.scandir(self.path):
            self.list.addItem(filename.name)

        file.close()

        self.text = QLabel(self)
        self.text.setText("[ Choose Song ]")
        self.text.move(20, 370)
        self.text.resize(840,50)
        self.text.setStyleSheet(self.styletitle)
        
        self.custom_font = QFont("Lato", 25)
        self.custom_font.setWeight(50)

        self.text.setFont(self.custom_font)

        self.btn_play = QPushButton(self)
        self.btn_play.setText("Play")
        self.btn_play.move(20, 450)
        self.btn_play.clicked.connect(self.playSong)
        self.btn_play.setStyleSheet(self.stylebutton)

        self.btn_stop = QPushButton(self)
        self.btn_stop.setText("Stop")
        self.btn_stop.move(140, 450)
        self.btn_stop.clicked.connect(self.stopSong)
        self.btn_stop.setStyleSheet(self.stylebutton)

        self.btn_back = QPushButton(self)
        self.btn_back.setText("Back")
        self.btn_back.move(260, 450)
        self.btn_back.clicked.connect(self.oneDirBack)
        self.btn_back.setStyleSheet(self.stylebutton)

        self.pathName = QLabel(self)
        self.pathName.setText(self.path)
        self.pathName.move(20, 20)
        self.pathName.resize(840, 20)
        self.pathName.setStyleSheet(self.stylepathname)

        self.progress = QProgressBar(self)
        self.progress.move(20, 500)
        self.progress.resize(860, 20)
        self.progress.setMaximum(100)
        self.progress.setStyleSheet(self.styleprogress)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgressbar)

        self.btn_close = QPushButton(self)
        self.btn_close.setText("Close")
        self.btn_close.move(780,450)
        self.btn_close.setStyleSheet(self.stylebutton_close)
        self.btn_close.clicked.connect(self.closeWindow)

        self.show()

  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())