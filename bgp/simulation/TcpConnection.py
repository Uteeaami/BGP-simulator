from bgp.packets.IpPacket import ip_packet_build
from bgp.globals import *
import struct
import logging


def tcp_connection(router):
    for interface in router.interfaces:
        for neighbor in router.connections:
            for neighbor_interface in neighbor.interfaces:
                ip1 = interface.ip_address.split(".")
                ip2 = neighbor_interface.ip_address.split(".")
                if ip1[2] == ip2[3] and ip1[3] == ip2[2]:
                    establish_connection(
                        interface.ip_address, neighbor_interface.ip_address)
                    router.add_tcp_connection(neighbor)
                    neighbor.add_tcp_connection(router)


def establish_connection(sender_ip, receiver_ip):
    logging.info(f"Connecting interfaces [{sender_ip}] - [{receiver_ip}]")
    send_ip_packet(sender_ip, receiver_ip, 0, "SYN")


def send_ip_packet(sender_ip, receiver_ip, acknowledgement_number, packet_type):
    ip_packet = ip_packet_build(
        sender_ip, receiver_ip, acknowledgement_number, packet_type)
    receive_ip_packet(sender_ip, receiver_ip,
                      acknowledgement_number, ip_packet)


def receive_ip_packet(sender_ip, receiver_ip, acknowledgement_number, packet):
    tcp_type = struct.unpack(TCP_IP_PACKET, packet)[14]

    if tcp_type == 2:
        logging.info(f"SYN message received from [{sender_ip}]")
        logging.info(f"Sending SYNACK from [{receiver_ip}] to [{sender_ip}]")
        send_ip_packet(receiver_ip, sender_ip,
                       acknowledgement_number, "SYNACK")

    elif tcp_type == 18:
        logging.info(f"SYNACK message received from [{sender_ip}]")
        logging.info(f"Sending ACK from [{receiver_ip}] to [{sender_ip}]")
        send_ip_packet(receiver_ip, sender_ip, acknowledgement_number, "ACK")

    elif tcp_type == 16:
        logging.info(
            f"CONNECTION ESTABLISHED [{receiver_ip}] - [{sender_ip}]\n")
    else:
        logging.info("wtf")
