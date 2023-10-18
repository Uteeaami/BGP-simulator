import struct
from bgp.components.BgpPacket import *
import time
import struct
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request

def BGP_FSM(self, parent):
    id = parent.id
    holdtime = 7
    BGPid = parent.BGPid
    optparam = 0
    sendable = create_open(id, holdtime, BGPid, optparam)
    self.send(sendable) # implement proper BGP msg here
    msg = self.recv(1024)
    print(msg)
    format = "!4LHBBHHLB"
    msg = struct.unpack(format, msg)
    parent.append_neighbor_ASS(msg[7])
    while True:
        sendable = create_keepalive()
        self.send(sendable)
        msg = self.recv(1024)
        # A reasonable maximum time between KEEPALIVE messages would be one third of the Hold Time interval.
        time.sleep(holdtime/3)

    def update():
        print()

def BGP_DECODER(msg):
    return True