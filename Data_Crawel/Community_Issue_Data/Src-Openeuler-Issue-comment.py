import pandas as pd
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }


def Crawling(repo, id, creator, label):
    url = 'https://gitee.com/api/v5/repos/' + repo + '/issues/' + id + '/comments?access_token=dd6f09ca82448c85f5a845a31c1f4519&page=1&per_page=100&order=asc'
    response = requests.get(url=url)
    data = response.json()
    if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
        print('error: fail to request')
        return
    for i in range(0, len(data)):
        issue = data[i]
        if issue['user']['type'] != "User" or issue['user']['name'] == 'openeuler-ci-bot':
            continue
        issue_id_.append(id)
        commenter.append(issue['user']['login'])
        creator_.append(creator)
        body.append(issue['body'])
        label_.append(label)
        comment_time.append(issue['created_at'])


if __name__ == "__main__":
    Openeuler_all_issue_data = pd.read_csv('Src-Openeuler_all_issue_data_2.csv')
    issue_id = Openeuler_all_issue_data['issue_id']
    creator = Openeuler_all_issue_data['creator']
    label = Openeuler_all_issue_data['label']
    community_name = Openeuler_all_issue_data['community_name']
    comments = Openeuler_all_issue_data['comments']
    commenter, comment_time, creator_, label_, issue_id_, body = [], [], [], [], [], []
    count = 0
    for id in issue_id:
        if comments[count] <= 1:
            count += 1
            continue
        # time.sleep(0.1)
        Crawling(community_name[count], id, creator[count], label[count])
        print('第{count}个Issue爬取完毕,共{all}条issue'.format(count=count, all=len(issue_id)))
        if count % 50 == 0:
            src_openeuler_issue_comment = pd.DataFrame({
                'commenter': commenter,
                'creator': creator_,
                'issue_id': issue_id_,
                'body': body,
                'label': label_,
                'comment_time': comment_time,
            })
            src_openeuler_issue_comment.to_csv('Src-openeuler_issue_comment_2.csv', index=None)
            print('csv save！')
        count += 1

    src_openeuler_issue_comment = pd.DataFrame({
        'commenter': commenter,
        'creator': creator_,
        'issue_id': issue_id_,
        'body': body,
        'label': label_,
        'comment_time': comment_time,
    })
    src_openeuler_issue_comment.to_csv('Src-openeuler_issue_comment_2.csv', index=None)
    print('All csv save！')
