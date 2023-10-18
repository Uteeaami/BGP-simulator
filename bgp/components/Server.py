from socketserver import ThreadingTCPServer
import threading

from bgp.components.Echohandler import Echohandler


class Server(threading.Thread):
    def __init___(self):
        self.parent
        self.bind_addr

    def set_parent(self, parent):
        self.parent = parent

    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

    def run(self):
        print("running server:", self.bind_addr, self.parent.AS)
        handler = Echohandler
        server_socket = ThreadingTCPServer((self.bind_addr,179), handler)
        server_socket.parent = self.parent
        server_socket.serve_forever()
    