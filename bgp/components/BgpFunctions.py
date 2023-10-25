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
        if msg[18] == 2: # 19. merkitsevin tavu = headerin määrittämä type. 2 = UPDATE
            print("receive update")
        if parent.instances_n == parent.instances and first == True:
            print("sending first updates")
            #first_update(self, parent, this_neighbor_AS)
            first = False

        time.sleep(holdtime/3)  # "A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval."

    def first_update(self, parent, this_neighbor_AS):
        attr_flag_octet = 0b01000000
        attr_flag_2octet = 0b01010000
        # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
        ORIGIN = 1
        NEXT_HOP = parent.server
        # taio logiikkaa AS_PATH
        AS_PATH_SEQMENTS = []
        # Each AS path segment is represented by a triple
        # <path segment type, path segment length, path segment value>.
        PATH_SEQMENT_TYPE = 2 # sequence, sequence on järjestetty sarja
        for AS in parent.neighbor_ASS:
            if AS != this_neighbor_AS:
                PATH_SEQMENT_VALUE = id.to_bytes(2, byteorder="big") #    The path segment value field contains one or more AS
                PATH_SEQMENT_VALUE += AS.to_bytes(2, byterorder="big")  #  numbers, each encoded as a 2-octet length field.
                PATH_SEQMENT_LENGTH = int(2).to_bytes(1, byterorder="big") # aspath AS n = 2
                AS_PATH_SEQMENTS.append((PATH_SEQMENT_TYPE, PATH_SEQMENT_LENGTH, PATH_SEQMENT_VALUE))


        sendable = create_update(0, 0, 0)