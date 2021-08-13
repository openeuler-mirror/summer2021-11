import pandas as pd
import re
from csv_to_json import csv2json
from 数据分析.LDA_model.LDA import LDA


# from 数据分析.TF_ID分析.Issue_title_body_TFIDF import main


def get_index(lst=None, item=''):
    return [i for i in range(len(lst)) if lst[i] == item]


def sig_user_list():
    sig_data = pd.read_csv('../Data_Crawel/SIG_Info/sig_repositories_maintainers_data.csv')
    sig_maintainers = sig_data['sig_maintainers']
    user_list = []
    for name in sig_maintainers:
        for i in eval(name):
            user_list.append(i)
    user_list = sorted(set(user_list))
    return user_list


def user_sig(user_list):
    sig_data = pd.read_csv('../Data_Crawel/SIG_Info/sig_repositories_maintainers_data.csv')
    sig_maintainers = sig_data['sig_maintainers']
    sig_name = sig_data['sig_name']
    user_sig_list = []
    for name in user_list:
        temp = []
        count = 0
        for name_list in sig_maintainers:
            if name in eval(name_list):
                temp.append(sig_name[count])
            count += 1
        user_sig_list.append(temp)
    print(user_sig_list)
    return user_sig_list


# def judge(text, all_relate_index):
#     for index in all_relate_index:
#         raw_text = comments_body[index].replace('\n', '').replace('\r', '')
#         if text in raw_text:
#             # print(True)
#             # print(index)
#             # print(comments_username[index])
#             judege_type = True
#             return index, comments_username[index], judege_type
#     return 0, 0, False


# def comment_body(content, commenter, creater):
#     cite_re_result = re.findall(r'\@(.*?)[^A-Za-z0-9\-_]', content)  # 直接@用户的列表
#
#     comment_re_result = re.findall(r'\> \@(.*?)[^A-Za-z0-9\-_]', content)  # 回复中的@用户的列表
#     # # re_result = re.findall(r'\d+', content, flags=0)
#
#     print(cite_re_result)
#     print(comment_re_result)
#
#     if cite_re_result != []:  # 存在@用户关系
#         for name in cite_re_result:  # 遍历@的用户名单
#             if name in ['main', 'github', 'tf', '0000', '1', '2', '0000', '0', 'tensorflowbutler', 'openeuler-ci-bot'
#                         # 'googlebot'
#                         ]:  # 去除代码及无关用户干扰
#                 continue
#             if name.lower() == commenter.lower() and '>' in content:  # 评论者自己@评论自己情况 名称统一小写 使用>确认回复关系
#                 print('评论者自己@自己情况')
#                 all_relate_index = get_index(issue_id[0: count], issue_id[count])
#                 text = re.search(r'\> [^\@][^ ](.*?)\n', content)  # 匹配评论内容
#
#                 if text == None:  # 对于@之后接评论内容，并且评论内容只有一行的情况的处理
#                     pattern = r'\> \@' + str(name) + '(.*?)\n'
#                     text = re.search(pattern, content)
#                     if text == None:  # 代码中的>使得程序误判存在引用评论情况
#                         continue
#                     else:
#                         text = text.group(1)[2:-2]
#                         raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
#                         if judege_type == False:
#                             continue
#                         if comments_username[count] == raw_commenter:
#                             continue
#                         comment_issue_id.append(issue_id[count])
#                         source.append(comments_username[count])
#                         target.append(raw_commenter)
#                         relation_type.append('commenter to raw_commenter')
#                         commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
#                         print('commenter to raw_commenter')
#                 else:
#                     text = text.group(1)[2:-2]
#                     print('匹配的文本:', text)
#                     raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
#                     if judege_type == False:
#                         continue
#                     print(raw_index, raw_commenter)
#                     if comments_username[count] == raw_commenter:
#                         continue
#                     comment_issue_id.append(issue_id[count])
#                     source.append(comments_username[count])
#                     target.append(raw_commenter)
#                     relation_type.append('commenter to raw_commenter')
#                     commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
#
#                     print('commenter to raw_commenter')
#
#             else:  # 正常@关系  commenter to @User
#                 comment_issue_id.append(issue_id[count])
#                 source.append(comments_username[count])
#                 target.append(name)
#                 relation_type.append('commenter to @User')
#                 commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
#
#                 print('commenter to @User')
#
#
#     elif cite_re_result == [] and comment_re_result == []:  # 原回复和现回复都未@用户
#         if '>' in content:  # 如果评论中存在引用评论的关系
#             all_relate_index = get_index(issue_id[0: count], issue_id[count])
#             text = re.search(r'\> [^\@](.*?)\r\n', content)
#             if text == None:  # 如果未找到实际存在的引用评论
#                 count += 1
#                 continue
#             else:
#                 text = text.group(0)[2:-2]
#                 print('原回复和现回复都未@用户情况')
#                 print('匹配的文本:', text)
#
#                 raw_index, raw_commenter, judege_type = judge(text, all_relate_index)
#                 if judege_type == False:  # 如果没有找到之前的引用评论
#                     count += 1
#                     continue
#                 print(raw_index, raw_commenter)
#                 comment_issue_id.append(issue_id[count])
#                 source.append(comments_username[count])
#                 target.append(raw_commenter)
#                 relation_type.append('commenter to raw_commenter')
#                 commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
#
#
#         else:  # 评论中不存在引用评论的关系 commenter to issue_creator
#             if comments_username[count] == creator[count]:  # 评论者自己评论自己的issue
#                 comment_issue_id.append(issue_id[count])
#                 source.append(comments_username[count])
#                 target.append(creator[count])
#                 relation_type.append('commenter to issue_creator')
#                 commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))
#
#                 count += 1
#                 continue
#             comment_issue_id.append(issue_id[count])
#             source.append(comments_username[count])
#             target.append(creator[count])
#             relation_type.append('commenter to issue_creator')
#             commenter_time.append(comment_time[count].replace('T', ' ').replace('Z', ''))


