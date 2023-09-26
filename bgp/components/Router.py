import time
import threading
import logging
from bgp.components.Interface import Interface


class Router:
    def __init__(self, name, id, AS):
        self.id = id
        self.name = name
        self.AS = AS
        self.interfaces = []
        self.connections = []
        self.lock = threading.Lock()

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
            new_interface = Interface(f"i{self.id}.{router.id}", f"10.0.{self.id}.{router.id}", self.AS)
            self.add_interface(new_interface)

        if router not in self.connections:
            self.connections.append(router)
        else:
            logging.info("Connection already exists")

    def send_message(self, message):
            logging.info(f"{self.name} sent message: {message}")
            
            for router in self.connections:
                router.receive_message(message)

    def receive_message(self, message):
            logging.info(f"{self.name} received message: {message}")

    def log_info(self):
            logging.info(f"########### {self.name} Info ###########")
            logging.info("Interfaces:")
            for interface in self.interfaces:
                logging.info(interface)
            logging.info("Connections:")
            for connection in self.connections:
                logging.info(f" - {connection.name}")


def router_task(router):
    try:
        while True:
            message = f"Hello from {router.name}"
            router.send_message(message)
            time.sleep(2)
    except Exception as e:
        logging.info(f"Error in thread {router.name}: {e}")

