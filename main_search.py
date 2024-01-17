import base64
import time
from pybloom_live import ScalableBloomFilter
from Client.Client_Search import Client_Search
from Client.password_related import decrypt_data
from Server.Server_Search import Server_Search

# 查找的关键字
key = 'Id'

# 读取密钥skey
with open('Client/document/password.txt', 'r') as file:
    skey = file.read()

#  加载KT数据为字典
kt = {}
with open("Client/document/KT.txt", 'r') as file:
    for line in file:
        data = line.split()  # 分割每行数据
        kt[data[0]] = base64.b85decode(data[1])

# 加载BF布隆过滤器
bf = ScalableBloomFilter.fromfile(open('Client/document/BF.bf', "rb"))

# 初始化update_dict（数据库数据）
update_dict = {}

# 从文件加载update字典并保存到update_dict
with open('Server/EDB.txt', 'r') as file:
    for line in file:
        data = line.split()
        update_dict[data[0]] = data[1:]  # 提取关键字和文档id并将数据存入字典

# base64解码字典的键值对为字节串
update_dict = {base64.b85decode(key): base64.b85decode(value[0]) for key, value in update_dict.items()}

# 查找关键字对应的搜索搜索凭证
st = Client_Search(key, kt)
if st == "":
    print("关键字错误")
    exit()

inds = []  # 初始化查找的文档索引

start_time = time.time()  # 记录开始时间
# 开始查找文档索引并保存到inds
inds = Server_Search(st, bf, update_dict)
end_time = time.time()  # 记录结束时间

# 初始化解密后的关键字/文档字典
dict_inds = {}
ind_ints = []       # 解密后的文档索引
# 将加密的文档索引一个一个解密并保存到ind_ints里
for ind in inds:
    ind_ints.append(int.from_bytes(decrypt_data(ind, skey), byteorder='big'))  # 解密

    dict_inds[key] = ind_ints
print('查找关键字：{0}，共找到：{1}个文档, 文档解密后为：{2}'.format(key, len(inds), ind_ints[1:]))  # 记录查找的时间
print('查找关键字：{0}，共找到：{1}个文档, 耗时：{2}s'.format(key, len(inds), end_time-start_time))  # 记录查找的时间
