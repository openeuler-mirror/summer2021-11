# coding:utf8
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def set_data(inptfile):
    f = open(inptfile, 'r', encoding='UTF-8')
    print(f.readlines())


class ElasticObj:
    def __init__(self, index_name, index_type, ip):
        """
        :param index_name: 索引名称
        :param index_type: 索引类型
        """
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.es = Elasticsearch([ip])
        # 用户名密码状态
        # self.es = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    def create_index(self):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "full_name": {
                            'type': 'text'
                        },
                        "name": {
                            'type': 'text'
                        },
                        "forks_count": {
                            'type': 'int'
                        },
                        "stargazers_count": {
                            'type': 'int'
                        },
                        "watchers_count": {
                            'type': 'int'
                        },
                        "open_issues_count": {
                            'type': 'int'
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings, ignore=400)
            print(res)

    # 插入数据
    def insert_data(self, inputfile):
        f = open(inputfile, 'r', encoding='UTF-8')
        data = []
        for line in f.readlines():
            # 把末尾的'\n'删掉
            print(line.strip())
            # 存入list
            data.append(line.strip())
        f.close()

        ACTIONS = []
        i = 1
        bulk_num = 2000
        for list_line in data:
            # 去掉引号
            list_line = eval(list_line)
            # print(list_line)
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": i,  # _id 也可以默认生成，不赋值
                "_source": {
                    "full_name": list_line["full_name"],
                    "name": list_line["name"],
                    "forks_count": list_line["forks_count"],
                    "stargazers_count": list_line["stargazers_count"],
                    "watchers_count": list_line["forks_count"],
                    "open_issues_count": list_line["open_issues_count"]},

            }
            i += 1
            ACTIONS.append(action)
            # 批量处理
            if len(ACTIONS) == bulk_num:
                print('插入', i / bulk_num, '批数据')
                print(len(ACTIONS))
                success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
                del ACTIONS[0:len(ACTIONS)]
                print(success)

        if len(ACTIONS) > 0:
            success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
            del ACTIONS[0:len(ACTIONS)]
            print('Performed %d actions' % success)


if __name__ == '__main__':
    obj = ElasticObj("test", "en", ip="127.0.0.1")
    obj.create_index()
    obj.insert_data("../Data_Crawel/Community_Issue_Data/Raw_data/temp.json")
