
import random


class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, prefix, next_hop, as_path, neighbor_as):
        self.routing_table[prefix] = {
            "next_hop": next_hop,
            "as_path": as_path,
            "origin": "i",
            "local_pref": random.randint(0,100),
            "med": 0,
            "route_type": 20,
            "neighbor_as": neighbor_as
        }

    def remove_route(self, prefix):
        if prefix in self.routing_table:
            del self.routing_table[prefix]

    def get_route(self, prefix):
        return self.routing_table.get(prefix)