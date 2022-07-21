#!/usr/bin/env python
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread
import socket
import os
import threading
import sys, time

HOST = 'localhost'
PORT = 5005

server_created_flag = False
global server
global conn


class Ui_MainWindow(object):
    client_socket = []
    diag_mode = -1
    dtcValue1 = -1
    dtcValue2 = -1
    dtcValue3 = -1
    dtcValue4 = -1

    def setupUi(self, MainWindow):
        global server_created_flag
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 800)
        MainWindow.setWindowTitle('Server')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("background-color:white;")

        # Start server button
        self.server_start = QtWidgets.QPushButton(MainWindow)
        self.server_start.setText("Start server")
        self.server_start.setStyleSheet("font: bold; font-size: 15px;")
        self.server_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.server_start.clicked.connect(self.start_server)

        ### Set DTC

        # Set DTC1
        self.dtc1 = QtWidgets.QPushButton(MainWindow)
        self.dtc1.setText("Set DTC1 active")
        self.dtc1.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc1.setGeometry(QtCore.QRect(70, 300, 200, 40))
        self.dtc1.clicked.connect(lambda: self.set_dtc1(7, 0.1))

        # Set DTC2
        self.dtc2 = QtWidgets.QPushButton(MainWindow)
        self.dtc2.setText("Set DTC2 active")
        self.dtc2.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc2.setGeometry(QtCore.QRect(70, 370, 200, 40))
        self.dtc2.clicked.connect(lambda: self.set_dtc2(6, 0.1))

        # Set DTC3
        self.dtc3 = QtWidgets.QPushButton(MainWindow)
        self.dtc3.setText("Set DTC3 active")
        self.dtc3.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc3.setGeometry(QtCore.QRect(70, 440, 200, 40))
        self.dtc3.clicked.connect(lambda: self.set_dtc3(5, 0.1))

        # Set DTC4
        self.dtc4 = QtWidgets.QPushButton(MainWindow)
        self.dtc4.setText("Set DTC4 active")
        self.dtc4.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc4.setGeometry(QtCore.QRect(70, 510, 200, 40))
        self.dtc4.clicked.connect(lambda: self.set_dtc4(4, 0.1))

        ### LEDS
        # Led 1
        self.led1_state = QtWidgets.QLabel(MainWindow)
        self.led1_state.setGeometry(QtCore.QRect(330, 300, 40, 40))

        # Led 2
        self.led2_state = QtWidgets.QLabel(MainWindow)
        self.led2_state.setGeometry(QtCore.QRect(330, 370, 40, 40))

        # Led 3
        self.led3_state = QtWidgets.QLabel(MainWindow)
        self.led3_state.setGeometry(QtCore.QRect(330, 441, 40, 40))

        # Led 4
        self.led4_state = QtWidgets.QLabel(MainWindow)
        self.led4_state.setGeometry(QtCore.QRect(330, 510, 40, 40))

        # Set all DTC's
        self.set_all_dtc = QtWidgets.QPushButton(MainWindow)
        self.set_all_dtc.setText("Set all DTC")
        self.set_all_dtc.setStyleSheet("font: bold; font-size: 15px;")
        self.set_all_dtc.setGeometry(QtCore.QRect(70, 580, 200, 40))
        self.set_all_dtc.clicked.connect(self.set_all)

        # Start server label
        self.server_label = QtWidgets.QLabel(self.centralwidget)
        self.server_label.setText("Client connected")
        self.server_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.server_label.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")
        self.server_label.setVisible(False)

        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        self.conti_label.setStyleSheet("qproperty-alignment: AlignCenter;")
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 0 ###############################
    def start_server(self):
        self.set_all_dtc.setText('Set all DTC')

        self.dtc1.setText("Set DTC1 active")
        self.dtc2.setText("Set DTC2 active")
        self.dtc3.setText("Set DTC3 active")
        self.dtc4.setText("Set DTC4 active")

        self.led1_state.setStyleSheet('')
        self.led2_state.setStyleSheet('')
        self.led3_state.setStyleSheet('')
        self.led4_state.setStyleSheet('')
        ''' Complete with necessary code'''
        thr = threading.Thread(target=self.server_thread)
        thr.start()

    def server_thread(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', PORT))
        s.listen(5)
        c, addr = s.accept()
        self.server_label.setVisible(True)
        print('Got connection from', addr)
        self.client_socket = c
        self.recv()

    ############################### EXERCISE 1 ###############################
    def recv_handler(self, stop_event):
        while True:
            message = self.client_socket.recv(1024).decode()
            print(message)
            if "0x3E" in str(message):
                message = int(message)
                mode = message & 0xff
                self.diag_mode = mode
            if "0x22" in str(message):
                ledNr = str(message)[-2:]
                ledNr = int(ledNr)
                if ledNr == 1:
                    self.read_dtc1(str(message))
                elif ledNr == 2:
                    self.read_dtc2(str(message))
                elif ledNr == 3:
                    self.read_dtc3(str(message))
                else:
                    self.read_dtc4(str(message))
            if "0x2E" in str(message):
                # message[2]="6"
                ledNr = str(message)[4:6]
                if ledNr == "00":
                    self.set_led0(str(message))
                elif ledNr=="01":
                    self.set_led1(str(message))
                elif ledNr == "02":
                    self.set_led2(str(message))
                else:
                    self.set_led3(str(message))

        pass

    def recv(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    ############################### EXERCISE 2 ###############################
    # DTC1
    def set_dtc1(self, led, bright):
        # print(self.dtcValue1)
        print(f" {bright} : {self.dtcValue1}")
        if bright == 0.1:
            if self.dtcValue1 == -1:
                self.dtcValue1 = 1
            else:
                self.dtcValue1 = (self.dtcValue1 + 1) % 2
        else:
            self.dtcValue1 = bright

        print(f" 1 {self.dtcValue1}")
        # print(self.dtcValue1)
        if self.dtcValue1 == 1:
            self.led1_state.setStyleSheet("background-color: green;")
        else:
            self.led1_state.setStyleSheet("background-color: red")
        # color = self.led1_state.palette().button().color().name()
        # if color == "#008000":
        #
        # if color == "#ff0000" or color == "#f0f0f0":
        #
        # print(self.led1_state.palette().button().color().name())

        pass

    # DTC2
    def set_dtc2(self, led, bright):
        if bright == 0.1:
            if self.dtcValue2 == -1:
                self.dtcValue2 = 1
            else:
                self.dtcValue2 = (self.dtcValue2 + 1) % 2
        else:
            self.dtcValue2 = bright

        print(f" 1 {self.dtcValue2}")
        # print(self.dtcValue1)
        if self.dtcValue2 == 1:
            self.led2_state.setStyleSheet("background-color: green;")
        else:
            self.led2_state.setStyleSheet("background-color: red")
        pass

    # DTC3
    def set_dtc3(self, led, bright):
        # if bright != 0.1:
        if bright == 0.1:
            if self.dtcValue3 == -1:
                self.dtcValue3 = 1
            else:
                self.dtcValue3 = (self.dtcValue3 + 1) % 2
        else:
            self.dtcValue3 = bright

        print(f" 1 {self.dtcValue3}")
        # print(self.dtcValue1)
        if self.dtcValue3 == 1:
            self.led3_state.setStyleSheet("background-color: green;")
        else:
            self.led3_state.setStyleSheet("background-color: red")
        pass

    # DTC4
    def set_dtc4(self, led, bright):
        if bright == 0.1:
            if self.dtcValue4 == -1:
                self.dtcValue4 = 1
            else:
                self.dtcValue4 = (self.dtcValue4 + 1) % 2
        else:
            self.dtcValue4 = bright

        print(f" 1 {self.dtcValue4}")
        # print(self.dtcValue1)
        if self.dtcValue4 == 1:
            self.led4_state.setStyleSheet("background-color: green;")
        else:
            self.led4_state.setStyleSheet("background-color: red")
        pass

    def set_all(self):
        bright = self.dtcValue1
        bright = (bright + 1) % 2
        self.set_dtc1(0,bright=bright)
        self.set_dtc2(0,bright=bright)
        self.set_dtc3(0,bright=bright)
        self.set_dtc4(0,bright=bright)
        pass

    ############################### EXERCISE 3 ###############################
    def read_dtc1(self, data):
        ledNr = data[-2:]
        message = "0x62" + ledNr
        if self.dtcValue1 == 1:
            message += "02550"
        if self.dtcValue1 == 0:
            message += "25500"
        self.client_socket.send(message.encode())
        pass

    def read_dtc2(self, data):
        ledNr = data[-2:]
        message = "0x62" + ledNr
        if self.dtcValue2 == 1:
            message += "02550"
        if self.dtcValue2 == 0:
            message += "25500"
        self.client_socket.send(message.encode())
        pass

    def read_dtc3(self, data):
        ledNr = data[-2:]
        message = "0x62" + ledNr
        if self.dtcValue3 == 1:
            message += "02550"
        if self.dtcValue3 == 0:
            message += "25500"
        self.client_socket.send(message.encode())
        pass

    def read_dtc4(self, data):
        ledNr = data[-2:]
        message = "0x62" + ledNr
        if self.dtcValue4 == 1:
            message += "02550"
        if self.dtcValue4 == 0:
            message += "25500"
        self.client_socket.send(message.encode())
        pass

    ############################### EXERCISE 4 ###############################
    def set_led0(self, data):
        data = data[:2] + "6" + data[3:]
        print(f" Received : {data}")
        self.client_socket.send(data.encode())
        pass

    def set_led1(self, data):
        data = data[:2] + "6" + data[3:]
        self.client_socket.send(data.encode())
        pass

    def set_led2(self, data):
        data = data[:2] + "6" + data[3:]
        self.client_socket.send(data.encode())
        pass

    def set_led3(self, data):
        data = data[:2] + "6" + data[3:]
        self.client_socket.send(data.encode())
        pass


##########################################################################


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


def main():
    global server_created_flag
    import sys
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
