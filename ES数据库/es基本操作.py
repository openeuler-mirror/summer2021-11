from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])
es.indices.delete(index='sig_info', ignore=[400, 404])
