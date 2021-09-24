import pandas as pd
import re

issue_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
issue_id = issue_data['issue_id']
issue_community_name = issue_data['community_name']
title = issue_data['title']
body = issue_data['body']


def text_porcess(text):
    print(text)
    text = re.sub('<!-- #请根据issue的类型(.*?)-->', '', text)
    text = re.sub('<!-- #请根据issue相关的版本(.*?)-->', '', text)

    text = re.sub('!\[输入图片说明\](.*?)', '', text)
    text = re.sub('https://(.*?) ', '', text)

    text = re.sub('报错(.*?) ', '', text)
    text = re.sub('\*\*环境情况\*\*\:(.*?)其它\:', '', text)
    text = re.sub('logs(.*?)', '', text)
    # text = re.sub('https://(.*?)', '', text)
    print('\n')
    print(text)
    return text


if __name__ == '__main__':
    index = 0
    text = []
    for i in range(11):
        temp_text = ''
        # print(i)
        temp_text += title[i]
        temp_text += ':' + body[i]
        temp_text = text_porcess(temp_text)
        print('\n')
        # print(temp_text)
