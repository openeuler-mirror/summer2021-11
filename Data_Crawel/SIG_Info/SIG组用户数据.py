import pandas as pd
import requests
import base64
import yaml
import json

headers = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }


def scrapyhtml_sig_overall_data(url_data):
    sig_name, sig_repositories = [], []
    content = url_data['content']
    content_decode = base64.b64decode(content).decode()
    data = yaml.load(content_decode)['sigs']
    for i in range(0, len(data)):
        temp_data = data[i]
        name = temp_data['name']
        repositories = temp_data['repositories']
        sig_name.append(name)
        sig_repositories.append(repositories)
    sig_repositories_list = pd.DataFrame({
        'sig_name': sig_name,
        'sig_repositories': sig_repositories
    })
    return sig_repositories_list


def scrapyhtml_sig_detail_data(sig_name):
    url2 = 'https://gitee.com/api/v5/repos/openeuler/community/contents/sig%2F' + sig_name + '%2FOWNERS?access_token=54684bdeddb6825638d58fbd028816ee'
    response = requests.get(url2, headers)
    url_data = response.json()
    content = url_data['content']
    content_decode = base64.b64decode(content).decode()
    data = yaml.load(content_decode)['maintainers']
    temp_sig_maintainers = []
    # sig_name.append(sig_name)
    for i in range(0, len(data)):
        temp_data = data[i]
        temp_sig_maintainers.append(temp_data)
    sig_maintainers.append(list(temp_sig_maintainers))

    return sig_maintainers


url = 'https://gitee.com/api/v5/repos/openeuler/community/contents/sig%2Fsigs.yaml?access_token=54684bdeddb6825638d58fbd028816ee'
response = requests.get(url, headers)
url_data = response.json()
if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
    print('error: fail to request')
sig_repositories_list = scrapyhtml_sig_overall_data(url_data)
sig_list = sig_repositories_list['sig_name']
sig_maintainers, sig_name = [], []
for name in sig_list:
    scrapyhtml_sig_detail_data(name)
sig_repositories_list['sig_maintainers'] = sig_maintainers
sig_repositories_list.to_csv('sig_repositories_maintainers_data.csv',index=None)
