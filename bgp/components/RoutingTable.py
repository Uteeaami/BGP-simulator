import random


class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, prefix, next_hop, destination_as, distance, path):
        if prefix not in self.routing_table:
            prefix = prefix + "/32"
            self.routing_table[prefix] = []

        self.routing_table[prefix].append({
            "next_hop": next_hop,
            "as_path": 16386,
            "origin": "e",
            "local_pref": random.randint(0, 100),
            "med": 0,
            "route_type": 20,
            "destination_as": destination_as,
            "distance": distance,
            "best_route": path
        })

    def get_route(self, prefix):
        return self.routing_table.get(prefix)
    
    def __str__(self):
        table_str = "BGP Routing Table\n"
        table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15}\n".format(
            "Network", "Next Hop", "AS Path", "Origin", "Local Pref", "MED", "Destination AS", "Distance", "Best Route"
        )
        
        for prefix, routes in self.routing_table.items():
            for route in routes:
                
                # Convert the 'path' list to a string by joining its elements, adding neighdbors it's just an int so that is why we check
                best_route = route["best_route"]
                if isinstance(best_route, int):
                    path_str = str(best_route)
                else:
                    path_str = " -> ".join(map(str, best_route))

                table_str += "{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<15}\n".format(
                    prefix,
                    route["next_hop"],
                    route["as_path"],
                    route["origin"],
                    route["local_pref"],
                    route["med"],
                    route["destination_as"],
                    route["distance"],
                    path_str
                )

        return table_str
