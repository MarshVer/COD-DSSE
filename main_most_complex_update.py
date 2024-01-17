import time
import base64
from pybloom_live import ScalableBloomFilter
from Client.config import k
from Client.password_related import encrypt_data
from Client.Update import Update

# 指定本地keywords-document-index的文件路径(可包含多个关键字)
document_dict_path = 'Client/most_complex_db/100.txt'
# 指定对文档的操作add/del
op = 'add'

# 读取密钥key
with open('Client/document/password.txt', 'r') as file:
    skey = file.read()

# 加载BF布隆过滤器
bf = ScalableBloomFilter.fromfile(open('Client/document/BF.bf', "rb"))

#  加载KT数据为字典
kt = {}
with open("Client/document/KT.txt", 'r') as file:
    for line in file:
        # 分割每行数据
        data = line.split()
        if data:
            kt[data[0]] = base64.b85decode(data[1])

# 从文件加载数据为字典
document_dic = {}
update = {}
tol_time = 0
with open(document_dict_path, 'r') as file:
    for line in file:
        encrypt_ind = []
        # 分割每行数据
        data = line.split()
        encrypt_ind.append(encrypt_data(int(data[1]).to_bytes(32, 'big'), skey))  # 加密

        # 记录开始时间
        start_time = time.time()
        # 更新关键字问文档索引
        update.update(Update(k, kt, bf, data[0], op, encrypt_ind))
        # 记录结束时间
        end_time = time.time()
        tol_time = tol_time + end_time - start_time

print("更新Enron全部关键字和文档的时间：", tol_time)

# 保存update
with open('Server/EDB.txt', 'a') as file:
    for key, value in update.items():
        # 将键值对格式化为字符串，并写入文件
        line = f"{base64.b85encode(key).decode('utf-8')}{' '}{base64.b85encode(value).decode('utf-8')}\n"
        file.write(line)
print("update保存成功")
