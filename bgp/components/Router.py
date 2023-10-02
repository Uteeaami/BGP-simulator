import logging
import random
import threading
import time
from bgp.globals import *
from bgp.components.Interface import Interface
from bgp.components.networking.PacketSender import PacketSender
from bgp.components.networking.PacketReceiver import PacketReceiver
from bgp.components.RouterStates import RouterStates


class Router(threading.Thread):
    def __init__(self, name, id, AS):
        super().__init__()
        self.id = id
        self.name = name
        self.AS = AS
        self.packet_queue = []
        self.waiting_response = []
        self.interfaces = []
        self.connections = []
        self.tcp_connections = []
        self.packet_sender = PacketSender(self)
        self.packet_receiver = PacketReceiver(self)
        self.state = RouterStates.OFFLINE
        self.packet_sender_lock = threading.Lock()
        self.packet_receiver_lock = threading.Lock()


    def __str__(self):
        return f"Router {self.name}"

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def add_connection(self, router):
        existing_interface = next((interface for interface in self.interfaces if
                                   interface.name == f"i{self.id}.{router.id}" and
                                   interface.ip_address == f"10.0.{self.id}.{router.id}"),
                                  None)

        if existing_interface:
            new_interface = existing_interface
        else:
            new_interface = Interface(
                f"i{self.id}.{router.id}", f"10.0.{self.id}.{router.id}", self.AS)
            self.add_interface(new_interface)

        if router not in self.connections:
            self.connections.append(router)
        else:
            logging.info("Connection already exists")

    def add_tcp_connection(self, router):
        if router not in self.tcp_connections:
            self.tcp_connections.append(router)
        else:
            logging.info(f"TCP connection to {router.name} already exists.")

    def get_router_by_ip(self, ip_address):
        for router in self.connections:
            for interface in router.interfaces:
                if(interface.ip_address == ip_address):
                    return router

    def get_interface_by_ip(self, ip_address):
        for interface in self.interfaces:
            if interface.ip_address == ip_address:
                return interface
        return None
    
    def get_matching_interfaces(self, neighbor_router):
        matching_interfaces = []
        for own_interface in self.interfaces:
            own_interface_ip = own_interface.ip_address.split(".")
            own_interface_ip_2, own_interface_ip_3 = own_interface_ip[2], own_interface_ip[3]

            for neighbor_interface in neighbor_router.interfaces:
                neighbor_interface_ip = neighbor_interface.ip_address.split(".")
                neighbor_interface_ip_2, neighbor_interface_ip_3 = neighbor_interface_ip[2], neighbor_interface_ip[3]

                if own_interface_ip_2 == neighbor_interface_ip_3 and own_interface_ip_3 == neighbor_interface_ip_2:
                    matching_interfaces.append([own_interface.ip_address, neighbor_interface.ip_address])

        return matching_interfaces if matching_interfaces else None

    def log_info(self):
            logging.info(f"########### {self.name} Info ###########")
            logging.info("Interfaces:")
            for interface in self.interfaces:
                logging.info(interface)
            logging.info("Connections:")
            for connection in self.connections:
                logging.info(f" - {connection.name}")

    def run(self):
        self.state = RouterStates.IDLE
        while self.state != RouterStates.ACTIVE:

            if self.state == RouterStates.IDLE:
                self.state = RouterStates.CONNECTING
                with self.packet_sender_lock:
                    for connection in self.connections:
                        self.packet_sender.send_ip_packet(connection, "SYN")
            
            if  self.packet_queue:
                with self.packet_receiver_lock:
                    packet = self.packet_receiver.receive_packet(self.packet_queue[0])
                    self.packet_queue.pop(0)
                    if packet == True:
                        if self.packet_queue:
                            self.state = RouterStates.CONNECTING
                        else:
                            self.state = RouterStates.ACTIVE

        while True:
            time.sleep(random.randint(15,20))
            print(self.waiting_response)
            print("Active", self.name)
            print("connections", self.tcp_connections)
            break

