from pymongo import *
import json


class Json2Mongo(object):
    def __init__(self, db, table):
        self.host = 'localhost'
        self.port = 27017
        self.db = db
        self.table = table

    # 读取json文件
    def __open_file(self, file):
        self.file = open(file, 'r', encoding='utf-8')
        # 创建mongodb客户端
        self.client = MongoClient(self.host, self.port)
        # 创建数据库
        self.db = self.client[self.db]
        # 创建集合
        self.collection = self.db[self.table]

    # 关闭文件
    def __close_file(self):
        self.file.close()

    # 写入数据库
    def write_database(self, file):
        self.__open_file(file)

        # 转换为python对象
        data = json.load(self.file)

        try:
            self.collection.insert(data)
            print('写入成功')
        except Exception as e:
            print(e)
        finally:
            self.__close_file()


if __name__ == '__main__':
    j2m = Json2Mongo('fibre_db', '2019-4-15_2019-4-21')
    j2m.write_database('E:/python/Fibre_NLP/result/2019-4-15_2019-4-21/every_summary.json')