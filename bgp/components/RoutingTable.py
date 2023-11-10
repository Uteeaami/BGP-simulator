import random


class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, prefix, next_hop, neighbor_as, distance, path):
        if prefix not in self.routing_table:
            self.routing_table[prefix] = []

        self.routing_table[prefix].append({
            "next_hop": next_hop,
            "as_path": 16386,
            "origin": "e",
            "local_pref": random.randint(0, 100),
            "med": 0,
            "route_type": 20,
            "neighbor_as": neighbor_as,
            "distance": distance,
            "best_route": path
        })

    def get_route(self, prefix):
        return self.routing_table.get(prefix)
    
    def __str__(self):
        table_str = "BGP Routing Table\n"
        table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15}\n".format(
            "Network", "Next Hop", "AS Path", "Origin", "Local Pref", "MED", "Neighbor AS", "Distance", "Best Route"
        )
        
        for prefix, routes in self.routing_table.items():
            for route in routes:
                # Convert the 'path' list to a string by joining its elements
                path_str = " -> ".join(map(str, route["best_route"]))
                table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15}\n".format(
                    prefix,
                    route["next_hop"],
                    route["as_path"],
                    route["origin"],
                    route["local_pref"],
                    route["med"],
                    route["neighbor_as"],
                    route["distance"],
                    path_str
                )

        return table_str
