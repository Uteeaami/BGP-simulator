import heapq

class TopologyTable:
    def __init__(self):
        self.table = []

    def check_for_dupes(self):
        for entry in self.table:
            tmp = entry.get("DEST_AS")
            for second_entry in self.table:
                inner_tmp = second_entry.get("DEST_AS")
                if tmp[0] == inner_tmp[0]:
                    dist1 = entry.get("DIST")
                    dist2 = second_entry.get("DIST")
                    if len(dist1) < len(dist2):                      
                        self.table.remove(second_entry)

