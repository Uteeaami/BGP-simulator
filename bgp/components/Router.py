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
        self.update_queue = []
        self.propagate_condition = 0
        self.client = []
        self.lock = threading.Lock()
        self.routingtable = RoutingTable()
        self.server = None     # Tämä on servun IP-osoite
        self.instances_n = 0   # Nämä muuttujat 
        self.instances = 0     # ^^
        self.state = RouterStates.OFFLINE
        self.neighbours = []

    def __str__(self):
        return f"Router {self.name}"
    
    def set_BGPid(self, BGPid):
        self.BGPid = BGPid

    def append_neighbor_ASS(self, ASS):
        self.neighbor_ASS.append(ASS)

    # Probably not needed not 100% sure.
    def add_neighbour_router(self, neighbour):
        self.neighbours.append(neighbour)
        neighbour.neighbours.append(self)

    def add_client(self, client_addr, server_addr):
        self.client.append((client_addr, server_addr))

    # To add an entry, only neighbor router is needed
    # Define other functions so that in the end this function will be called
    def add_routing_table_entry(self, neighbor_router):
        self.routingtable.add_route(
            self.server, neighbor_router.server, "AS_PATH", neighbor_router.AS)
        
    def get_neighbor_router_by_AS(self, AS):
        for neighbor in self.neighbours:
            if neighbor.AS.replace('AS', '') == str(AS):
                return neighbor

    def set_server(self, server_addr):
        self.server = server_addr

    def get_server(self):
        return self.server

    def send_update(self):
        print("asd")

    def run(self):
        time.sleep(random.randint(0,5))
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
        # ServerThread.set_msg("asd")

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
            self.instances += 1

