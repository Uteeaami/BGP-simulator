import logging
from bgp.components.Router import Router
from bgp.simulation.TcpConnection import tcp_connection
from bgp.globals import *

"""
Routers have n interfaces that are the independent "connections?" between the routers
The creation of the interface and routers needs to be automated since the simulator is customizeable.
For example the IP_addresses, interface names etc.. need to be randomized.

"""

# These could be somewhere else idk and done better

logging.basicConfig(format='%(message)s', encoding='utf-8', level=logging.DEBUG)

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


def create_default_connections():
    """
        r1 has r2, r3, r7
        r2 has r1, r4
        r3 has r1, r6
        r4 has r2, r9
        r5 has r6, r10
        r6 has r3, r5, r8
        r7 has r1
        r8 has r6
        r9 has r4
        r10 has r5
    """
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

    for src, dest in connections:
        src_router = next(router for router in routers if router.name == src)
        dest_router = next(router for router in routers if router.name == dest)
        src_router.add_connection(dest_router)
        dest_router.add_connection(src_router)


def main():

    logging.info("\nBGP-Simulator")
    logging.info("First, connect routers to each other by typing 'r1' and 'r2' for example")

    while (True):
        option1 = input("\nConnect router (or 'q' to quit): ")
        if option1 == 'q':
            break
        option2 = input("To: ")

        router1 = next(
            (router for router in routers if router.name == option1), None)
        router2 = next(
            (router for router in routers if router.name == option2), None)

        if router1 and router2:
            router1.add_connection(router2)
            router2.add_connection(router1)
        else:
            logging.info("Invalid router name. Please try again.")

    # Check if any routers are not connected and add default connections
    unconnected_routers = [
        router for router in routers if not router.connections]
    if unconnected_routers:
        logging.info("Adding default connections for unconnected routers...")
        create_default_connections()

    #TCP connection simulation -- needs threading?
    for router in routers:
        router.start()

    # TODO: BGP simulation - in own module perhaps, so that code is clean yes
    # TODO: Routingtables - Some higher level one that stores all routers and their connections -> From there the actual one can be made


if __name__ == "__main__":
    main()
