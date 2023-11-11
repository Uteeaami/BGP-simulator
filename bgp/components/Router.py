from collections import Counter
import time
import random
import threading
import time
from bgp.components.Client import Client
from bgp.components.RouterStates import RouterStates
from bgp.components.RoutingTable import RoutingTable
from bgp.components.TopologyTable import TopologyTable
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
        self.updates = []
        self.propagate_condition = 0
        self.client = []
        self.lock = threading.Lock()
        self.routingtable = RoutingTable()
        self.topologytable = TopologyTable()
        self.server = None     # IP-Address
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

    def add_neighbour_router(self, neighbour):
        self.neighbours.append(neighbour)
        neighbour.neighbours.append(self)

    def add_client(self, client_addr, server_addr):
        self.client.append((client_addr, server_addr))

    def add_neighbor_to_routing_table(self, neighbor):
        self.routingtable.add_route(
            neighbor.server, "0.0.0.0", neighbor.id, 1, neighbor.id
        )

    def add_routing_table_entries(self):
        for entry in self.topologytable.table:
            route = []
            dest_as = entry.get("DEST_AS")
            distance = entry.get("DIST")
            paths = entry.get("PATH")
            for path in paths:
                route.append(path)
            route.append(dest_as[0])
            self.routingtable.add_route(
                dest_as[1], entry.get("NEXT_HOP"), dest_as[0], len(distance) + 1, route)  
    
    def get_neighbor_router_by_AS(self, AS):
        for neighbor in self.neighbours:
            if neighbor.AS.replace('AS', '') == str(AS):
                return neighbor

    def add_entry_to_topology_table(self, as_path, next_hop, nlris):
        for neihgbor in self.neighbours:
            if nlris[0] == neihgbor.id:
                return 
        entry = {
            "NEXT_HOP": next_hop, 
            "DIST": as_path,
            "DEST_AS": nlris[0],
            "PATH": as_path
            }
        self.topologytable.table.append(entry)

    # def build_graph(self):
    #     graph = {}

    #     for entry in self.topologytable.table:
    #         dest_as = entry["DEST_AS"]
    #         dist = entry["DIST"]

    #         dest_as_str = str(dest_as)  # Convert to string

    #         if dest_as_str not in graph:
    #             graph[dest_as_str] = {}

    #         for neighbor in dist:
    #             neighbor_str = str(neighbor)  # Convert to string
    #             graph[dest_as_str][neighbor_str] = 1  # Assuming equal weight for simplicity

    #     return graph

    # def find_shortest_paths(self):
    #     shortest_paths = {}

    #     graph = self.build_graph()

    #     for entry in self.topologytable.table:
    #         dest_as = entry["DEST_AS"]
    #         start_node = entry["DIST"][0]
    #         distances = self.topologytable.dijkstra(graph, start_node)
    #         shortest_paths[dest_as] = distances

        # return shortest_paths

    def set_server(self, server_addr):
        self.server = server_addr

    def get_server(self):
        return self.server

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

