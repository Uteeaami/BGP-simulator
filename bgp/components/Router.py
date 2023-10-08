import time
import random
import threading
from socketserver import ThreadingTCPServer, BaseRequestHandler
import socket
import time
import struct
from bgp.components.RouterStates import RouterStates

# olisi hienoa jos server ja clientti molemmat voisi käyttää samaa logiikkaa, en oo vielä varma toteutuksesta =(
# Clientti kutsuu funktiota muuttujalla sock, Server puolestaan self.request
def BGP_FSM(self):
    self.send(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here


def BGP_DECODER(msg):
    return True

class echohandler(BaseRequestHandler):
    def handle(self):
        self.state = RouterStates.CONNECT
        print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
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
            print(f'Received: {msg}')
            if BGP_DECODER(msg) != True: # input first msg received (OPEN), if not proper -> break
                print("Illegal BGP message!")
                print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                break
            self.state = RouterStates.OPENCONFIRM
            self.state = RouterStates.ESTABLISHED
            time.sleep(10)
            # OPEN ends here, UPDATE begins

            #self.wfile.write(msg)
            #self.wfile.flush()

class Client(threading.Thread):
    def __init___(self, id, bind_addr, target_addr):
        super().__init__()
        self.id = id
        self.bind_addr = bind_addr
        self.target_addr = target_addr
        self.state = "initialize here only"
        self.msg = "initialize here only"

    def set_id(self, id):
        self.id = id

    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

    def set_target_addr(self, target_addr):
        self.target_addr = target_addr

    def run(self):
        print("running client: ", self.id, self.bind_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.bind_addr)
        sock.connect(self.target_addr)
        while True:
            msg = sock.recv(1024)
            time.sleep(5)
            BGP_FSM(sock)

class Server(threading.Thread):
    def __init___(self):
        super().__init__()
        self.id = id
        self.bind_addr = bind_addr
        self.state = "initialize here only"
        self.msg = "initialize here only"

    def run(self):
        print("running server:", self.bind_addr)
        server_socket = ThreadingTCPServer((self.bind_addr,179), echohandler)
        server_socket.serve_forever()
        
    def set_bind_addr(self, bind_addr):
        self.bind_addr = bind_addr

    def set_state(self, state):
        self.state = state
    
    def get_state(self):
        return this.state
    
    def set_msg(self, msg):
        self.msg = msg
    
    def get_msg(self):
        return self.msg

class Router(threading.Thread):
    def __init__(self, name, id, AS):
        super().__init__()
        self.name = name
        self.AS = AS
        self.client = []
        self.server = "initialize here only"
        self.state = RouterStates.OFFLINE
        self.packet_sender_lock = threading.Lock()
        self.packet_receiver_lock = threading.Lock()

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
        ServerThread.start()
        time.sleep(3)
        #ServerThread.set_msg("asd")

        i = 0
        for cli in self.client:
            time.sleep(1)
            client_port = random.randint(1024, 65535)
            client_addr = (cli[0], client_port)
            server_addr = (cli[1], 179)
            ClientThread = Client()
            ClientThread.set_id(i)
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
