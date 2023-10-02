from bgp.components.RouterStates import RouterStates
from bgp.globals import *
import struct
import socket

class PacketReceiver:
    def __init__(self, router):
        self.router = router
    
    def receive_packet(self, packet):
        type = struct.unpack(TCP_IP_PACKET, packet)[6]
        if type == 6:
            return self.receive_tcp_packet(packet)
        else:
            return None
        
    def receive_tcp_packet(self, packet):
        tcp_type = struct.unpack(TCP_IP_PACKET, packet)[14]
        binary_sender_ip = struct.unpack(TCP_IP_PACKET, packet)[8]
        binary_receiver_ip = struct.unpack(TCP_IP_PACKET, packet)[9]

        sender_ip = socket.inet_ntoa(struct.pack("!I", binary_sender_ip))
        receiver_ip = socket.inet_ntoa(struct.pack("!I", binary_receiver_ip))
        receiver_router = self.router.get_router_by_ip(sender_ip)

        if tcp_type == 2:
            # print(f"Sending SYNACK from [{self.router.name}] to [{receiver_router.name}]")
            self.router.packet_sender.send_ip_packet(receiver_router, "SYNACK")
            if self.router in receiver_router.waiting_response:
                receiver_router.waiting_response.remove(self.router)
            return False

        elif tcp_type == 18:
            # print(f"Sending ACK from [{self.router.name}] to [{receiver_router.name}]")
            self.router.packet_sender.send_ip_packet(receiver_router, "ACK")
            if self.router in receiver_router.waiting_response:
                receiver_router.waiting_response.remove(self.router)
            return False
        
        elif tcp_type == 16:
            print(f"CONNECTION ESTABLISHED [{self.router.name}] - [{receiver_router.name}]\n")
            if self.router in receiver_router.waiting_response:
                receiver_router.waiting_response.remove(self.router)
            self.router.tcp_connections.append(receiver_router)
            return True
        else:
            print("wtf")
            return False
        
        return False


    