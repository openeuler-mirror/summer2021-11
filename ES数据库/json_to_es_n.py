#!/usr/bin/python
import threading
import queue
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import sys

# host_list = [
#     {"host":"10.58.7.190","port":9200},
#     {"host":"10.58.55.191","port":9200},
#     {"host":"10.58.55.192","port":9200},
# ]
#
host_list = [
    {"host": "0.0.0.0", "port": 9200},
]

# create a es clint obj
client = Elasticsearch(host_list)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "insert.json"), "r") as f:
    for line in f:
        actions = []
        actions.append(json.loads(line))
        try:
            for k, v in helpers.parallel_bulk(client=client, thread_count=1, actions=actions):
                # 这里的actions是插入es的数据，这个格式必须是列表的格式，列表的每个元素又必须是字典
                pass
        except Exception as e:
            sys.stderr(e)
