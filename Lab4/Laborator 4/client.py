# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading
import sys, time

HOST = 'localhost'
PORT = 5005
client = 0

led0_flag = False
led1_flag = False
led2_flag = False
led3_flag = False


class Ui_MainWindow(object):
    server_socket = []
    diag_mode = -1
    dtcValue1 = -1
    dtcValue2 = -1
    dtcValue3 = -1
    dtcValue4 = -1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 500)
        MainWindow.setMinimumSize(QtCore.QSize(658, 500))
        MainWindow.setMaximumSize(QtCore.QSize(658, 500))
        self.logo_img = QtGui.QPixmap('./rsz_conti.png')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setWindowTitle('Client')
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(150, 20, 400, 100))
        self.logo.setObjectName("logo")
        self.connected_msg = QtWidgets.QLabel(self.centralwidget)
        self.connected_msg.setGeometry(QtCore.QRect(292, 175, 85, 30))
        self.connected_msg.setObjectName("connected_msg")
        self.connected_msg.setStyleSheet("font: bold; color: green")
        self.not_diag_mode = QtWidgets.QLabel(self.centralwidget)
        self.not_diag_mode.setGeometry(QtCore.QRect(272, 187, 120, 30))
        self.not_diag_mode.setObjectName("not_diag_mode")
        self.not_diag_mode.setStyleSheet("font: bold; color: red")
        self.not_diag_mode.setVisible(False)
        self.diagMode = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode.setGeometry(QtCore.QRect(185, 210, 131, 41))
        self.diagMode.setObjectName("diagMode")
        self.diagMode.clicked.connect(self.diag)
        self.diagMode.setEnabled(False)
        self.diagMode_off = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode_off.setGeometry(QtCore.QRect(325, 210, 131, 41))
        self.diagMode_off.setObjectName("diagMode")
        self.diagMode_off.setEnabled(False)
        self.diagMode_off.clicked.connect(self.stop_diag)

        self.set_led0 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led0.setGeometry(QtCore.QRect(30, 310, 81, 31))
        self.set_led0.clicked.connect(self.set_led0_flags)

        self.set_led1 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led1.setGeometry(QtCore.QRect(30, 350, 81, 31))
        self.set_led1.clicked.connect(self.set_led1_flags)

        self.set_led2 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led2.setGeometry(QtCore.QRect(30, 390, 81, 31))
        self.set_led2.clicked.connect(self.set_led2_flags)

        self.set_led3 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led3.setGeometry(QtCore.QRect(30, 430, 81, 31))
        self.set_led3.clicked.connect(self.set_led3_flags)

        self.led0_state = QtWidgets.QLabel(self.centralwidget)
        self.led0_state.setGeometry(QtCore.QRect(140, 313, 25, 25))
        self.led0_state.setVisible(False)

        self.led1_state = QtWidgets.QLabel(self.centralwidget)
        self.led1_state.setGeometry(QtCore.QRect(140, 353, 25, 25))
        self.led1_state.setVisible(False)

        self.led2_state = QtWidgets.QLabel(self.centralwidget)
        self.led2_state.setGeometry(QtCore.QRect(140, 393, 25, 25))
        self.led2_state.setVisible(False)

        self.led3_state = QtWidgets.QLabel(self.centralwidget)
        self.led3_state.setGeometry(QtCore.QRect(140, 433, 25, 25))
        self.led3_state.setVisible(False)

        self.set_led_title = QtWidgets.QLabel(self.centralwidget)
        self.set_led_title.setGeometry(QtCore.QRect(75, 270, 92, 21))
        self.set_led_title.setObjectName("set_led_title")
        self.set_led_title.setStyleSheet("font:bold; font-size:11px;")
        self.read_dtc_title = QtWidgets.QLabel(self.centralwidget)
        self.read_dtc_title.setGeometry(QtCore.QRect(470, 270, 101, 20))
        self.read_dtc_title.setObjectName("read_dtc_title")
        self.read_dtc_title.setStyleSheet("font:bold; font-size:11px;")

        self.dtc1 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc1.setGeometry(QtCore.QRect(460, 310, 81, 31))
        self.dtc1.clicked.connect(lambda: self.get_dtc_state('01'))

        self.dtc2 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc2.setGeometry(QtCore.QRect(460, 350, 81, 31))
        self.dtc2.clicked.connect(lambda: self.get_dtc_state('02'))

        self.dtc3 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc3.setGeometry(QtCore.QRect(460, 390, 81, 31))
        self.dtc3.clicked.connect(lambda: self.get_dtc_state('03'))

        self.dtc4 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc4.setGeometry(QtCore.QRect(460, 430, 81, 31))
        self.dtc4.clicked.connect(lambda: self.get_dtc_state('04'))

        self.dtc1_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc1_state.setGeometry(QtCore.QRect(570, 315, 65, 20))
        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue')

        self.dtc2_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc2_state.setGeometry(QtCore.QRect(570, 355, 65, 20))
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue')

        self.dtc3_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc3_state.setGeometry(QtCore.QRect(570, 395, 65, 20))
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue')

        self.dtc4_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc4_state.setGeometry(QtCore.QRect(570, 435, 65, 20))
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue')

        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(260, 130, 131, 51))
        self.connect.setObjectName("connect")
        self.connect.clicked.connect(self.start_client)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setPixmap(self.logo_img)
        self.connected_msg.setText(_translate("MainWindow", ""))
        self.not_diag_mode.setText(_translate("MainWindow", "NOT IN DIAG MODE"))
        self.diagMode.setText(_translate("MainWindow", "Enter Diag Mode"))
        self.diagMode_off.setText(_translate("MainWindow", "Stop Diag Mode"))
        self.set_led0.setText(_translate("MainWindow", "Set LED0"))
        self.set_led1.setText(_translate("MainWindow", "Set LED1"))
        self.set_led2.setText(_translate("MainWindow", "Set LED2"))
        self.set_led3.setText(_translate("MainWindow", "Set LED3"))

        self.set_led_title.setText(_translate("MainWindow", "SET LED STATES"))
        self.read_dtc_title.setText(_translate("MainWindow", "READ DTC STATES"))
        self.dtc3.setText(_translate("MainWindow", "Read DTC3"))
        self.dtc2.setText(_translate("MainWindow", "Read DTC2"))
        self.dtc1.setText(_translate("MainWindow", "Read DTC1"))
        self.dtc4.setText(_translate("MainWindow", "Read DTC4"))
        self.led0_state.setText(_translate("MainWindow", ""))
        self.led1_state.setText(_translate("MainWindow", ""))
        self.led2_state.setText(_translate("MainWindow", ""))
        self.led3_state.setText(_translate("MainWindow", ""))
        self.connect.setText(_translate("MainWindow", "CONNECT"))

    ############################### EXERCISE 0 ###############################
    def start_client(self):
        q = -1
        self.diagMode.setEnabled(True)
        self.diagMode_off.setEnabled(False)

        self.dtc1.setEnabled(True)
        self.dtc2.setEnabled(True)
        self.dtc3.setEnabled(True)
        self.dtc4.setEnabled(True)

        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED1')
        self.set_led3.setText('Set LED3')

        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue;')
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue;')
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue;')
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue;')

        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED2')
        self.set_led3.setText('Set LED3')

        self.led0_state.setVisible(False)
        self.led1_state.setVisible(False)
        self.led2_state.setVisible(False)
        self.led3_state.setVisible(False)
        ''' Complete with necessary code'''
        s = socket.socket()
        s.connect((HOST, PORT))
        self.server_socket = s
        self.recv_messages()
        self.diag_mode = 0


    ############################### EXERCISE 1 ###############################
    def recv_handler(self, stop_event):
        while True:
            message = self.server_socket.recv(1024).decode()
            print(message)
            if "0x62" in str(message):
                ledNr = str(message)[4:6]
                print(ledNr)
                if self.diag_mode:
                    if ledNr == "01":
                        self.set_dtc1_state(str(message)[-5:])
                    elif ledNr == "02":
                        self.set_dtc2_state(str(message)[-5:])
                    elif ledNr == "03":
                        self.set_dtc3_state(str(message)[-5:])
                    elif ledNr == "04":
                        self.set_dtc4_state(str(message)[-5:])
            if "0x6E" in str(message):
                ledNr = str(message)[4:6]
                print(ledNr)
                if self.diag_mode:
                    if ledNr == "00":
                        self.set_led0_label(str(message)[-1:])
                    elif ledNr == "01":
                        self.set_led1_label(str(message)[-1:])
                    elif ledNr == "02":
                        self.set_led2_label(str(message)[-1:])
                    elif ledNr == "03":
                        self.set_led3_label(str(message)[-1:])
        pass

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    def diag(self):
        print("here")
        self.server_socket.send(str(0x3E01).encode())
        self.diag_mode = 1
        self.diagMode.setEnabled(False)
        self.diagMode_off.setEnabled(True)
        print(self.diag_mode)
        pass

    def stop_diag(self):
        self.server_socket.send(str(0x3E00).encode())
        self.diag_mode = 0
        self.diagMode.setEnabled(True)
        self.diagMode_off.setEnabled(False)
        print(self.diag_mode)
        pass

    ############################### EXERCISE 3 ###############################
    # READ DTC's
    def get_dtc_state(self, dtc_string):
        if self.diag_mode:
            message = "0x22" + dtc_string
            self.server_socket.send(message.encode())
        pass

    # SET DTC1 State
    def set_dtc1_state(self, data_recv):
        if data_recv == "02550":
            self.dtc1_state.setText("good")
            self.dtc1_state.setStyleSheet('font:bold; color: green;')
            self.dtcValue1 = 1
        elif data_recv == "25500":
            self.dtc1_state.setText("bad")
            self.dtc1_state.setStyleSheet('font:bold; color: red;')
            self.dtcValue1 = 0
        pass

    # SET DTC2 State
    def set_dtc2_state(self, data_recv):
        if data_recv == "02550":
            self.dtc2_state.setText("good")
            self.dtc2_state.setStyleSheet('font:bold; color: green;')
            self.dtcValue2 = 1
        elif data_recv == "25500":
            self.dtc2_state.setText("bad")
            self.dtc2_state.setStyleSheet('font:bold; color: red;')
            self.dtcValue2 = 0
        pass

    # SET DTC3 State
    def set_dtc3_state(self, data_recv):
        if data_recv == "02550":
            self.dtc3_state.setText("good")
            self.dtc3_state.setStyleSheet('font:bold; color: green;')
            self.dtcValue3 = 1
        elif data_recv == "25500":
            self.dtc3_state.setText("bad")
            self.dtc3_state.setStyleSheet('font:bold; color: red;')
            self.dtcValue3 = 0
        pass

    # SET DTC4 State
    def set_dtc4_state(self, data_recv):
        if data_recv == "02550":
            self.dtc4_state.setText("good")
            self.dtc4_state.setStyleSheet('font:bold; color: green;')
            self.dtcValue4 = 1
        elif data_recv == "25500":
            self.dtc4_state.setText("bad")
            self.dtc4_state.setStyleSheet('font:bold; color: red;')
            self.dtcValue4 = 0
        pass

    ############################### EXERCISE 4 ###############################

    # SET LED0
    def set_led0_label(self, data_recv):
        global led0_flag
        self.led0_state.setVisible(True)
        print(f"halp {data_recv}")
        if data_recv == "1":
            self.led0_state.setStyleSheet("background-color: green")
            led0_flag = True
        else:
            self.led0_state.setStyleSheet("background-color: red")
            led0_flag = False
        pass

    def set_led0_flags(self):
        global led0_flag
        message = "0x2E00"

        if led0_flag == False:
            message += "1"
        else:
            message += "0"

        self.server_socket.send(message.encode())
        pass

    # SET LED1
    def set_led1_label(self, data_recv):
        global led1_flag
        self.led1_state.setVisible(True)
        if data_recv == "1":
            self.led1_state.setStyleSheet("background-color: green")
            led1_flag = True
        else:
            self.led1_state.setStyleSheet("background-color: red")
            led1_flag = False
        pass

    def set_led1_flags(self):
        global led1_flag
        message = "0x2E01"
        if led1_flag == False:
            message += "1"
        else:
            message += "0"
        self.server_socket.send(message.encode())
        pass

    # SET LED2
    def set_led2_label(self, data_recv):
        global led2_flag
        self.led2_state.setVisible(True)
        if data_recv == "1":
            self.led2_state.setStyleSheet("background-color: green")
            led2_flag = True
        else:
            self.led2_state.setStyleSheet("background-color: red")
            led2_flag = False
        pass

    def set_led2_flags(self):
        global led2_flag
        message = "0x2E02"
        if led2_flag == False:
            message += "1"
        else:
            message += "0"
        self.server_socket.send(message.encode())
        pass

    # SET LED3
    def set_led3_label(self, data_recv):
        global led3_flag
        self.led3_state.setVisible(True)
        if data_recv == "1":
            self.led3_state.setStyleSheet("background-color: green")
            led3_flag = True
        else:
            self.led3_state.setStyleSheet("background-color: red")
            led3_flag = False
        pass

    def set_led3_flags(self):
        global led3_flag
        message = "0x2E03"
        if led3_flag == False:
            message += "1"
        else:
            message += "0"
        self.server_socket.send(message.encode())
        pass

    ##########################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
