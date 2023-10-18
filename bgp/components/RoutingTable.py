
class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_connection(self, router_id, destination, interface):
        if router_id not in self.routing_table:
            self.routing_table[router_id] = []
        self.routing_table[router_id].append((destination, interface))

    def get_connections(self, router_id):
        return self.routing_table.get(router_id, [])
