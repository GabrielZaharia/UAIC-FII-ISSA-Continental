from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import rsa_library
import _pickle as cPickle
import os
import threading
import sys, time

HOST = 'localhost'
PORT = 12346

airbag_on = int('0xfe01', 16)
corrupted_low = int('0x5732', 16)
corrupted_high = int('0x5701', 16)


class Ui_MainWindow(object):
    public_pair = []
    private_pair = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 500)
        MainWindow.setWindowTitle('Client')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("background-color:white;")

        # Start client button
        self.client_start = QtWidgets.QPushButton(MainWindow)
        self.client_start.setText("Connect client")
        self.client_start.setStyleSheet("font: bold; font-size: 15px;")
        self.client_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.client_start.clicked.connect(self.start_client)

        self.client_label = QtWidgets.QLabel(self.centralwidget)
        self.client_label.setGeometry(QtCore.QRect(320, 170, 205, 41))
        self.client_label.setStyleSheet("font:bold;font-size: 15px;")

        # Connected label
        self.connected_label = QtWidgets.QLabel(self.centralwidget)
        self.connected_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.connected_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Airbag on
        self.airbag = QtWidgets.QPushButton(MainWindow)
        self.airbag.setText("Airbag on")
        self.airbag.setStyleSheet("font: bold; font-size: 15px;")
        self.airbag.setGeometry(QtCore.QRect(70, 260, 211, 41))
        self.airbag.clicked.connect(self.send_on_data)
        self.airbag.setEnabled(False)

        # Airbag on label
        self.airbag_on_label = QtWidgets.QLabel(self.centralwidget)
        self.airbag_on_label.setGeometry(QtCore.QRect(300, 260, 200, 40))
        self.airbag_on_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Corrupted low
        self.corrupted_low = QtWidgets.QPushButton(MainWindow)
        self.corrupted_low.setText("Corrupted low")
        self.corrupted_low.setStyleSheet("font: bold; font-size: 15px;")
        self.corrupted_low.setGeometry(QtCore.QRect(70, 330, 211, 41))
        self.corrupted_low.clicked.connect(self.send_corrupted_low)
        self.corrupted_low.setEnabled(False)

        # Corrupted low label
        self.corrupted_low_label = QtWidgets.QLabel(self.centralwidget)
        self.corrupted_low_label.setGeometry(QtCore.QRect(300, 330, 200, 40))
        self.corrupted_low_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Corrupted high
        self.corrupted_high = QtWidgets.QPushButton(MainWindow)
        self.corrupted_high.setText("Corrupted high")
        self.corrupted_high.setStyleSheet("font: bold; font-size: 15px;")
        self.corrupted_high.setGeometry(QtCore.QRect(70, 400, 211, 41))
        self.corrupted_high.clicked.connect(self.send_corrupted_high)
        self.corrupted_high.setEnabled(False)

        # Corrupted high label
        self.corrupted_high_label = QtWidgets.QLabel(self.centralwidget)
        self.corrupted_high_label.setGeometry(QtCore.QRect(300, 400, 200, 40))
        self.corrupted_high_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 5 ###############################
    def start_client(self):
        self.corrupted_low_label.clear()
        self.airbag_on_label.clear()
        self.corrupted_high_label.clear()
        self.airbag.setEnabled(False)
        self.corrupted_high.setEnabled(False)
        self.corrupted_low.setEnabled(False)
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((HOST, PORT))

        # receive data from the server and decoding to get the string.
        public_pair = s.recv(1024).decode()
        private_pair = s.recv(1024).decode()
        sep = public_pair.find(":")
        public_pair = (int(public_pair[:sep]), int(public_pair[sep + 1:]))
        sep = private_pair.find(":")
        private_pair = (int(private_pair[:sep]), int(private_pair[sep + 1:]))
        print(public_pair)
        print(private_pair)
        self.public_pair = public_pair
        self.private_pair = private_pair
        received_message = s.recv(1024).decode()
        print(f"Before print: {received_message}")
        self.unlock_car = rsa_library.decrypt(self.private_pair, int(received_message))
        # self.unlock_car = "Ma-ta"
        print(received_message)
        print(hex(self.unlock_car))
        self.server_socket = s
        self.recv_messages()

        # close the connection

        ''' complete with necesarry code '''

    ############################### EXERCISE 8 ###############################
    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    def recv_handler(self, stop_event):
        # self.unlock_car = self.server_socket.recv(1024).decode()

        while True:
            message = int(self.server_socket.recv(1024).decode())
            decrypted_message = rsa_library.decrypt(self.private_pair, message)
            print(f" I receive {decrypted_message} ")
            if decrypted_message == self.unlock_car:
                self.airbag.setEnabled(True)
                self.corrupted_low.setEnabled(True)
                self.corrupted_high.setEnabled(True)
            if decrypted_message == 0:
                self.corrupted_low_label.setText("Corrupted")
            if decrypted_message == 105:
                self.airbag_on_label.setText("All good")

        pass
        ''' complete with necesarry code '''

    ############################### EXERCISE 9 ###############################
    def send_on_data(self):
        self.clear_messages()
        print("Trying")
        message = rsa_library.encrypt(self.public_pair, hex(airbag_on))
        print(f" I send this : {message} ")
        self.server_socket.send(str(message).encode())
        pass
        ''' complete with necesarry code '''

    ############################### EXERCISE 10 ###############################
    def send_corrupted_low(self):
        self.clear_messages()
        self.airbag.setEnabled(False)
        print("Trying")
        message = rsa_library.encrypt(self.public_pair, hex(corrupted_low))
        print(f" I send this message: {message} ")
        self.server_socket.send(str(message).encode())
        pass
        ''' complete with necesarry code '''

    ############################### EXERCISE 11 ###############################
    def send_corrupted_high(self):
        self.clear_messages()
        self.airbag.setEnabled(False)
        print("Trying")
        message = rsa_library.encrypt(self.public_pair, hex(corrupted_high))
        print(f" I send this message: {message} ")
        self.server_socket.send(str(message).encode())
        pass
        ''' complete with necesarry code '''
    def clear_messages(self):
        self.corrupted_low_label.setText("")
        self.airbag_on_label.setText("")


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()
    sys.exit(app.exec_())

me = os.getpid()
kill_proc_tree(me)
