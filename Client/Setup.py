import base64
import pickle
from Client.password_related import generate_symmetric_key
from pybloom_live import ScalableBloomFilter


def Setup(k):
    # 生成一个k位的随机密钥
    key = generate_symmetric_key(k)
    key = base64.b85encode(key).decode('utf-8')
    # 打开或创建一个文本文件（如果不存在的话）
    with open('Client/document/password.txt', 'w') as file:
        # 写入数据到文件
        file.write(key)

    # 创建一个空的关键字状态表KT
    kt = ""
    with open('Client/document/KT.txt', 'w') as file:
        # 写入数据到文件
        file.write(kt)

    # 创建一个空的布隆过滤器BF
    bf = ScalableBloomFilter()
    # 保存布隆过滤器到本地文件
    bf.tofile(open('Client/document/BF.bf', 'wb'))

    # 创建一个空的加密数据库EDB发送给服务器
    edb = ""
    return edb
