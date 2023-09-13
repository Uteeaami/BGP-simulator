import threading
from bgp.components.Router import Router
from bgp.components.Router import router_task
from bgp.components.Interface import Interface

"""
Routers have n interfaces that are the independent "connections?" between the routers
The creation of the interface and routers needs to be automated since the simulator is customizeable.
For example the IP_addresses, interface names etc.. need to be randomized.

"""

def main():
    interface1_2 = Interface("Interface 1.2", "10.0.1.2", "AS1")
    interface1_3 = Interface("Interface 1.3", "10.0.1.3", "AS1")
    interface2_1 = Interface("Interface 2.1", "10.0.2.1", "AS2")
    interface2_4 = Interface("Interface 2.4", "10.0.2.4", "AS2")
    interface3_1 = Interface("Interface 3.1", "10.0.3.1", "AS3")
    interface3_4 = Interface("Interface 3.4", "10.0.3.4", "AS3")
    interface4_2 = Interface("Interface 4.2", "10.0.4.2", "AS4")
    interface4_3 = Interface("Interface 4.3", "10.0.4.3", "AS4")
    interface4_5 = Interface("Interface 4.4", "10.0.4.5", "AS4")
    interface5_4 = Interface("Interface 4.5", "10.0.5.4", "AS5")

    # Create 5 routers
    router1 = Router("Router 1")
    router2 = Router("Router 2")
    router3 = Router("Router 3")
    router4 = Router("Router 4")
    router5 = Router("Router 5")

    # Add interfaces to routers
    router1.add_interface(interface1_2)
    router1.add_interface(interface1_3)
    router2.add_interface(interface2_1)
    router2.add_interface(interface2_4)
    router3.add_interface(interface3_1)
    router3.add_interface(interface3_4)
    router4.add_interface(interface4_2)
    router4.add_interface(interface4_3)
    router4.add_interface(interface4_5)
    router5.add_interface(interface5_4)

    # Connect routers
    router1.add_connection(router2)
    router1.add_connection(router3)
    router2.add_connection(router4)
    router3.add_connection(router4)
    router4.add_connection(router5)

    # Create threads for each router
    router_threads = [
        threading.Thread(target=router_task, args=(router1,)),
        threading.Thread(target=router_task, args=(router2,)),
        threading.Thread(target=router_task, args=(router3,)),
        threading.Thread(target=router_task, args=(router4,)),
        threading.Thread(target=router_task, args=(router5,))
    ]

    router1.print_interfaces()
    router2.print_interfaces()
    router3.print_interfaces()
    router4.print_interfaces()
    router5.print_interfaces()

    router1.print_connections()
    router2.print_connections()
    router3.print_connections()
    router4.print_connections()
    router5.print_connections()

    # Start the router threads
    for thread in router_threads:
        thread.start()

    for thread in router_threads:
        thread.join()


if __name__ == "__main__":
    main()