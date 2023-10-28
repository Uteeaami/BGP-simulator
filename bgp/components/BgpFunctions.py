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
    msg = self.recv(1024)
    # formatin pitäisi muuttua viestin koon mukaan, tällä hetkellä olettaa että viestissä ei ole optparamia, eli vika tavu = 0
    format = "!4LHBBHHLB"
    msg = struct.unpack(format, msg)
    parent.append_neighbor_ASS(msg[7]) # tämä antaa routerille tiedon peeraavista reitittimistä -> tietorakenteessa kaikki routerin peerit
    this_neighbor_AS = msg[7]          # kun taas tämä on instanssin oma peeri
    parent.instances_n += 1
    receiver_thread = threading.Thread(target = receiver, args = (self, parent, ))
    receiver_thread.start()
    while True:
        if len(queue) > 0:
            for q in queue:
                print("sending:", binascii.hexlify(queue[0]))
                self.send(queue[0])
                del queue[0]
        sendable = create_keepalive()
        self.send(sendable)
        if parent.instances_n == parent.instances and first == True:
            #print("sending first updates")
            #print("I AM AS: ", id, "I HAVE", parent.instances_n, "CONNECTION(S)")
            queue = first_updates(self, parent, this_neighbor_AS)
            first = False
            # KORJAA
        time.sleep(holdtime/3)  # "A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval."

def receiver(self, parent):
    proper_updates = []
    msg2 = b''
    while True:
        dubl = False
        msg = self.recv(4096)
        if msg == msg2 and msg[18] != 4:
            #print("SAMMA HÄR")
            dubl = True
        msg2 = msg
        #print("receiving:", binascii.hexlify(msg[16:18]), len(msg), int.from_bytes(msg[16:18], byteorder='big'), binascii.hexlify(msg))
        msglen = int.from_bytes(msg[16:18], byteorder='big')
        if len(msg) > msglen:
            msg = msg[:msglen]
        if msg[18] == 2 and dubl == False and msg not in proper_updates:
            # TODO: handle updates here, unpack, append own AS to AS_PATH, NEXT_HOP = parent.server and send to peers
            proper_updates.append(msg)
            print(binascii.hexlify(msg))

def first_updates(self, parent, this_neighbor_AS):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
    queue = []
    ORIGIN = 1
    NEXT_HOP = parent.server
    # Each AS path segment is represented by a triple
    # <path segment type, path segment length, path segment value>.
    for AS in parent.neighbor_ASS:
        AS_PATH = []
        if AS != this_neighbor_AS:
            AS_PATH.append(parent.id)
            AS_PATH.append(AS)
            sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, 0)
            #print(sendable)
            queue.append(sendable)
            self.send(sendable)
            #print(AS_PATH, "AS_PATH to:", this_neighbor_AS)
    return queue