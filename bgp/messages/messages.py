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


# Better way to make custom params for OPEN messages would be
# to get it in byte-form from another function and just
# pass it through here.
(open(0, 0, 0, 200000000000))
#print (binascii.hexlify(open(255, 0, 1028, 0)))

# todo 1-4 messages


