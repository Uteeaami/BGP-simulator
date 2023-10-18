import struct

# APUA seuraaviin --> miten saada parent paremmin luokalle

# olisi hienoa jos server ja clientti molemmat voisi käyttää samaa logiikkaa, en oo vielä varma toteutuksesta =(
# Clientti kutsuu funktiota muuttujalla sock, Server: self.request

def BGP_FSM(self):
    self.send(struct.pack("!13s", b"1st. BGP msg")) # implement proper BGP msg here
    #msg = self.recv(1024)

def BGP_DECODER(msg):
    return True