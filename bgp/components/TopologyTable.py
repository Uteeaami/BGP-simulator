import heapq

class TopologyTable:
    def __init__(self):
        self.table = []

    # def dijkstra(self, graph, start):
    #     distances = {node: float('infinity') for node in graph}
    #     distances[start] = 0

    #     priority_queue = [(0, start)]

    #     while priority_queue:
    #         current_distance, current_vertex = heapq.heappop(priority_queue)

    #         if current_distance > distances[current_vertex]:
    #             continue

    #         try:
    #             for neighbor, weight in graph[str(current_vertex)].items():  # Convert to string
    #                 distance = current_distance + weight

    #                 if distance < distances[neighbor]:
    #                     distances[neighbor] = distance
    #                     heapq.heappush(priority_queue, (distance, neighbor))
    #         except KeyError as e:
    #             print(f"KeyError: {e}")
    #             print("graph:", graph)
    #             print("current_vertex:", current_vertex)
    #             print("distances:", distances)
    #             print("priority_queue:", priority_queue)

    #     return distances

# import heapq

# class TopologyTable:
#     def __init__(self):
#         self.table = {}

#     def add_to_table(self, data):
#         for entry in data:
#             dest_as = entry['DEST_AS'][0]
#             dist = entry['DIST']

#             if dest_as not in self.table:
#                 self.table[dest_as] = []

#             # Only add dist to the values if it's not already present
#             if dist not in self.table[dest_as]:
#                 heapq.heappush(self.table[dest_as], dist)

#     def calculate_best_routes(self):
#         for key, values in self.table.items():
#             min_length = float('inf')

#             # Find the minimum length for the current destination
#             for dist_tuple in values:
#                 min_length = min(min_length, len(dist_tuple))

#             # Remove values longer than the minimum length
#             self.table[key] = [dist_tuple for dist_tuple in values if len(dist_tuple) == min_length]

#     def improve_routes(self):
#         for dest_as, values in self.table.items():
#             for i, dist_tuple in enumerate(values):
#                 for j in range(len(dist_tuple) - 1):
#                     # Check if there is a shorter route by combining segments
#                     combined_route = dist_tuple[:j+1] + dist_tuple[j+2:]
#                     if combined_route not in values:
#                         # Remove the longer route and add the combined route
#                         values.append(combined_route)
#                         break

#     def display_table(self):
#         for key, values in self.table.items():
#             print(f"Key {key}, Values {values}")

# def main():
#     table = TopologyTable()
#     mock_data = [
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 5, 6), 'DEST_AS': (8, '10.0.5.8'), 'PATH': (3, 5, 6)},
#         {'NEXT_HOP': '10.0.5.4', 'DIST': (2,), 'DEST_AS': (4, '10.0.5.5'), 'PATH': (2,)},
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 5), 'DEST_AS': (6, '10.0.5.6'), 'PATH': (3, 5)},
#         {'NEXT_HOP': '10.0.5.4', 'DIST': (2, 4), 'DEST_AS': (9, '10.0.5.18'), 'PATH': (2, 4)},
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 6, 5), 'DEST_AS': (10, '10.0.5.19'), 'PATH': (3, 6, 5)},
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3,), 'DEST_AS': (5, '10.0.5.1'), 'PATH': (3,)},
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3,), 'DEST_AS': (6, '10.0.5.6'), 'PATH': (3,)},
#         {'NEXT_HOP': '10.0.5.0', 'DIST': (3, 6), 'DEST_AS': (8, '10.0.5.8'), 'PATH': (3, 6)}
#     ]

#     table.add_to_table(mock_data)
#     print("Original Table:")
#     table.display_table()

#     table.calculate_best_routes()
#     print("\nTable after calculating best routes:")
#     table.display_table()

#     table.improve_routes()
#     print("\nTable after improving routes:")
#     table.display_table()

# if __name__ == "__main__":
#     main()





