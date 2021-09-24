import pandas as pd
import re

comment_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
# comment_data = comment_data.sort_values(by='issue_id', ascending=True)
# issue_id_2497_list = list(pd.read_csv(
#     '/Users/wenzong/PycharmProjects/开源社区推荐系统Project/Baseline Model/GAT/issue_id2label2assignee_onehot.csv')[0:2498][
#                               'issud_id'])
issue_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
issue_self_id = issue_data['issue_id']
community_name = issue_data['community_name']
issue_id = list(comment_data['issue_id'])
creator = comment_data['creator']
comments_username = comment_data['commenter']
comments_body = comment_data['body']
comment_time = comment_data['comment_time']
comment_issue_id = []
count = 0
source, target, relation_type, repo = [], [], [], []
commenter_time = []


def get_index(lst=None, item=''):
    return [index for (index, value) in enumerate(lst) if value == item]


def judge(text, all_relate_index):
    print(text, all_relate_index)
    for index in all_relate_index:
        # print(index, comments_body[index])
        if type(comments_body[index]) == float:
            continue
        raw_text = comments_body[index].replace('\n', '').replace('\r', '')
        if text in raw_text:
            # print(True)
            # print(index)
            # print(comments_username[index])
            judege_type = True
            return index, comments_username[index], judege_type
    return 0, 0, False


def comment_relation(comments_body):
    count = 0
    for content in comments_body:
        # if issue_id[count] not in issue_id_2497_list:
        #     count += 1
        #     continue
        if type(content) == float:
            count += 1
            continue
        cite_re_result = re.findall(r'\@(.*?)[^A-Za-z0-9\-_]', content)  # 直接@用户的列表
        print(cite_re_result)
        comment_re_result = re.findall(r'\> \@(.*?)[^A-Za-z0-9\-_]', content)  # 回复中的@用户的列表
        # # re_result = re.findall(r'\d+', content, flags=0)

        print(count)
        print(cite_re_result)
        print(comment_re_result)

        if cite_re_result != []:  # 存在@用户关系
            for name in cite_re_result:  # 遍历@的用户名单
                if name in ['main', 'github', 'tf', '0000', '1', '2', '0000', '0', 'tensorflowbutler'
                            # 'googlebot'
                            ]:  # 去除代码及无关用户干扰
                    continue
                if name.lower() == comments_username[count].lower() and '>' in content:  # 评论者自己@评论自己情况 名称统一小写 使用>确认回复关系
                    print('评论者自己@自己情况')
                    all_relate_index = get_index(issue_id[0: count], issue_id[count])
                    text = re.search(r'\> [^\@][^ ](.*?)\n', content)  # 匹配评论内容

                    if text == None:  # 对于@之后接评论内容，并且评论内容只有一行的情况的处理
                        pattern = r'\> \@' + str(name) + '(.*?)\n'
                        text = re.search(pattern, content)
                        if text == None:  # 代码中的>使得程序误判存在引用评论情况
                            continue
                        else:
                            text = text.group(1)[2:-2]
                            raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
                            if judege_type == False:
                                continue
                            if comments_username[count] == raw_commenter:
                                continue
                            comment_issue_id.append(issue_id[count])
                            repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                            source.append(comments_username[count])
                            target.append(raw_commenter)
                            relation_type.append('commenter to raw_commenter')
                            commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
                            print('commenter to raw_commenter')
                    else:
                        text = text.group(1)[2:-2]
                        print('匹配的文本:', text)
                        raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
                        if judege_type == False:
                            continue
                        print(raw_index, raw_commenter)
                        if comments_username[count] == raw_commenter:
                            continue
                        comment_issue_id.append(issue_id[count])
                        repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                        source.append(comments_username[count])
                        target.append(raw_commenter)
                        relation_type.append('commenter to raw_commenter')
                        commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))

                        print('commenter to raw_commenter')

                else:  # 正常@关系  commenter to @User
                    comment_issue_id.append(issue_id[count])
                    repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                    source.append(comments_username[count])
                    target.append(name)
                    relation_type.append('commenter to @User')
                    commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))

                    print('commenter to @User')


        elif cite_re_result == [] and comment_re_result == []:  # 原回复和现回复都未@用户
            if '>' in content:  # 如果评论中存在引用评论的关系
                all_relate_index = get_index(issue_id[0: count], issue_id[count])
                text = re.search(r'\> [^\@](.*?)\r\n', content)
                if text == None:  # 如果未找到实际存在的引用评论
                    count += 1
                    continue
                else:
                    text = text.group(0)[2:-2]
                    print('原回复和现回复都未@用户情况')
                    print('匹配的文本:', text)

                    raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
                    if judege_type == False:  # 如果没有找到之前的引用评论
                        count += 1
                        continue
                    print(raw_index, raw_commenter)
                    comment_issue_id.append(issue_id[count])
                    repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                    source.append(comments_username[count])
                    target.append(raw_commenter)
                    relation_type.append('commenter to raw_commenter')
                    commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))


            else:  # 评论中不存在引用评论的关系 commenter to issue_creator
                if comments_username[count] == creator[count]:  # 评论者自己评论自己的issue
                    comment_issue_id.append(issue_id[count])
                    repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                    source.append(comments_username[count])
                    target.append(creator[count])
                    relation_type.append('commenter to issue_creator')
                    commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))

                    count += 1
                    continue
                comment_issue_id.append(issue_id[count])
                repo.append(community_name[get_index(issue_self_id, issue_id[count])[0]])
                source.append(comments_username[count])
                target.append(creator[count])
                relation_type.append('commenter to issue_creator')
                commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))

        count += 1
        print('\n')


if __name__ == '__main__':
    comment_relation(comments_body)
    GAt_relation = pd.DataFrame({
        'comment_issue_id': comment_issue_id,
        'repo': repo,
        'source': source,
        'target': target,
        'relation_type': relation_type,
        'commenter_time': commenter_time
    })

    columns = ['comment_issue_id', 'repo', 'source', 'target', 'relation_type', 'commenter_time']
    GAt_relation.to_csv('openeuler+src_comment_relation.csv', index=None, columns=columns)
