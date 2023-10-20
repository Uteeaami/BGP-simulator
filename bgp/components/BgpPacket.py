import struct
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

    #logging.info("MSG LENGTH:", msglen + 19)
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

def create_update(wdroutes, PATHattr, NLRI):
    # NLRI, Network Layer Reachability Information is not encoded explicitly, but can be calculated as:
    # UPDATE message Length - 23 - Total Path Attributes Length - Withdrawn Routes Length
    if wdroutes != 0:
        updatemsg = octets_required(len(wdroutes)).to_bytes(2, byteorder='big')
        updatemsg += wdroutes
    else:
        length = 0
        updatemsg = length.to_bytes(2, byteorder='big')

    if PATHattr != 0:
        updatemsg += octets_required(len(PATHattr)).to_bytes(2, byteorder='big')
        updatemsg += PATHattr
    else:
        length = 0
        updatemsg += length.to_bytes(2, byteorder='big')

    if NLRI != 0:
        updatemsg += NLRI

    msglen = len(updatemsg)
    header = construct_header(msglen, 2)
    output = header + updatemsg
    return output

def create_keepalive():
    return construct_header(19, 4)

#asd = 0
#optparam = asd.to_bytes(5, byteorder="big")
#open(1, 10, 0, optparam)
#update(0,optparam,0)
#logging.info (binascii.hexlify(open(255, 0, 1028, 0)))
