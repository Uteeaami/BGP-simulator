import time
import random
import threading
import socket
import time
import struct
from bgp.components.Client import Client
from bgp.components.RouterStates import RouterStates
from bgp.components.RoutingTable import RoutingTable
from bgp.components.Server import Server


# APUA seuraaviin --> miten saada parent paremmin luokalle

# olisi hienoa jos server ja clientti molemmat voisi käyttää samaa logiikkaa, en oo vielä varma toteutuksesta =(
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request
def BGP_FSM(self):
    self.send(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here
    #msg = self.recv(1024)

def BGP_DECODER(msg):
    return True


class Router(threading.Thread):
    def __init__(self, name, id, AS):
        super().__init__()
        self.name = name
        self.id = id
        self.AS = AS
        self.client = []
        self.routingtable = RoutingTable
        self.server = "initialize here only"
        self.state = RouterStates.OFFLINE

    def __str__(self):
        return f"Router {self.name}"

    def add_client(self, client_addr, server_addr):
        self.client.append((client_addr, server_addr))
    
    def set_server(self, server_addr):
        self.server = server_addr

    def get_server(self):
        return self.server

    # one bgp fsm per connection -> selvitä miten toteuttaa fiksusti tilakoneet serverin threadatussa tcp
    # handlerissä. Jos tilakone lähtisisi päälle pelkästä server luokasta olisi tilakoneita vain yksi per palvelin

    def run(self):
        if len(self.client) > 0:
            print("client connections:", self.name, self.client)
        print("server:", self.name, self.server)
        time.sleep(1)

        ServerThread = Server()
        ServerThread.set_bind_addr(self.server)
        ServerThread.set_parent(self)
        ServerThread.start()
        time.sleep(1)
        #ServerThread.set_msg("asd")

        i = 1
        for cli in self.client:
            time.sleep(1)
            client_port = random.randint(1024, 65535)
            client_addr = (cli[0], client_port)
            server_addr = (cli[1], 179)
            ClientThread = Client()
            ClientThread.set_parent(self)
            ClientThread.set_bind_addr(client_addr)
            ClientThread.set_target_addr(server_addr)
            ClientThread.start()
            i += 1 

        while True:
            time.sleep(random.randint(15,20))
            
            #print(self.waiting_response)
            #print("Active", self.name)
            #print("connections", self.tcp_connections)
            #break