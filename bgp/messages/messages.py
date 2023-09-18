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

    print("MSG LENGTH:", msglen + 19)
    return output

def octets_required(paramlen):
    output = 0
    for x in range(paramlen):
        if x % 8 == 0:
            output += 1
    return output

def param_tobytes(param, octets):
    output = param.to_bytes(octets, byteorder='big')
    return output

def open(myAS, holdtime, BGPid, optparam):
    # https://datatracker.ietf.org/doc/html/rfc4271#section-4.2
    # Version always 4
    version = 4

    optparamlen = optparam.bit_length()
    octets = octets_required(optparamlen)
    print(octets)
    # remove B from format if no optparam
    format = '!BHHLB'
    #print(format)

    openmsg = struct.pack(format, version, myAS, holdtime, BGPid, octets)
    optparam = param_tobytes(optparam, octets)
    print("optparam: ", binascii.hexlify(optparam))

    openmsg += optparam
    msglen = len(openmsg)
    
    #print("msglen: ", msglen)
    #print("no header: ", binascii.hexlify(openmsg))
    header = construct_header(msglen, 1)
    output = header + openmsg
    print(binascii.hexlify(output))
    return output

def update(wdroutes, PATHatbrs, NLRI):
    # NLRI, Network Layer Reachability Information is not encoded explicitly, but can be calculated as:
    # UPDATE message Length - 23 - Total Path Attributes Length - Withdrawn Routes Length
    wdrouteslen = wdroutes.bit_length()
    PATHatbrslen = PATHatbrs.bit_length()
    octets1 = octets_required(wdrouteslen)
    octets2 = octets_required(PATHatbrslen)

    updatemsg = octets1.to_bytes(2, byteorder='big')
    updatemsg += param_tobytes(wdroutes, octets1)
    updatemsg += octets2.to_bytes(2, byteorder='big')
    updatemsg += param_tobytes(PATHatbrs, octets2)
    if NLRI != 0:
        updatemsg += NLRI.to_bytes(byteorder='big')
    print(updatemsg)

    msglen = len(updatemsg)
    header = construct_header(msglen, 2)
    output = header + updatemsg
    print(binascii.hexlify(header))
    print(binascii.hexlify(output))
    print(output)
    return output

# Better way to make custom params for OPEN messages would be
# to get it in byte-form from another function and just
# pass it through here.
#open(1, 1, 0, 0)
update(0, 0, 0)
#print (binascii.hexlify(open(255, 0, 1028, 0)))

# todo 1-4 messages


