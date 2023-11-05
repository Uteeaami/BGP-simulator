import heapq

class TopologyTable:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, current_router, neighbor_router):
        if current_router not in self.routing_table:
            self.routing_table[current_router] = []

        if neighbor_router not in self.routing_table:
            self.routing_table[neighbor_router] = []

        self.routing_table[current_router].append(neighbor_router)
        self.routing_table[neighbor_router].append(current_router)

    def get_neighbors(self, current_router):
        return self.routing_table.get(current_router, [])

    def find_shortest_paths(self, start_router):
        distances = {router: float('inf') for router in self.routing_table}
        distances[start_router] = 0
        previous_routers = {router: None for router in self.routing_table}

        queue = [(0, start_router)]

        while queue:
            current_distance, current_router = heapq.heappop(queue)

            for neighbor_router in self.get_neighbors(current_router):

                distance_to_neighbor = current_distance + 1
                
                if distance_to_neighbor < distances[neighbor_router]:
                    distances[neighbor_router] = distance_to_neighbor
                    previous_routers[neighbor_router] = current_router
                    heapq.heappush(queue, (distance_to_neighbor, neighbor_router))

        return distances, previous_routers


    def find_best_routes(self):
        best_routes = {}
        for router in self.routing_table:
            distances, previous_routers = self.find_shortest_paths(router)
            best_routes[router] = {
                "distances": distances,
                "previous_routers": previous_routers
            }

        return best_routes