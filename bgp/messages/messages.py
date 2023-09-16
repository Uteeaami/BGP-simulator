import struct


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


# todo 1-4 messages