from bgp.packets.IpPacket import ip_packet_build

class PacketSender:
    def __init__(self, router):
        self.router = router


    def send_ip_packet(self, receiver_router, type):
        interfaces = self.router.get_matching_interfaces(receiver_router)
        ip_packet = ip_packet_build(interfaces[0][0], interfaces[0][1], 0, type)
        receiver_router.packet_queue.append(ip_packet)
        self.router.waiting_response.append(receiver_router)
