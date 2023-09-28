import struct
import socket
from bgp.packets.TcpPacket import tcp_packet_build

"""
Options kept at zero
In order top to bottom:
Version & IHL           = 0x45 - version:4 | IHL min value: 5
DSCP & ECN              = 0x30 - DSCP: typeofservice value 48: network control | null, not valid for project
Total lenght            = 0x0000 - Not really valid for project, but might be!
Identification          = 0x0000 - ID field, not valid
Flags & fragment offset = 0x0000 - Flags not valid | fragmentation might be, if we decide to implement
TTL                     = 0x40 - 64sec, not really valid but TTL is a thing so good to keep it there
Protocol                = 0x06 - TCP
Header Checksum         = 0x0000 - We can implement this, so lets keep it open
Source & destination IP's 
"""
def ip_packet_build(source_ip, destination_ip, acknowledgement_number ,type):

    converted_source_ip = struct.unpack("!L", socket.inet_aton(source_ip) )[0]
    converted_destination_ip = struct.unpack("!L", socket.inet_aton(destination_ip) )[0]

    packet = struct.pack('!2B3H2BH2L',
                         0x45,
                         0x30,
                         0x0000,
                         0x0000,
                         0x0000,
                         0x40,
                         0x06,
                         0x0000,
                         converted_source_ip,
                         converted_destination_ip
                         )
    
    #Random generator for ack and sequence numbers? But these need to be remembered....
    #ACK == sequence_number + 1
    #Probably in receivers end -> decrypt packet -> get sequence -> add +1 -> make a new packet
    tcp_ip_packet = packet + tcp_packet_build(type, acknowledgement_number)

    return tcp_ip_packet


def main():
    packet = ip_packet_build("192.168.1.1", "192.168.2.1", 0, "SYNACK")
    logging.info(struct.unpack("!2B3H2BH2L2H2L4HB", packet))
    logging.info(packet)


if __name__ == "__main__":
    main()
