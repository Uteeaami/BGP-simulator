import logging
import time
from bgp.components.Router import Router
from bgp.simulation.TcpConnection import tcp_connection
from bgp.globals import *

logging.basicConfig(format='%(message)s',
                    encoding='utf-8', level=logging.DEBUG)

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

def create_default_connections():

    connections = [
        ("r1", "r2"),
        ("r1", "r3"),
        ("r2", "r4"),
    ]

    for src, dest in connections:
        src_router = next(router for router in routers if router.name == src)
        dest_router = next(router for router in routers if router.name == dest)
        src_router.add_connection(dest_router)
        dest_router.add_connection(src_router)


def main():

    create_default_connections()
    for router in routers:
        router.start()
    
    time.sleep(10)
    for router in routers:
        print(f"{router} has")
        for tcp in router.tcp_connections:
            print(tcp)


if __name__ == "__main__":
    main()