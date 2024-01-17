from Client.config import k


def Dsearch(st, edb):
    inds = []
    value = edb[st]
    while value != b' ':
        st = bytes(b1 ^ b2 for b1, b2 in zip(value, (st + b'\xff'*32)))[:k]
        rn = bytes(b1 ^ b2 for b1, b2 in zip(value, (st + b'\xff'*32)))[k:]
        value = edb[st]
        st = bytes(b1 ^ b2 for b1, b2 in zip(value, (rn + b'\xff'*32)))[:k]
        h = bytes(b1 ^ b2 for b1, b2 in zip(value, (rn + b'\xff'*32)))[k:]
        value = edb[h]
        ind = bytes(b1 ^ b2 for b1, b2 in zip(value, (h + b'\xff'*64)))[:2*k]
        rt = bytes(b1 ^ b2 for b1, b2 in zip(value, (h + b'\xff'*64)))[2*k:]
        inds.append(ind)
        while rt != b'\x00'*32:
            value = edb[rt]
            ind = bytes(b1 ^ b2 for b1, b2 in zip(value, (rt + b'\xff'*64)))[:2*k]
            rt = bytes(b1 ^ b2 for b1, b2 in zip(value, (rt + b'\xff'*64)))[2*k:]
            inds.append(ind)
        value = edb[st]
    return inds


def Server_Search(st, bf, edb):
    inds = []
    tags = Dsearch(st, edb)
    for tag in tags:
        if tag not in bf:
            ind = tag[k:]
            inds.append(ind)
    return inds