def user_comment_user(user_list):
    comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
    comment_commenter = list(comment_data['commenter'])
    comment_creator = comment_data['creator']
    comment_body = comment_data['body']
    comment_label = comment_data['label']
    comment_comment_time = comment_data['comment_time']

    user_comment_time, user_source, user_target = [], [], []
    temp_user_comment_time, temp_user_source, temp_user_target = [], [], []

    count = 0
    for name in user_list:
        comment_index = get_index(comment_commenter, name)
        for index in comment_index:
            if name == 'openeuler-ci-bot' or comment_creator[index] == 'openeuler-ci-bot' or name == comment_creator[
                index]:
                continue
            temp_user_source.append(name)
            temp_user_target.append(comment_creator[index])
            temp_user_comment_time.append(comment_comment_time[index])
    user_comment = pd.DataFrame({
        'comment_source': temp_user_source,
        'comment_target': temp_user_target,
        'timestamp': temp_user_comment_time
    })
    user_comment.to_csv('user_comment.csv', index=None)


def user_label(user_list):
    comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
    issue_label = comment_data['label']
    comment_commenter = list(comment_data['commenter'])
    comment_time = comment_data['comment_time']
    count = 0
    user_name, user_label, user_comment_time = [], [], []
    for name in user_list:
        comment_index = get_index(comment_commenter, name)
        temp_label = []
        for index in comment_index:
            if issue_label[index] == '[]':
                continue
            else:
                for label in eval(issue_label[index]):
                    # temp_label.append(label)
                    user_name.append(name)
                    user_label.append(label)
                    user_comment_time.append(comment_time[index])
        if temp_label == []:
            continue
        # user_name.append(name)
        # user_label.append(temp_label)
    user_label_csv = pd.DataFrame({
        'user_name': user_name,
        'user_label': user_label,
        'user_comment_time': user_comment_time
    })
    user_label_csv.to_csv('user_label_csv.csv', index=None)
    print(user_label_csv)


def user_issue_title_tfidf(user_list):
    comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
    issue_title_tfidf = pd.read_csv('../数据分析/TF_ID分析/OpenEuler+src_title_tfidf_only_eng.csv')
    comment_issue_id = comment_data['issue_id']
    comment_user_name = comment_data['commenter']
    tfidf_issue_id = issue_title_tfidf['issue_id']
    tfidf_value = issue_title_tfidf['title_tfidf']
    output_username, output_tfidf = [], []
    for user_name in user_list:
        issue_id_index = get_index(comment_user_name, user_name)
        isseu_id_list = []
        for index in issue_id_index:
            isseu_id_list.append(comment_issue_id[index])
        isseu_id_list = set(isseu_id_list)
        temp_user_tfidf = []
        for issue_id in isseu_id_list:
            tfidf_index = get_index(tfidf_issue_id, issue_id)
            temp_user_tfidf.append(eval(list(tfidf_value[tfidf_index])[0]))
        temp_user_tfidf = sorted(temp_user_tfidf)
        output_username.append(user_name)
        output_tfidf.append(temp_user_tfidf)
    user_issue_title_tfidf = pd.DataFrame({
        'user_name': output_username,
        'user_issue_title_tfidf': output_tfidf
    })
    user_issue_title_tfidf.to_csv('user_issue_title_tfidf.csv', index=None)


# def user_issue_title_tfidf_2(user_list):
#     comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
#     comment_user_name = comment_data['commenter']
#     comment_body = comment_data['body']
#     comment_issue_id = comment_data['issue_id']
#
#     issue_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
#     issue_title = issue_data['title']
#     issue_id = issue_data['issue_id']
#     for name in user_list:
#         comment_index = get_index(comment_user_name, name)
#         user_comment_body = ''
#         user_issue_title = ''
#         user_issue_id = []
#         for index in comment_index:
#             user_issue_id.append(comment_issue_id[index])
#         user_issue_id = set(user_issue_id)
#         print(user_issue_id)
#         for issue in user_issue_id:
#             print(list(issue_id).index(issue))
#             user_issue_title += issue_title[list(issue_id).index(issue)]
#         print(user_issue_title)
#         print(main(user_issue_title))


def user_comment_LDA(user_list):
    comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
    comment_user_name = comment_data['commenter']
    comment_body = comment_data['body']
    comment_issue_id = comment_data['issue_id']

    issue_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
    issue_title = issue_data['title']
    issue_id = issue_data['issue_id']
    for name in user_list:
        comment_index = get_index(comment_user_name, name)
        user_comment_body = ''
        user_issue_title = ''
        user_issue_id = []
        for index in comment_index:
            user_issue_id.append(comment_issue_id[index])
        user_issue_id = set(user_issue_id)
        print(user_issue_id)
        for issue in user_issue_id:
            print(list(issue_id).index(issue))
            user_issue_title += issue_title[list(issue_id).index(issue)]
        print(user_issue_title)
        LDA([user_issue_title])


user_list = sig_user_list()  # get user list
# user_sig_list = user_sig(user_list) # user sig info
# user_comment_user(user_list) # user comment users count
# user_label(user_list)  # user label count
user_issue_title_tfidf(user_list[0:100])  # user tf-idf count
# user_issue_title_tfidf_2(user_list[0:2])
# user_comment_LDA(user_list[0:1])

# user_deatil = pd.DataFrame({
#     'user_name': user_list,
#     'user_sig': user_sig_list
# })
# user_deatil.to_csv('user_deatil.csv')
# filenames = ('user_name', 'user_label') # csv to json
# csv2json('user_label_csv.csv',filenames)
