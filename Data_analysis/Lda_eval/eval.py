# LDA 模型性能eval
import pandas as pd
import numpy
from gensim.models.coherencemodel import CoherenceModel
import re
from Data_analysis.LDA_model.LDA2 import LDA_eval_fun


def title_model_eval():
    title_list = []
    for title in issue_title:
        title = comment_clean(title)  # 文本清理
        title_list.append(title)

    numpy.random.seed(1)
    topic_num, score = [], []
    for num in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        print(num)
        LDA_eval, texts, dictionary, corpus = LDA_eval_fun(title_list, num_topics=num)
        c_v = CoherenceModel(model=LDA_eval, texts=texts, corpus=corpus, dictionary=dictionary, coherence='c_v')
        # C_v (Coefficient of variance)：
        # 本方法基于滑动窗口，对主题词进行 one-set 分割（一个 set 内的任意两个词组成词对进行对比），并使用归一化点态互信息 (NPMI) 和余弦相似度来间接获得连贯度。
        temp_score = c_v.get_coherence()
        print('Topic num:', num, temp_score)
        topic_num.append(num)
        score.append(temp_score)
    lda_eval = pd.DataFrame({
        'topic_num': topic_num,
        'score': score,
    })


def title_body_model_eval():
    title_body_list = []
    index = 0
    for title in issue_title:
        temp_text = ''
        title = comment_clean(title)  # 文本清理
        body = issue_cleaned_body[index]
        temp_text += str(title) + str(body)
        title_body_list.append(temp_text)
        index += 1
    print(title_body_list)
    numpy.random.seed(1)
    topic_num, score = [], []
    for num in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        # for num in [2, 4, 6, 8, 10]:
        print(num)
        LDA_eval, texts, dictionary, corpus = LDA_eval_fun(title_body_list, num_topics=num)
        c_v = CoherenceModel(model=LDA_eval, texts=texts, corpus=corpus, dictionary=dictionary, coherence='c_v')
        # C_v (Coefficient of variance)：
        # 本方法基于滑动窗口，对主题词进行 one-set 分割（一个 set 内的任意两个词组成词对进行对比），并使用归一化点态互信息 (NPMI) 和余弦相似度来间接获得连贯度。
        temp_score = c_v.get_coherence()
        print('Topic num:', num, temp_score)
        topic_num.append(num)
        score.append(temp_score)
    lda_eval = pd.DataFrame({
        'topic_num': topic_num,
        'score': score,
    })


def comment_clean(text):
    text = re.sub(r'\@(.*?)[^A-Za-z0-9\-_]', '', text)  # 用户名去除
    text = re.sub(r'\> \@(.*?)[^A-Za-z0-9\-_]', '', text)  # 用户名去除
    text = re.sub(r'\> (.*?)\n', '', text)  # 引用的评论进行去除

    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
    text = re.sub(pattern, '', text)  # http网址去除
    text = re.sub(r'\s', ' ', text)  # 回车去除
    text = re.sub(r'```(.*?)```', '', text)  # ```代码去除
    text = re.sub(r'`(.*?)`', '', text)  # '  '文本去除
    text = re.sub(r'\#(.*?)\s', '', text)  # #37099 去除
    text = re.sub(r'\*\*Googlers\:(.*?)\-\-\>', '', text)
    # print(text)
    # print('\n')
    return text


if __name__ == '__main__':
    issue_data = pd.read_csv(
        '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')[
                 0:5000]
    issue_id = issue_data['issue_id']
    issue_title = issue_data['title']
    title_model_eval()
# 10
# Topic num: 10 0.4330857171145238
# 20
# Topic num: 20 0.456769686715086
# 30
# Topic num: 30 0.4409895815906429
# 40
# Topic num: 40 0.4605205552871368
# 50
# Topic num: 50 0.4447620816014288
# 60
# Topic num: 60 0.45086031841848967
# 70
# Topic num: 70 0.44232334309127447
# 80
# Topic num: 80 0.43807256119646426
# 90
# Topic num: 90 0.42996784365695456
# 100
# Topic num: 100 0.4016122999999912
