"""
Basicaly some notes i took while in the bus to nla
Source port - 2 octets - Use default 197 0000 0000 1100 0101
Destination port - 2 octets - Use default 197 0000 0000 1100 0101
Sequence number - 4 octest - basically random identifier changes by every message
Acknowledgement number - 4 octets - sequence number +1
Data Offset - 4 bits - How many 32-bit (octets) are in data. Not needed? Default to 0's
Reserved - 6 bits - Sent as zero
Control Bits - 6 bits = [
    URG - 1bit - Not valid for this project: 0
    ACK - 1bit - Carries ACK message (has gotten SYN) before, can also send SYN, ACK
    PSH - 1bit - Not valid for this project: 0
    RST - 1bit - Error occurred on sender probably not valid, but if we have time why not
    SYN - 1bit - Request to Synchronize, first message
    Fin - 1bit - Sender requests connection to close
]
Window - 2 octets - Set all to 1's, (amount of data sender is willing to take) or 0's not really valid for this project
Checksum - 2 octets...yes.. will have to check how this is done :D
Urgent Pointer - 2 octets - Not valid, set all to 0's
Options - Variable - Not valid set to 0 or just leave it
Padding - Variable - 1 octet padding set to 0's
Data - Variable - Depends on the data offset, not that valid so probably 0 or not included

197/2 = 98,5 - 1
98/2 = 49 - 0
49/2 = 24,5 - 1
24/2 = 12 - 0
12/2 = 6 - 0
6/2 = 3 - 0
3/2 = 1,5 - 1
1/2 = 0,5 - 1

The flow:
    --> Establish TCP connection between two routers
    --> Router 1 creates IP packet with TCPSYNPacket
    --> Router 1 sends said IP packet
    --> Router 2 receives said IP packet with TCPSYNPacket

    --> Router 2 creates IP packet with TCPSYNACKPacket
    --> Router 2 sends said IP packet
    --> Router 1 receives said IP packet with TCPSYNACKPacket

    --> Router 1 creates IP packet with TCPACKPacket
    --> Router 1 sends said IP packet
    --> Router 2 receives said IP packet with TCPACKPacket
    --> Connection established BGP FSM is in starting point

Same with pseudo:
    establish_tcp_connection(router1, router2)
        create_ip_packet(SYN, router1, router2)
            create_tcp_packet(SYN, sequence_number, ack_number)
        send_ip_packet(packet, router1, router2)
            receive_ip_packet(packet, router2)

Problems are since the sequence and acknowledge nubmers change, how do we do that? Put it in the function?
"""

import struct
import random


def tcp_packet_build(type, acknowledgement_number):
    # Do or not to do?
    # binary_sequence_number = struct.pack('!L', sequence_number)
    # binary_sequence_number_str = ''.join(format(byte, '08b') for byte in binary_sequence_number)

    # binary_acknowledgement_number = struct.pack('!L', acknowledgement_number)
    # binary_acknowledgement_number_str = ''.join(format(byte, '08b') for byte in binary_acknowledgement_number)
    sequence_number = random.randint(0, 4294967295)

    type = tcp_type_check(type)
    packet = struct.pack('!2H2L4HB',
                         0xC5,
                         0xC5,
                         sequence_number,
                         acknowledgement_number,
                         type,
                         0x0000,
                         0x0000,
                         0x0000,
                         0x00)
    return packet


"""
ACK = 16
SYNACK = 18
SYN = 2
"""


def tcp_type_check(type):
    if (type == "ACK"):
        type = 0x10
    elif (type == "SYNACK"):
        type = 0x12
    elif (type == "SYN"):
        type = 0x02
    else:
        logging.info("TCP Control Bit invalid...")

    return type


def main():
    tcp_packet_build("ACK", 20100, 0)


if __name__ == "__main__":
    main()
