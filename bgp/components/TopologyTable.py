
# class TopologyTable:
#     def __init__(self):
#         self.table = []

#     def dijkstra(self, graph, start):
#         distances = {node: float('infinity') for node in graph}
#         distances[start] = 0

#         priority_queue = [(0, start)]

#         while priority_queue:
#             current_distance, current_vertex = heapq.heappop(priority_queue)

#             if current_distance > distances[current_vertex]:
#                 continue

#             try:
#                 for neighbor, weight in graph[str(current_vertex)].items():  # Convert to string
#                     distance = current_distance + weight

#                     if distance < distances[neighbor]:
#                         distances[neighbor] = distance
#                         heapq.heappush(priority_queue, (distance, neighbor))
#             except KeyError as e:
#                 print(f"KeyError: {e}")
#                 print("graph:", graph)
#                 print("current_vertex:", current_vertex)
#                 print("distances:", distances)
#                 print("priority_queue:", priority_queue)

#         return distances

import heapq

class TopologyTable:
    def __init__(self):
        self.table = {}

    def add_to_table(self, key, values):
        if key not in self.table:
            self.table[key] = [values]
        else:
            # If key already exists, append the new values to the existing list
            self.table[key].append(values)

    def add_router(self, router):
        # Add a router to the table with an empty list as its value
        if router not in self.table:
            self.table[router] = []

    def dijkstra_shortest_path(self, start_router):
        distances = {router: float('infinity') for router in self.table}
        distances[start_router] = 0
     
        previous_routers = {router: None for router in self.table}

        priority_queue = [(0, start_router, [])]

        while priority_queue:
            current_distance, current_router, current_path = heapq.heappop(priority_queue)

            if current_distance > distances[current_router]:
                continue

            for next_distance in self.table[current_router]:
                distance = current_distance + len(next_distance)
                next_router = next_distance[-1]
                next_path = current_path + [next_router]  # Append next_router to the current_path

                if distance < distances[next_router]:
                    distances[next_router] = distance
                    heapq.heappush(priority_queue, (distance, next_router, next_path))

        return distances


def main():

    table = TopologyTable()
    mock_data = [
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 5, 6), 'DEST_AS': (8, '10.0.5.8'), 'PATH': (3, 5, 6)},
        {'NEXT_HOP': '10.0.5.4', 'DIST': (2,), 'DEST_AS': (4, '10.0.5.5'), 'PATH': (2,)},
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 5), 'DEST_AS': (6, '10.0.5.6'), 'PATH': (3, 5)},
        {'NEXT_HOP': '10.0.5.4', 'DIST': (2, 4), 'DEST_AS': (9, '10.0.5.18'), 'PATH': (2, 4)},
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 6, 5), 'DEST_AS': (10, '10.0.5.19'), 'PATH': (3, 6, 5)},
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3,), 'DEST_AS': (5, '10.0.5.1'), 'PATH': (3,)},
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3,), 'DEST_AS': (6, '10.0.5.6'), 'PATH': (3,)},
        {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 6), 'DEST_AS': (8, '10.0.5.8'), 'PATH': (3, 6)}
        ]

    for data in mock_data:
        key = data['DEST_AS'][0]
        values = data['DIST']
        table.add_to_table(key, values)

    for key, values in table.table.items():
        print(f"key {key} values {values}")

    start_router = 1
    table.add_router(start_router)
    shortest_paths = table.dijkstra_shortest_path(start_router)

    print(shortest_paths)
    # for destination, result in shortest_paths.items():
    #     distance = result  # The distance is stored directly
    #     path = distance[1]  # The path is stored in the third element of the tuple
    #     print(f"Best path from router {start_router} to router {destination} is through {', '.join(map(str, path))}")

if __name__ == "__main__":
    main()
