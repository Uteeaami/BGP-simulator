import time
import random
import threading
import socket
import time
from bgp.components.Client import Client
from bgp.components.RouterStates import RouterStates
from bgp.components.RoutingTable import RoutingTable
from bgp.components.Server import Server

class Router(threading.Thread):
    def __init__(self, name, id, AS):
        super().__init__()
        self.name = name
        self.id = id
        self.BGPid = 0
        self.AS = AS
        self.neighbor_ASS = []
        self.client = []
        self.routingtable = RoutingTable
        self.server = "initialize here only"
        self.state = RouterStates.OFFLINE
        self.neighbours = []

    def __str__(self):
        return f"Router {self.name}"
    
    def set_BGPid(self, BGPid):
        self.BGPid = BGPid

    def append_neighbor_ASS(self, ASS):
        self.neighbor_ASS.append(ASS)

    def add_neighbour_router(self, neighbour):
        self.neighbours.append(neighbour)

    def add_client(self, client_addr, server_addr):
        self.client.append((client_addr, server_addr))
        # self.routingtable.add_connection(self.id, client_addr, server_addr)

    def set_server(self, server_addr):
        self.server = server_addr

    def get_server(self):
        return self.server

    def send_update(self):
        print("asd")

    # one bgp fsm per connection -> selvitä miten toteuttaa fiksusti tilakoneet serverin threadatussa tcp
    # handlerissä. Jos tilakone lähtisisi päälle pelkästä server luokasta olisi tilakoneita vain yksi per palvelin

    def run(self):
        BGPid = random.randint(0, 4294967295)
        self.set_BGPid(BGPid)
        if len(self.client) > 0:
            print("client connections:", self.name, self.client)
        print("server:", self.name, self.server)

        ServerThread = Server()
        ServerThread.set_bind_addr(self.server)
        ServerThread.set_parent(self)
        ServerThread.start()
        time.sleep(1)
        #ServerThread.set_msg("asd")

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

        while True:
            time.sleep(5)
            print(self.neighbor_ASS)
            #print(self.waiting_response)
            #print("Active", self.name)
            #print("connections", self.tcp_connections)
            #break