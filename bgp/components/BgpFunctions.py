import struct
from bgp.components.BgpPacket import *
import time
import struct
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request



def BGP_FSM(self, parent):
    first = True

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
    while True:
        #print("number of connections", parent, ":", parent.instances_n, parent.instances)
        sendable = create_keepalive()
        self.send(sendable)
        msg = self.recv(1024)
        if parent.instances_n == parent.instances and first == True:
            #print("sending first updates")
            #print("I AM AS: ", id, "I HAVE", parent.instances_n, "CONNECTION(S)")
            first_update(self, parent, this_neighbor_AS)
            first = False
            # KORJAA
        if msg[18] == 2: # 19. merkitsevin tavu = headerin määrittämä type. 2 = UPDATE
                print("I AM:", parent.id, "receive update")


        time.sleep(holdtime/3)  # "A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval."

def first_update(self, parent, this_neighbor_AS):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
    ORIGIN = 1
    NEXT_HOP = parent.server
    # taio logiikkaa AS_PATH
    # Each AS path segment is represented by a triple
    # <path segment type, path segment length, path segment value>.
    for AS in parent.neighbor_ASS:
        AS_PATH = []
        if AS != this_neighbor_AS:
            AS_PATH.append(parent.id)
            AS_PATH.append(AS)
            sendable = create_update(0, ORIGIN, AS_PATH, NEXT_HOP, 0)
            #print(sendable)
            self.send(sendable)
            print(AS_PATH, "!!!!!!!!!")