import requests
import pandas as pd
import re
from ast import literal_eval

headers = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }
title, body, issue_id, issue_url, assignee, creator, comments, label, created_at, now_community = [], [], [], [], [], [], [], [], [], []

community_data = pd.read_csv('Raw_data/Openeuler-所有社区的信息.csv')
community_name = community_data['full_name']
for name in community_name:
    print('正在爬取仓库：' + name)
    url = 'https://gitee.com/api/v5/repos/' + str(
        name) + '/issues?access_token=54684bdeddb6825638d58fbd028816ee&state=all&sort=created&direction=asc&page=1&per_page=100'
    response = requests.get(url=url)
    pagenum = response.headers['total_page']
    for i in range(1, int(pagenum) + 1):
        print('正在爬取第' + str(i) + '页')
        url = 'https://gitee.com/api/v5/repos/' + str(
            name) + '/issues?access_token=54684bdeddb6825638d58fbd028816ee&state=all&sort=created&direction=asc&page=' + str(
            i) + '&per_page=100'
        response = requests.get(url=url)
        data = response.json()
        if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
            print('error: fail to request')
        for i in range(0, len(data)):
            issue = data[i]
            now_community.append(name)
            issue_id.append(issue['number'])
            title.append(issue['title'])
            body.append(issue['body'])
            issue_url.append(issue['html_url'])
            if issue['assignee'] == None:
                assignee.append('None')
            # elif len(issue['assignee']) > 1:
            #     assignee_temp = []
            #     for _ in issue['assignee']:
            #         assignee_temp.append(_['login'])
            #     assignee.append(assignee_temp)
            else:
                assignee.append(issue['assignee']['login'])
            creator.append(issue['user']['login'])
            comments.append(issue['comments'])
            created_at.append(issue['created_at'].replace('T', ' ').replace('+08:00', ''))
            label_temp = []
            if issue['labels'] == '[]':
                label.append('[]')
            else:
                for _ in issue['labels']:
                    label_temp.append(_['name'])
                label.append(label_temp)

oe_issue_list = pd.DataFrame(
    {
        'community_name': now_community,
        'title': title,
        'body': body,
        'issue_id': issue_id,
        'issue_url': issue_url,
        'assignee': assignee,
        'label': label,
        'creator': creator,
        'comments': comments,
        'created_at': created_at

    })
columns = ['community_name', 'issue_id', 'title', 'body', 'issue_url', 'assignee', 'label', 'creator', 'comments',
           'created_at']
oe_issue_list.to_csv('Openeuler_all_issue_data.csv', index=None, columns=columns)
print('csv已保存！')
