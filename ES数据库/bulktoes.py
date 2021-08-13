import json
import os

current_path = os.path.dirname(__file__)
new_jsonfile = open(current_path + '/bulk_singer.json', 'w', encoding='UTF-8')
# w打开一个文件只用于写入
# 如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除
# 如果该文件不存在，创建新文件

with open('sig.json', 'r', encoding='utf8')as fp:
    json_data = json.load(fp)
    # json_data是list
    # json_data[i]是dict
    id_num = 1
    for i in range(0, len(json_data)):
        # 添加index行
        new_data = {}
        new_data['index'] = {}
        new_data['index']['_index'] = "all_singer"
        new_data['index']['_id'] = str(id_num)
        id_num = id_num + 1
        temp = json.dumps(new_data).encode("utf-8").decode('unicode_escape')
        new_jsonfile.write(temp)
        new_jsonfile.write('\n')
        # 原json对象处理为1行
        old_data = {}
        old_data['sig_name'] = json_data[i]['sig_name']
        old_data['sig_repositories'] = json_data[i]['sig_repositories']
        old_data['sig_maintainers'] = json_data[i]['sig_maintainers']
        # old_data['singer_brief'] = json_data[i]['singer_brief']
        # old_data['singer_album'] = json_data[i]['singer_album']
        # old_data['singer_group'] = json_data[i]['singer_group']
        temp = json.dumps(old_data).encode("utf-8").decode('unicode_escape')
        new_jsonfile.write(temp)
        new_jsonfile.write('\n')

new_jsonfile.close()
