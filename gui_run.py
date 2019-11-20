#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import sys
import cv2
from PyQt5.QtWidgets import (QMainWindow, QApplication,)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPalette, QBrush
from PyQt5.QtCore import QTimer, pyqtSlot, QSize
from helpers.camvideostream import CamVideoStream
from helpers import core, help
import os
'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Base directory were the current file is
iconImg = os.path.join(BASE_DIR, 'icon.png')
errorImg = iconImg
bgImg = os.path.join(BASE_DIR, 'main_window_bg.jpg')
mainUiFile = os.path.join(BASE_DIR, 'mainWindow.ui')
confFile = os.path.join(BASE_DIR, 'configurations.conf')
VIDEO_SOURCE = 0
TRACKING_ACTIVE = 'Tracking activated ....'
APP_READY = 'Ready'
TRAINING_NOW = 'Training ..'
''' ./constants declaration'''

class MainWindow(QMainWindow):
    ''' Qt window object that defines the window of faces tracking '''
    def __init__(self,  parent):
        super(MainWindow, self).__init__()
        loadUi(mainUiFile, self) # Loading UI
        self.setWindowTitle("Face Tracking and Attendance System")
        self.startButton.setCheckable(True)
        self.startButton.clicked.connect(self.startSystem)
        self.training_now = False
        self.fullScreenButton.setCheckable(True)
        self.fullScreenButton.clicked.connect(self.screenFullNormal)
        self.helpButton.clicked.connect(self.help)
        self.quitButton.clicked.connect(self.exitApp)
        self.statusBox.setText(APP_READY)
        self.working = False
        self.dialogs = list() # To be able raise another window (dialog)
        # Setting Background image
        spam = bgImg
        self.mainFrame.setStyleSheet("background-image: url({});".format(spam) )
        self.quitButton.setStyleSheet("color:#ff0000;")

    def changeStatus(self, status):
        self.statusBox.setText(status)

    def screenFullNormal(self):
        status = self.fullScreenButton.text()
        if status == 'Full Screen':
            self.showFullScreen()
            self.fullScreenButton.setText('Normal Size')
        else:
            self.showNormal()
            self.fullScreenButton.setText('Full Screen')

    def startSystem(self):
        if not self.working:
            self.changeStatus(TRACKING_ACTIVE)
            self.feed = CamVideoStream(src=VIDEO_SOURCE, name='Attendance System', loop=True).start()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.loadFeed)
            self.timer.start(1)
            self.working = True
            self.startButton.setText('Stop')
        else:
            try:
                self.timer.stop()
                self.feed.release()
            except Exception as E:
                try:
                    self.feed.stop()
                except Exception as E:
                    print(E)
                    pass
            self.working = False
            self.startButton.setText('Start')
            self.changeStatus(APP_READY)

    def loadFeed(self):
        """ Load feed with opencv from source (webcam) """
        ret, self.img = self.feed.read() #  reading feed frame by frame'
        img2 = core.draw_box(self.img)
        # self.img = cv2.resize(self.img, (250,300))
        self.displayFeed(self.img, 1)
        self.displayFeed(img2, 2)

    def displayFeed(self, fram, window=1):
        """  Method to display feed on viewfield """
        qformat = QImage.Format_Indexed8
        f = cv2.FONT_HERSHEY_TRIPLEX
        try:
            ''' recent version of opencv return '''
            if (len(fram.shape)) == 3:  # [0] : rows, [1] = cols, [2]: channels
                if fram.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
        except:
            text1 = "Error!!!"
            text2 = "Unable to access camera with address: {}".format(VIDEO_SOURCE)
            img = cv2.imread(errorImg, 1)
            img = cv2.putText(img, text1, (0, 70), f, 2, (0, 0, 255)) # BGR
            fram = cv2.putText(img, text2, (0, 130), f, 2, (0, 0, 255) ) # BGR
        try:
            frameI = QImage(fram, fram.shape[1], fram.shape[0], fram.strides[0], qformat)
            # Converting BGR (openCv) to RGB (Qt)
            frameI = frameI.rgbSwapped()
            if window == 1:
                self.mainFrame.setPixmap(QPixmap.fromImage(frameI))
                self.mainFrame.setScaledContents(True)
            else:
                self.responseFrame.setPixmap(QPixmap.fromImage(frameI))
                self.responseFrame.setScaledContents(True)
        except AttributeError:
            print('No more frames')

    def help(self):
        dialog = help.HelpDialog(self)
        self.dialogs.append(dialog)
        dialog.show()

    def exitApp(self):
        try:
            self.timer.stop()
            self.feed.release()
        except Exception as e:
            try:
                self.feed.stop()
            except Exception as e:
                print( str(e) )
                pass
        finally:
            for win in self.dialogs:
                try:
                    win.close()
                except Exception as E:
                    print('[FATAL ERROR]: ', E)
                    pass
            self.close()

def boot():
    app = QApplication([])
    main = MainWindow(None)
    main.setToolTip("Face Tracking and Attendance System")
    main.setWindowIcon(QIcon(iconImg))
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    boot()
