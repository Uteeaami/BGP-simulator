import time
from bgp.components.Router import Router
from ScriptRunner import run_startup_scripts
from GlobalText import *
import tomli

run_startup_scripts() # USE ONLY WITH LINUX SYSTEMS

with open("config.toml", mode="rb") as fp:
    config = tomli.load(fp)

real_address = config["real_address"]
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

connections = config["connections"]


def create_default_connections():
    for router in routers:
        add_server_address(router)

    for connect in connections:
        for router in routers:
            if router.name == connect[1]:
                server_addr = router.get_server()
                neighbor_router = router
        for router in routers:
            if router.name == connect[0]:
                router.add_client(real_address[0], server_addr)
                router.add_neighbour_router(neighbor_router)
                del real_address[0]

def create_manual_connection(router, neighbor):
    add_server_address(router)
    add_server_address(neighbor)
    router.add_client(real_address[0], neighbor.get_server())
    router.add_neighbour_router(neighbor)
    del real_address[0]

def add_server_address(router):
    if not router.server:
        router.set_server(real_address[0])
        del real_address[0]

def main():

# Print the introduction text
    print(bgp_ASCII_INTRO)
    print(bgp_usage)

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
            create_manual_connection(router1, router2)
        else:
            print("Invalid router name. Please try again.")

    # Create default connections if any of the routers doesn't have connections
    for router in routers:
        if not router.client:
            create_default_connections()
            break

    for router in routers:
        router.start()

    while True:
        input()
        for router in routers:
            router.topologytable.check_for_dupes()
            router.add_routing_table_entries()
            
        option = input("\n Print routingtable of router: ")
        for router in routers:
            if option == router.name:
                print(router.routingtable)
                
if __name__ == "__main__":
    main()
