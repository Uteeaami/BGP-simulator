import time
import random
import threading


class Router:
    def __init__(self, name):
        self.name = name
        self.id = random.randint(0, 10**10)
        self.interfaces = []
        self.connections = []
        self.lock = threading.Lock()

    def add_interface(self, interface):
        with self.lock:
            self.interfaces.append(interface)

    def add_connection(self, router):
        with self.lock:
            self.connections.append(router)

    def send_message(self, message):
        with self.lock:
            print(f"{self.name} sent message: {message}")
            for router in self.connections:
                router.receive_message(message)

    def receive_message(self, message):
        with self.lock:
            print(f"{self.name} received message: {message}")

    def print_interfaces(self):
        with self.lock:
            print(f"########### {self.name} has interfaces ###########")
            for interface in self.interfaces:
                print(interface)


def router_task(router):
    while True:
        message = f"Hello from {router.name}"
        router.send_message(message)
        time.sleep(2)
