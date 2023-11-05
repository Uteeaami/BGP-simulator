import struct
import socket
import binascii

def construct_header(msglen, msgtype):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.1
    # header MARKER field always set to all ones
    # 16 octets

    # msglen to mutate header LENGTH
    # min 19 max 4096, always adds header length (+19)
    # 2 octets

    # msgtype to mutate header TYPE
    # 1 OPEN, 2 UPDATE, 3 NOTIFICATION, 4 KEEPALIVE
    # 1 octet

    output = struct.pack('!4LHB',
                         0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff,
                         msglen + 19,
                         msgtype)

    return output

def octets_required(paramlen):
    output = 0
    for x in range(paramlen):
        if x % 2 == 0:
            output += 1
    return output

def param_tobytes(param, octets):
    output = param.to_bytes(octets, byteorder='big')
    return output

def create_open(myAS, holdtime, BGPid, optparam):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.2
    # Version always 4
    version = 4
    format = '!BHHL'
    openmsg = struct.pack(format, version, myAS, holdtime, BGPid)

    if optparam != 0:
        octets = octets_required(len(optparam))
        openmsg += octets.to_bytes(1, byteorder='big')
        openmsg += optparam
    else:
        length = 0
        openmsg += length.to_bytes(1, byteorder='big')

    msglen = len(openmsg)
    header = construct_header(msglen, 1)
    output = header + openmsg
    return output

# https://stackoverflow.com/a/13294427
def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]
# https://stackoverflow.com/a/13294427

def create_update(wdroutes, ORIGIN, AS_PATH, NEXT_HOP, NLRI):
    # oletuksia: updateja kutsutaan aina ja vain aina pathattribuuteilla VAIN yksi NLRI osoite, wdroutes kosmeettinen atm

    # NLRI, Network Layer Reachability Information is not encoded explicitly, but can be calculated as:
    # UPDATE message Length - 23 - Total Path Attributes Length - Withdrawn Routes Length
    # parameter types AS_PATH list, ORIGIN int, NEXT_HOP string, NLRI tuple
    if wdroutes != 0:
        updatemsg = octets_required(len(wdroutes)).to_bytes(2, byteorder='big')
        updatemsg += wdroutes
    else:
        length = 0
        updatemsg = length.to_bytes(2, byteorder='big')

    if AS_PATH == 0 and ORIGIN == 0 and NEXT_HOP == 0:
        length = 0
        updatemsg += length.to_bytes(2, byteorder='big')

    else: 

    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.3
    # https://www.ciscopress.com/articles/article.asp?p=2738462&seqNum=2
    # Each path attribute is a triple
    # <attribute type, attribute length, attribute value> of variable length.
        
        ORIGIN_t = 0b0100000000000001
        AS_PATH_t = 0b0100000000000010  
        NEXT_HOP_t = 0b0100000000000011
    
        attr = ORIGIN_t.to_bytes(2, byteorder = 'big')
        attr += int(1).to_bytes(1, byteorder = 'big') # ORIGIN length always 1
        attr += ORIGIN.to_bytes(1, byteorder = 'big') 

    # The path segment value field contains one or more AS numbers, 
    # each encoded as a 2-octet length field.
        path = b''
        length = 0
        for AS in AS_PATH:
            path += AS.to_bytes(2, byteorder = 'big')
            length += 1
        AS_PATH = int(2).to_bytes(1, byteorder = 'big') 
        AS_PATH += length.to_bytes(1, byteorder = 'big') 
        AS_PATH += path
        attr += AS_PATH_t.to_bytes(2, byteorder = 'big')
        attr += len(AS_PATH).to_bytes(1, byteorder = 'big') 
        attr += AS_PATH

        attr += NEXT_HOP_t.to_bytes(2, byteorder= 'big')
        attr += int(4).to_bytes(1, byteorder = 'big') # NEXT_HOP length always 4 octets (32bit IPv4)
        attr += ip2int(NEXT_HOP).to_bytes(4, byteorder = 'big')

        updatemsg += len(attr).to_bytes(2, byteorder = 'big')
        updatemsg += attr

    if NLRI != 0:
        length = NLRI[0].to_bytes(1, byteorder = 'big')
        prefix = ip2int(NLRI[1]).to_bytes(4, byteorder = 'big')
        updatemsg += length
        updatemsg += prefix

    msglen = len(updatemsg)
    header = construct_header(msglen, 2)
    output = header + updatemsg
    return output

def create_keepalive():
    return construct_header(0, 4)

print(ip2int("1.0.0.1"))