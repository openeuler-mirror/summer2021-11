import pandas as pd
import requests

data = pd.read_csv('../Community_Issue_Data/Raw_data/Openeuler_all_issue_data.csv')
headers = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }
issue_id = data['issue_id']
creator = data['creator']
assignee = data['assignee']
label = data['label']
created_at = data['created_at']
community_name = list(pd.read_csv('../Community_Issue_Data/Raw_data/Openeuler-所有社区的信息.csv')['full_name'])  # 按爬取的社区顺序存储
issue_url = data['issue_url']


# issue_list = list(data.loc[data['community_name'] == 'openeuler/A-Tune']['issue_id'])


def scrapyhtml(issue_id, creator, community_name, assignee, label, issue_url, data):
    for i in range(0, len(data)):
        issue = data[i]
        if issue['user']['login'] in ["test-bot", 'openeuler-ci-bot']:
            continue
        # if issue['user']['login'] == creat:
        #     continue
        # if issue['user']['login'] in assignee:
        #     continue
        # if label == '[]':
        #     continue
        community_name_new.append(community_name)
        creator_new.append(creator)
        comments_username_new.append(issue['user']['login'])
        comments_body_new.append(issue['body'])
        issue_id_new.append(issue_id)
        comment_time_new.append(issue['created_at'])
        assignee_new.append(assignee)
        label_new.append(label)
        issue_url_new.append(issue_url)


issue_id_new, issue_url_new = [], []
creator_new, comments_username_new = [], []
comments_body_new, label_new, assignee_new, community_name_new = [], [], [], []
comment_time_new, created_time_new = [], []

count = 0
for name in community_name:
    issue_list = data.loc[data['community_name'] == name]['issue_id']
    for id in issue_list:
        url = ' https://gitee.com/api/v5/repos/' + name + '/issues/' + id + '/comments?access_token=54684bdeddb6825638d58fbd028816ee&page=1&per_page=100&order=asc '
        response = requests.get(url, headers)
        url_data = response.json()
        if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
            print('error: fail to request')
            count += 1
            continue
        scrapyhtml(id, creator[count], name, assignee[count], label[count], issue_url[count],
                   url_data)
        print('一共', len(issue_id), '页', '正在爬取第', count, '页')
        if count % 10 == 0 or count == len(issue_id) - 1:
            comments_body = pd.DataFrame(
                {
                    'issue_id': issue_id_new,
                    'community_name': community_name_new,
                    'creator': creator_new,
                    'comments_username': comments_username_new,
                    'comments_body': comments_body_new,
                    'assignee': assignee_new,
                    'label': label_new,
                    'comment_time': comment_time_new,
                    'issue_url': issue_url_new
                })
            colums = ['community_name', 'issue_id', 'creator', 'comments_username',
                      'comments_body', 'assignee', 'label', 'comment_time', 'issue_url']
            comments_body.to_csv('Openeuler-comments_data.csv', columns=colums, index=None)
            print('已保存')
        count += 1
