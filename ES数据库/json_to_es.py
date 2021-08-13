# -*- coding: UTF-8 -*-
from itertools import islice
import json
import sys
from elasticsearch import Elasticsearch, helpers
import threading

_index = 'indextest'  # 修改为索引名
_type = 'string'  # 修改为类型名
es_url = 'http://localhost:9200/'  # 修改为elasticsearch服务器
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.decode('utf-8').encode('gb2312')
es = Elasticsearch(es_url)
es.indices.create(index=_index, ignore=400)
chunk_len = 10
num = 0


def bulk_es(path):
    bulks = []
    print(path)
    f = open(path, 'r', encoding='UTF-8')
    chunk_len = []
    for line in f.readlines():
        # 把末尾的'\n'删掉
        # print(line.strip())
        # 存入list
        chunk_len.append(line.strip())
    f.close()
    try:
        for i in range(chunk_len):
            bulks.append({
                "_index": _index,
                "_type": _type,
                "_source": {
                    "full_name": chunk_len["full_name"],
                    "name": chunk_len["name"],
                    "forks_count": chunk_len["forks_count"],
                    "stargazers_count": chunk_len["stargazers_count"],
                    "watchers_count": chunk_len["forks_count"],
                    "open_issues_count": chunk_len["open_issues_count"]
                }

            })
            helpers.bulk(es, bulks)
    except:
        pass


path = '../Data_Crawel/Community_Issue_Data/Raw_data/temp.json'
bulk_es(path)

with open(sys.argv[0]) as f:
    while True:
        lines = list(islice(f, chunk_len))
        num = num + chunk_len
        sys.stdout.write('\r' + 'num:' + '%d' % num)
        sys.stdout.flush()
        bulk_es(lines)
        if not lines:
            print("\n")
            print("task has finished")
            break
