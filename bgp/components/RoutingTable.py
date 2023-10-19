import random


class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, prefix, next_hop, as_path, neighbor_as):
        if prefix not in self.routing_table:
            self.routing_table[prefix] = []

        self.routing_table[prefix].append({
            "next_hop": next_hop,
            "as_path": as_path,
            "origin": "i",
            "local_pref": random.randint(0, 100),
            "med": 0,
            "route_type": 20,
            "neighbor_as": neighbor_as
        })

    def get_route(self, prefix):
        return self.routing_table.get(prefix)
    
    def __str__(self):
        table_str = "BGP Routing Table\n"
        table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15}\n".format(
            "Network", "Next Hop", "AS Path", "Origin", "Local Pref", "MED", "Neighbor AS"
        )
        
        for prefix, routes in self.routing_table.items():
            for route in routes:
                table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15}\n".format(
                    prefix,
                    route["next_hop"],
                    route["as_path"],
                    route["origin"],
                    route["local_pref"],
                    route["med"],
                    route["neighbor_as"]
                )

        return table_str