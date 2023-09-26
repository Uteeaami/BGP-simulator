import struct
import binascii


# function structure for receiving messages on AS could be something like this:
#   receive_msg():
#       this_is_first_message == True:     # pseudo
#           receive_open():
#
# different conditions for different messages as determined by the protocol and AS needs

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

    logging.info("MSG LENGTH:", msglen + 19)
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

def open(myAS, holdtime, BGPid, optparam):
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
        openmsg += optparamlen.to_bytes(1, byteorder='big')

    msglen = len(openmsg)
    
    #logging.info("msglen: ", msglen)
    #logging.info("no header: ", binascii.hexlify(openmsg))
    header = construct_header(msglen, 1)
    output = header + openmsg
    logging.info("openmsg bytes: ", output)
    logging.info("opemmsg hexed: ", binascii.hexlify(output))
    return output

# make open() like this
def update(wdroutes, PATHatbrs, NLRI):
    # NLRI, Network Layer Reachability Information is not encoded explicitly, but can be calculated as:
    # UPDATE message Length - 23 - Total Path Attributes Length - Withdrawn Routes Length
    if wdroutes != 0:
        updatemsg = octets_required(len(wdroutes)).to_bytes(2, byteorder='big')
        updatemsg += wdroutes
    else:
        length = 0
        updatemsg = length.to_bytes(2, byteorder='big')

    if PATHatbrs != 0:
        updatemsg += octets_required(len(PATHatbrs)).to_bytes(2, byteorder='big')
        updatemsg += PATHatbrs
    else:
        length = 0
        updatemsg += length.to_bytes(2, byteorder='big')

    if NLRI != 0:
        updatemsg += NLRI

    msglen = len(updatemsg)
    header = construct_header(msglen, 2)
    output = header + updatemsg
    logging.info("updatemsg bytes: ", output)
    logging.info("only_____header: ", binascii.hexlify(header))
    logging.info("updatemsg hexed: ", binascii.hexlify(output))

    output = updatemsg
    return output


asd = 0
optparam = asd.to_bytes(5, byteorder="big")
#open(1, 10, 0, optparam)
update(0,optparam,0)
#logging.info (binascii.hexlify(open(255, 0, 1028, 0)))

# todo 1-4 messages


