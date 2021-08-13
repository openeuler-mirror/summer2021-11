import requests
import pandas as pd
import re
from ast import literal_eval

headers = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }


def get_allch():
    url = 'https://gitee.com/api/v5/orgs/src-openEuler/repos?access_token=54684bdeddb6825638d58fbd028816ee&type=all&page=1&per_page=100'
    name, full_name, description, forks_count, stargazers_count, watchers_count, open_issues_count = [], [], [], [], [], [], []
    response = requests.get(url=url)
    pagenum = response.headers['total_page']
    for i in range(1, int(pagenum) + 1):
        url = 'https://gitee.com/api/v5/orgs/src-openeuler/repos?access_token=54684bdeddb6825638d58fbd028816ee&type=all&page=' + str(i) + '&per_page=100'
        response = requests.get(url=url)
        data = response.json()
        for i in range(0, len(data)):
            detail = data[i]
            name.append(detail['name'])
            full_name.append(detail['full_name'])
            description.append(detail['description'])
            forks_count.append(detail['forks_count'])
            stargazers_count.append(detail['stargazers_count'])
            watchers_count.append(detail['watchers_count'])
            open_issues_count.append(detail['open_issues_count'])
    community_data = pd.DataFrame({
        'name': name,
        'full_name': full_name,
        'description': description,
        'forks_count': forks_count,
        'stargazers_count': stargazers_count,
        'watchers_count': watchers_count,
        'open_issues_count': open_issues_count
    })
    columns = ['name', 'full_name', 'description', 'forks_count', 'stargazers_count', 'watchers_count',
               'open_issues_count']
    community_data.to_csv('Src-Openeuler-所有社区的信息.csv', columns=columns)
    print('csv已保存！')


get_allch()
