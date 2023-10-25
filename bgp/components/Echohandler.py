from socketserver import BaseRequestHandler
import time
from bgp.components.BgpFunctions import *

from bgp.components.RouterStates import RouterStates


class Echohandler(BaseRequestHandler):
    def handle(self):
        self.server.parent.instances += 1
        #print(self.server.parent)
        self.state = RouterStates.CONNECT
        print(f'Connected: {self.client_address} to {self.server.parent}')
        print("sending first msg")
            #self.request.sendall(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here
        BGP_FSM(self.request,  self.server.parent)
        self.state = RouterStates.OPENSENT
            #if not msg:
                #print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                #break # exits handler, framework closes socket
        time.sleep(10)

            #self.wfile.write(msg)
            #self.wfile.flush()