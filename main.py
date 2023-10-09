import threading
from bgp.components.Router import Router
import logging

"""
Routers have n interfaces that are the independent "connections?" between the routers
The creation of the interface and routers needs to be automated since the simulator is customizeable.
For example the IP_addresses, interface names etc.. need to be randomized.

"""


logging.basicConfig(format='%(message)s', encoding='utf-8', level=logging.DEBUG)

real_address = ["192.168.0.106", "192.168.0.107", "192.168.0.108",
                "192.168.0.109", "192.168.0.103",
                "192.168.0.111", "192.168.0.112", "192.168.0.104",
                "192.168.0.113", "192.168.0.114", "192.168.0.115",
                "192.168.0.116", "192.168.0.119", "192.168.0.120",
                "192.168.0.121", "192.168.0.122", "192.168.0.123",
                "192.168.0.124", "192.168.0.125", "192.168.0.126",
                ]
routers = []

r1 = Router("r1", 1, "AS1")
r2 = Router("r2", 2, "AS2")
r3 = Router("r3", 3, "AS3")
r4 = Router("r4", 4, "AS4")
r5 = Router("r5", 5, "AS5")
r6 = Router("r6", 6, "AS6")
r7 = Router("r7", 7, "AS7")
r8 = Router("r8", 8, "AS8")
r9 = Router("r9", 9, "AS9")
r10 = Router("r10", 10, "AS10")

routers.append(r1)
routers.append(r2)
routers.append(r3)
routers.append(r4)
routers.append(r5)
routers.append(r6)
routers.append(r7)
routers.append(r8)
routers.append(r9)
routers.append(r10)

connections = [
        ("r1", "r2"),
        ("r1", "r3"),
        ("r2", "r4"),
        ("r3", "r6"),
        ("r5", "r6"),
        ("r6", "r8"),
        ("r7", "r1"),
        ("r9", "r4"),
        ("r10", "r5"),
    ]

def create_default_connections():

    servers = []

    for router in routers:
        router.set_server(real_address[0])
        del real_address[0]

    for connect in connections:
        for router in routers:
            if router.name == connect[1]:
                server_addr = router.get_server()
        for router in routers:
            if router.name == connect[0]:
                router.add_client(real_address[0], server_addr)
                #router.add_client(router.get_server(), server_addr)
                # switch these for different amount of interfaces,
                # real_adress[0] specifies new interface for every client connection
                del real_address[0]

def main():

    while (True):
        option1 = input("\nConnect router (or 'enter' to continue): ")
        if option1 == '':
            break
        option2 = input("To: ")

        router1 = next(
            (router for router in routers if router.name == option1), None)
        router2 = next(
            (router for router in routers if router.name == option2), None)

        if router1 and router2:
            connections.append((option1, option2))
        else:
            logging.info("Invalid router name. Please try again.")

        
    create_default_connections()
    for router in routers:
        router.start()


if __name__ == "__main__":
    main()