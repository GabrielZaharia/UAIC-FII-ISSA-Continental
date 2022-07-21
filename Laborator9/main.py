import socket
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


class data_handler:
    packages_list = []
    completed_packages = []

    def receive_frame(self, fram):
        print(f"Received data {fram.data}")
        # print(f" CRC : {fram.crc}")
        for el in self.packages_list:
            if el.seq_cnt == fram.seq:
                el.add_to_package(fram)
                if el.count == 3:
                    self.on_full_package(el)
                return
        new_package = synchronized_package(fram.seq)
        # new_package.seq_cnt = fram.seq
        new_package.add_to_package(fram)
        self.packages_list.append(new_package)



    def on_full_package(self, package):
        self.packages_list.remove(package)
        package.sort_package()
        package.print_package()
        self.completed_packages.append(package)
        self.update_package_buffer()
        self.print_completed()

    def update_package_buffer(self):
        if len(self.completed_packages) > 3:
            self.sort_completed()
            del self.completed_packages[0]

    def print_completed(self):
        self.sort_completed()
        print(f"Printing package buffer")
        for pack in self.completed_packages:
            print(f"Package {pack.seq_cnt}")
            for frm in pack.frame_list:
                print(f" ID: {frm.id} , SEQ: {frm.seq} , CRC: {frm.crc}, DATA: {frm.data}")

    def sort_completed(self):
        self.completed_packages.sort(key=lambda x: x.seq_cnt, reverse=False)


class frame:
    def __init__(self, idd, seqq, dataa, crcc):
        self.id = idd
        self.seq = seqq
        self.data = dataa
        self.crc = crcc


class synchronized_package:


    def __init__(self, seq):
        self.frame_list = []
        self.seq_cnt = seq
        self.count = 0

    def add_to_package(self, frm):
        # if self.seq_cnt == -1:
        #     self.seq_cnt = frm.seq
        occ = [x for x in self.frame_list if x.id == frm.id]
        if not occ:
            self.frame_list.append(frm)
            self.count += 1

    def sort_package(self):
        self.frame_list.sort(key=lambda x: x.id, reverse=False)

    def print_package(self):
        print(f"Completed package {self.seq_cnt}")
        for frm in self.frame_list:
            print(f" ID: {frm.id} , SEQ: {frm.seq} , CRC: {frm.crc}, DATA: {frm.data}")



def read_message(sSocket):
    try:
        id = sSocket.recv(4)
        sequence = sSocket.recv(4)
        payload = sSocket.recv(500)
        payload.split(b'\\x')
        data_list =[]
        for el in payload:
            data_list.append(el)
        crc = sSocket.recv(4)
        id = int.from_bytes(id, "big", signed=False)
        sequence = int.from_bytes(sequence, "big", signed=False)
        # payload = int.from_bytes(payload, "big")
        # crc=crc.decode('UTF-8')
        crc = int.from_bytes(crc, 'big', signed=False)
        received_frame = frame(id, sequence, data_list, crc)
        return received_frame
    except:
        return None

def is_still_connected(sock):
    try:
        sock.sendall(b"ping")
        return True
    except:
        return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    dat = data_handler()
    # s.sendall(b"Hello, world")
    while is_still_connected(s):

        frm = read_message(s)
        if frm:
            dat.receive_frame(frm)

