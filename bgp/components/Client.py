import random
import socket
import threading
import time
from bgp.components.BgpFunctions import BGP_FSM


class Client(threading.Thread):
    def __init___(self, bind_addr, target_addr):
        self.parent
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
        time.sleep(random.randint(1,5))
        try:
            sock.bind(self.bind_addr)
        except Exception as e:
            print("CANT BIND!", self.bind_addr, e)

        time.sleep(random.randint(3,10))
        sock.connect(self.target_addr)
        while True:
            time.sleep(5)
            BGP_FSM(sock, self.parent)
