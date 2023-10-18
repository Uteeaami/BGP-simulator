
class RoutingTable:
    def __init__(self):
        self.routing_table = {}

    def add_connection(self, router_id, router_ip, destination_ip):
        self.routing_table[router_id].append((router_ip, destination_ip))

    def get_connections(self, router_id):
        return self.routing_table.get(router_id, [])
