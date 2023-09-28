import threading
from bgp.globals import *
from bgp.components.Interface import Interface
from bgp.packets.IpPacket import ip_packet_build


class Router:
    def __init__(self, name, id, AS):
        self.id = id
        self.name = name
        self.AS = AS
        self.interfaces = []
        self.connections = []
        self.tcp_connections = []

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
            print("Connection already exists")

    def add_tcp_connection(self, router):
        if router not in self.tcp_connections:
            self.tcp_connections.append(router)
        else:
            print(f"TCP connection to {router.name} already exists.")

    def print_info(self):
        print(f"########### {self.name} Info ###########")
        print("Interfaces:")
        for interface in self.interfaces:
            print(interface)
        print("Connections:")
        for connection in self.connections:
            print(f" - {connection.name}")
