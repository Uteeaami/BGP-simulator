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
    this_neighbor_addr = self.getpeername()[0] # osoite
    parent.append_neighbor_ASS((this_neighbor_AS, this_neighbor_addr))
    parent.instances_n += 1
    receiver_thread = threading.Thread(target = receiver, args = (self, parent, ))
    receiver_thread.start()
    while True:
        
        if len(parent.update_queue) > 0:
            #rand = random.randint(0, 200000)
            #print("propagatin'", parent.id)
            parent.lock.acquire()
            send = True
            index = 0
            for update in parent.update_queue:
                for AS in update[1]:
                    if AS == this_neighbor_AS:
                        send = False
                if send == True:
                    sendable = create_propagate_update(self, parent, update)
                    queue.append(sendable)
                    del parent.update_queue[index]
                    index -= 1
                index += 1

            if send == False:
                parent.propagate_condition += 1
            if parent.propagate_condition == parent.instances:
                parent.update_queue = []
                parent.propagate_condition = 0

            #print("endin'", parent.id, rand)
            parent.lock.release()

        if len(queue) > 0:
            for q in queue:
                #print("sending:", binascii.hexlify(queue[0]))
                self.send(queue[0])
                del queue[0]
        sendable = create_keepalive()
        self.send(sendable)
        if parent.instances_n == parent.instances and first == True:
            #print("sending first updates")
            #print("I AM AS: ", id, "I HAVE", parent.instances_n, "CONNECTION(S)")
            queue += first_updates(self, parent, this_neighbor_AS)
            first = False
            # KORJAA
        time.sleep(holdtime/3)  # "A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval."

def receiver(self, parent):
    proper_updates = []
    msg2 = b''
    while True:
        #dubl = False
        msg = self.recv(4096)
        #if msg == msg2 and msg[18] != 4:
            #print("SAMMA HÄR")
            #dubl = True
        msg2 = msg
        #print("receiving:", binascii.hexlify(msg[16:18]), len(msg), int.from_bytes(msg[16:18], byteorder='big'), binascii.hexlify(msg))
        msglen = int.from_bytes(msg[16:18], byteorder='big')
        if len(msg) > msglen:
            msg = msg[:msglen]
        if msg[18] == 2: # and dubl == False and msg not in proper_updates:
            # TODO: handle updates here, unpack, append own AS to AS_PATH, NEXT_HOP = parent.server and send to peers
            #proper_updates.append(msg)
            #print(binascii.hexlify(msg))
            handle_update(msg, self, parent)

# https://stackoverflow.com/a/13294427
def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def handle_update(msg, self, parent):
    ORIGIN_t = 0b0100000000000001
    AS_PATH_t = 0b0100000000000010
    # AS_PATH_bigt = 0b0101000000000010 # käytettäisi jos path attrbuutin koko yli 255, oletus ettei
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
            AS_PATH_s = int.from_bytes(attr[octet_n + 3 : octet_n + 4], byteorder='big')
            # ei tarvita, oletus aina = 2 AS_SEQUENCE: ordered set of ASes a route in the UPDATE message has traversed
            AS_n = int.from_bytes(attr[octet_n + 4 : octet_n + 5], byteorder='big')
            AS_PATH = ()
            for AS in (range(AS_n)):
                AS_PATH += struct.unpack('!H', attr[octet_n + 5 + (AS * 2) : octet_n + 5 + ((AS + 1) * 2)])
                #AS_PATH += (int.from_bytes(attr[octet_n + 5 + (AS * 2) : octet_n + 5 + ((AS + 1) * 2)], byteorder = 'big'))
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
    for n in range(int(nlri_len / 5)): # oletus että len(cidr_len) + len(prefix) = 1 + 4 oktettia, ei välttämättä aina totta, mutta sattuu nyt olemaan
        cidr_len = int.from_bytes(nlri[n*5 : 1 + n*5], byteorder='big')
        # ei sinänsä tarvita, oletus että aina /32 = yksi osoite, ei range
        prefix = int.from_bytes(nlri[1 + n*5 : 7 + n*5], byteorder='big')
        prefix = int2ip(prefix)
        NLRIS.append((cidr_len, prefix))

    print("AS", parent.id, "received update from:", self.getpeername()[0], "AS", AS_PATH[0], "AS PATH:", AS_PATH, "NEXT HOP:", NEXT_HOP, ":", " that advertise routes(s) to:", NLRIS)
    recv_update = [ORIGIN, AS_PATH, NEXT_HOP, NLRIS]
    parent.update_queue.append(recv_update)

def create_propagate_update(self, parent, recv_update):
    ORIGIN = 1
    AS_PATH = (parent.id,) + recv_update[1]
    NEXT_HOP = parent.server
    NLRI = recv_update[3]
    #print("AS", parent.id, "propagating update from:", self.getpeername()[0], "AS", AS_PATH[1], "AS PATH:", AS_PATH, "NEXT HOP:", NEXT_HOP, ":", " that advertise routes(s) to:", NLRI)
    sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, NLRI[0])
    return sendable

def first_updates(self, parent, this_neighbor_AS):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
    queue = []
    ORIGIN = 1
    NEXT_HOP = parent.server
    cidr_len = 32
    # Each AS path segment is represented by a triple
    # <path segment type, path segment length, path segment value>.

    for AS in parent.neighbor_ASS:
        AS_PATH = []
        #print(AS[0])
        if AS[0] != this_neighbor_AS:
            AS_PATH.append(parent.id)
            prefix = AS[1]
            #NLRI = ((cidr_len, prefix))
            NLRI = ((AS[0], prefix))
            sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, NLRI)
            #print(sendable)
            queue.append(sendable)
            #self.send(sendable)
            #print(AS_PATH, "AS_PATH to:", this_neighbor_AS)
    return queue