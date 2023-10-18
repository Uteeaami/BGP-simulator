import socket
import threading
import time
from bgp.components.BgpFunctions import BGP_FSM


class Client(threading.Thread):
    def __init___(self, bind_addr, target_addr):
        self.parent = parent
        self.bind_addr = bind_addr
        self.target_addr = target_addr

    def set_parent(self, parent):
        self.parent = parent

    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

    def set_target_addr(self, target_addr):
        self.target_addr = target_addr

    def run(self):
        print("running client on", self.parent, self.bind_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.bind_addr)
        sock.connect(self.target_addr)
        while True:
            msg = sock.recv(1024)
            time.sleep(5)
            BGP_FSM(sock)    