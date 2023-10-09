import time
import random
import threading
from socketserver import ThreadingTCPServer, BaseRequestHandler
import socket
import time
import struct
from bgp.components.RouterStates import RouterStates


# APUA seuraaviin --> miten saada parent paremmin luokalle

# olisi hienoa jos server ja clientti molemmat voisi käyttää samaa logiikkaa, en oo vielä varma toteutuksesta =(
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request
def BGP_FSM(self):
    self.send(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here
    #msg = self.recv(1024)

def BGP_DECODER(msg):
    return True


class Router(threading.Thread):
    def __init__(self, name, id, AS):
        super().__init__()
        self.lock = threading.Lock()
        self.name = name
        self.id = id
        self.AS = AS
        self.client = []
        self.server = "initialize here only"
        self.state = RouterStates.OFFLINE

    def __str__(self):
        return f"Router {self.name}"

    def add_client(self, client_addr, server_addr):
        self.client.append((client_addr, server_addr))
    
    def set_server(self, server_addr):
        self.server = server_addr

    def get_server(self):
        return self.server

        # one bgp fsm per connection -> selvitä miten toteuttaa fiksusti tilakoneet serverin threadatussa tcp
    # handlerissä. Jos tilakone lähtisisi päälle pelkästä server luokasta olisi tilakoneita vain yksi per palvelin

    def run(self):
        if len(self.client) > 0:
            print("client connections:", self.name, self.client)
        print("server:", self.name, self.server)
        time.sleep(1)

        ServerThread = Server()
        ServerThread.set_bind_addr(self.server)
        ServerThread.set_parent(self)
        ServerThread.start()
        time.sleep(1)
        #ServerThread.set_msg("asd")

        i = 1
        for cli in self.client:
            time.sleep(1)
            client_port = random.randint(1024, 65535)
            client_addr = (cli[0], client_port)
            server_addr = (cli[1], 179)
            ClientThread = Client()
            ClientThread.set_parent(self)
            ClientThread.set_bind_addr(client_addr)
            ClientThread.set_target_addr(server_addr)
            ClientThread.start()
            i += 1 

        while True:
            time.sleep(random.randint(15,20))
            
            #print(self.waiting_response)
            #print("Active", self.name)
            #print("connections", self.tcp_connections)
            #break

class Server(threading.Thread):
    def __init___(self):
        self.parent = parent
        self.bind_addr = bind_addr

    def run(self):
        print("running server:", self.bind_addr, self.parent.AS)
        handler = echohandler
        server_socket = ThreadingTCPServer((self.bind_addr,179), handler)
        server_socket.parent = self.parent
        server_socket.serve_forever()
    
    # huono tapa tehdä, olio-ohjelmoinnin jatkokurssista 1
    def set_parent(self, parent):
        self.parent = parent

    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

class echohandler(BaseRequestHandler):
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

class Client(threading.Thread):
    def __init___(self, id, bind_addr, target_addr):
        self.parent = parent
        self.bind_addr = bind_addr
        self.target_addr = target_addr

    def set_parent(self, parent):
        self.parent = parent

    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

    def set_target_addr(self, target_addr):
        self.target_addr = target_addr

    def run(self):
        print("running client on", self.parent, self.bind_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.bind_addr)
        sock.connect(self.target_addr)
        while True:
            msg = sock.recv(1024)
            time.sleep(5)
            BGP_FSM(sock)    
