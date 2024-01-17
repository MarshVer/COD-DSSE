import base64
import hashlib
import json
import secrets
import struct
from Client.password_related import generate_symmetric_key, pseudo_random_generator
from Client.config import k


def sha256_hash(input_bytes):
    # 创建一个 SHA-256 哈希对象
    sha256_hash_obj = hashlib.sha256()

    # 更新哈希对象
    sha256_hash_obj.update(input_bytes)

    # 获取十六进制表示的哈希值并转换为字节串
    hash_hex = sha256_hash_obj.hexdigest()
    hash_bytes = bytes.fromhex(hash_hex)

    return hash_bytes


def DUpdate(st, dic, ind):
    key = sha256_hash(st)
    if key not in dic:
        h = secrets.token_bytes(k)
        dic[key] = st + h
        dic[h] = bytes(b1 ^ b2 for b1, b2 in zip((ind + b'\x00'*32), (h + b'\xff'*64)))
    else:
        value = dic[key]
        h = value[k:]
        value = dic[h]
        msg = bytes(b1 ^ b2 for b1, b2 in zip(value, (h + b'\xff'*64)))
        rt = secrets.token_bytes(k)
        dic[h] = bytes(b1 ^ b2 for b1, b2 in zip((ind + rt), (h + b'\xff'*64)))
        dic[rt] = bytes(b1 ^ b2 for b1, b2 in zip(msg, (rt + b'\xff'*64)))
    return dic


def Update(k, kt, bf, w, op, inds):
    if op == 'del':
        for ind in inds:  # 遍历所有的文档索引
            tag = sha256_hash(w.encode('utf-8')) + ind  # 连接关键字的哈希值和文档索引
            bf.add(tag)  # 将tag插入布隆过滤器
        bf.tofile(open('Client/document/BF.bf', 'wb'))
        return {}
    else:
        update = {}  # 初始化空的更新字典
        if w not in kt:
            st = pseudo_random_generator(k, w)  # 利用k和w生成伪随机数并转化为bytes
            kt[w] = st  # 将w的搜索凭证存入kt
            update[st] = b' '
        else:
            st = kt[w]  # 查询关键字w的搜索凭证
        for ind in inds:  # 遍历所有的文档索引
            tag = sha256_hash(w.encode('utf-8')) + ind  # 连接关键字的哈希值和文档索引
            update = DUpdate(st, update, tag)
        value = update[sha256_hash(st)]
        rn = secrets.token_bytes(k)
        stn = secrets.token_bytes(k)
        update[sha256_hash(st)] = bytes(b1 ^ b2 for b1, b2 in zip(value, (rn + b'\xff'*32)))
        update[stn] = bytes(b1 ^ b2 for b1, b2 in zip((sha256_hash(st) + rn), (stn + b'\xff'*32)))
        kt[w] = stn
        # 将字典写入文件
        with open('Client/document/KT.txt', 'w', encoding="utf-8") as file:
            for key, value in kt.items():
                # 将键值对格式化为字符串，并写入文件
                line = f"{key}{' '}{base64.b85encode(value).decode('utf-8')}\n"
                file.write(line)
        return update
