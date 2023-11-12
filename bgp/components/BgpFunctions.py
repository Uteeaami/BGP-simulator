import struct
from bgp.components.BgpPacket import *
import threading
import time
import struct
import binascii
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request


def BGP_FSM(self, parent):
    first = True
    queue = []
    recv_queue = []
    own_upd_queue = []
    index = 0

    id = parent.id
    BGPid = parent.BGPid
    holdtime = 7
    optparam = 0
    sendable = create_open(id, holdtime, BGPid, optparam)
    self.send(sendable)
    msg = self.recv(4096)
    # formatin pitäisi muuttua viestin koon mukaan, tällä hetkellä olettaa että open viestissä ei ole optparamia, eli vika tavu = 0
    format = "!4LHBBHHLB"

    msg = struct.unpack(format, msg)
    this_neighbor_AS = msg[7] # instanssin peer numero
    this_neighbor_addr = self.getpeername()[0] # osoiteadd_routing_table_entry

    parent.append_neighbor_ASS((this_neighbor_AS, this_neighbor_addr))
    
    # Create table entries for neighbors
    neighbor = parent.get_neighbor_router_by_AS(this_neighbor_AS)
    parent.add_neighbor_to_routing_table(neighbor)

    # neighbor = parent.get_neighbor_router_by_AS(this_neighbor_AS)
    # topology_table.add_route(parent.id, neighbor.id)

    parent.instances_n += 1
    receiver_thread = threading.Thread(target = receiver, args = (self, parent, recv_queue, ))
    receiver_thread.start()
    while True:

        if len(recv_queue) > 0:
            msgs = []
            msg = recv_queue[0]
            original = binascii.hexlify(msg)
            #print(original)
            msglen = int.from_bytes(msg[16:18], byteorder='big')
            while len(msg) > msglen:
                msgs.append(msg[:msglen])
                msg = msg[msglen:]
                msglen = int.from_bytes(msg[16:18], byteorder='big')

            if msglen == len(msg):
                msgs.append(msg)
            #print(original, (msgs))
            for message in msgs:
                if message[18] == 2:
                    handle_update(message, self, parent)
            del recv_queue [0]

        parent.lock.acquire()
        add = True
        count = 0
        for i in range(index, len(parent.update_queue)):
            update = parent.update_queue[i]
            for AS in update[1]:
                if AS == this_neighbor_AS:
                    add = False
            if add == True:
                update = create_propagate_update(self, parent, update)
                queue.append(update)
            count += 1
        index += count
        parent.lock.release()

        if len(queue) > 0:
            for q in queue:
                self.send(queue[0])
                del queue[0]

        sendable = create_keepalive()
        self.send(sendable)

        if parent.instances_n == parent.instances and first == True:
            queue += first_updates(self, parent, this_neighbor_AS)
            first = False

        time.sleep(holdtime/3)  # "A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval."


def receiver(self, parent, recv_queue):
    # viestien katoaminen voi johtua siitä että handle_update ottaa prion eik self.recv
    while True:
        msg = self.recv(4096)
        recv_queue.append(msg)


# https://stackoverflow.com/a/13294427
def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def handle_update(msg, self, parent):
    ORIGIN_t = 0b0100000000000001
    AS_PATH_t = 0b0100000000000010
    NEXT_HOP_t = 0b0100000000000011

    wd_len = int.from_bytes(msg[19:21], byteorder='big')
    attr_len = int.from_bytes(msg[21 + wd_len :23 + wd_len], byteorder='big')
    attr = msg[23 + wd_len : 23 + attr_len + wd_len]
    nlri = msg[23 + attr_len + wd_len : ]

    ORIGIN = 0
    NLRIS = []
    NEXT_HOP = 0
    total_len = len(attr)

    # atribuuttien händläys
    for octet_n in range(len(attr) - 4):
        if int.from_bytes(attr[octet_n : octet_n + 2], byteorder='big') == ORIGIN_t:
            ORIGIN = attr[octet_n + 3] # = 1, aina
            octet_n += 3
            if octet_n > total_len:
                break

        if int.from_bytes(attr[octet_n : octet_n + 2], byteorder='big') == AS_PATH_t:
            AS_n = int.from_bytes(attr[octet_n + 4 : octet_n + 5], byteorder='big')
            AS_PATH = ()

            for AS in (range(AS_n)):
                AS_PATH += struct.unpack('!H', attr[octet_n + 5 + (AS * 2) : octet_n + 5 + ((AS + 1) * 2)])

            octet_n += int.from_bytes(attr[octet_n + 2 : octet_n + 3], byteorder='big')

            if octet_n > total_len:
                break

        if int.from_bytes(attr[octet_n : octet_n + 2], byteorder='big') == NEXT_HOP_t:
            NH_len = int.from_bytes(attr[octet_n + 2 : octet_n + 3], byteorder='big')
            NEXT_HOP = attr[octet_n + 3 : octet_n + 3 + NH_len]
            NEXT_HOP = int.from_bytes(NEXT_HOP, byteorder='big')
            NEXT_HOP = int2ip(NEXT_HOP)
            octet_n += 8

            if octet_n > total_len:
                break

    # NLRI händläys
    nlri_len = len(nlri)

    for n in range(int(nlri_len / 5)):
        cidr_len = int.from_bytes(nlri[n*5 : 1 + n*5], byteorder='big')
        prefix = int.from_bytes(nlri[1 + n*5 : 7 + n*5], byteorder='big')
        prefix = int2ip(prefix)
        NLRIS.append((cidr_len, prefix))
    if parent.id == 10:
        print("AS", parent.id, "received update from:", self.getpeername()[0], "AS", AS_PATH[0], "AS PATH:", AS_PATH, "NEXT HOP:", NEXT_HOP, ":", " that advertise routes(s) to:", NLRIS)
    recv_update = [ORIGIN, AS_PATH, NEXT_HOP, NLRIS]
    parent.update_queue.append(recv_update)
    parent.add_entry_to_topology_table(AS_PATH, NEXT_HOP, NLRIS)

def create_propagate_update(self, parent, recv_update):
    ORIGIN = 1
    AS_PATH = (parent.id,) + recv_update[1]
    NEXT_HOP = parent.server
    NLRI = recv_update[3]
    sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, NLRI[0])
    return sendable

def first_updates(self, parent, this_neighbor_AS):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
    queue = []
    ORIGIN = 1
    NEXT_HOP = parent.server

    for AS in parent.neighbor_ASS:
        AS_PATH = []
        if AS[0] != this_neighbor_AS:
            AS_PATH.append(parent.id)
            prefix = AS[1]
            NLRI = ((AS[0], prefix))
            sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, NLRI)
            # EN TIIÄ TARRTEEKS TÄHÄN
            #parent.add_entry_to_topology_table(AS_PATH, NEXT_HOP, NLRI)
            queue.append(sendable)
            
    return queue