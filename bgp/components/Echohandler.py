from socketserver import BaseRequestHandler
import time
from bgp.components.Router import BGP_DECODER, BGP_FSM

from bgp.components.RouterStates import RouterStates


class Echohandler(BaseRequestHandler):
    def handle(self):
        #print(self.server.parent)
        self.state = RouterStates.CONNECT
        print(f'Connected: {self.client_address} to {self.server.parent}')
        while True:
            print("sending first msg")
            #self.request.sendall(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here
            BGP_FSM(self.request)
            self.state = RouterStates.OPENSENT
            msg = self.request.recv(1024).strip()
            #print("msg received")
            #if not msg:
                #print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                #break # exits handler, framework closes socket
            #print(f'Received: {msg}')
            if BGP_DECODER(msg) != True: # input first msg received (OPEN), if not proper -> break
                print("Illegal BGP message!")
                print(f'Disconnected: {self.client_address}')
                break
            self.state = RouterStates.OPENCONFIRM
            self.state = RouterStates.ESTABLISHED
            #print(self)
            time.sleep(10)
            # OPEN päättyy, UPDATE alkaa. Ei logiikkaa vielä --> oletus että jos vastaanottaa viestin, se on ok.
            # UPDATE luettu --> tarvitaan keino/tietorakenne/jotain välittää sen sisältö parentille (Router), jotta voidaan tehdä reititysvalintoja.

            #self.wfile.write(msg)
            #self.wfile.flush()