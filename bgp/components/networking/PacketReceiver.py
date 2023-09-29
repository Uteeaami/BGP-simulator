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
            self.receive_tcp_packet(packet)
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
            # print(f"SYN message received from [{sender_ip}]")
            # print(f"Sending SYNACK from [{receiver_ip}] to [{sender_ip}]")
            self.router.packet_sender.send_ip_packet(receiver_router, "SYNACK")
            self.router.waiting_response.append(receiver_router)
            if self.router in receiver_router.waiting_response:
                receiver_router.waiting_response.remove(self.router)
            return False

        elif tcp_type == 18:
            # print(f"SYNACK message received from [{sender_ip}]")
            # print(f"Sending ACK from [{receiver_ip}] to [{sender_ip}]")
            self.router.packet_sender.send_ip_packet(receiver_router, "ACK")
            if self.router in receiver_router.waiting_response:
                receiver_router.waiting_response.remove(self.router)
            self.router.state = RouterStates.ACTIVE
            return False
        
        elif tcp_type == 16:
            # print(f"CONNECTION ESTABLISHED [{receiver_ip}] - [{sender_ip}]\n")
            return True
        else:
            print("wtf")


    