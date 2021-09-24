import pandas as pd
from elasticsearch import Elasticsearch
import re
from Data_analysis.TF_ID分析.TF_IDF_fun import TF_IDF_main
from Data_analysis.LDA_model.LDA2 import LDA2
import hanlp
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from gensim import models, corpora

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
tok = HanLP['tok/fine']

# 自定义中文停用词
cn_stopwords = []
with open("../Data_analysis/TF_ID分析/cn_stopwords.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        cn_stopwords.append(line)

# 自定义开源社区字典
tok.dict_force = None
my_dict = []
with open("../Data_analysis/TF_ID分析/my_dict.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        my_dict.append(line)

# 规则标签字典
label_dict = []
label_rule = {'邮件列表': ['邮件', '邮件列表', '邮箱', '求助', '订阅', 'maillist'],
              '多人协作': ['etherpad', '会议记录', 'etherpad', 'openeuler.org'],
              '贡献协议签署': ['cla', '签署', '代码提交'],
              '门禁': ['jenkins', '构建', '静态检查', '测试用例', '编译', '机器人', '测试环境', '功能测试', '测试'],
              '官网': ['下载', '官网', '博客', '镜像', 'iso', 'rpm', '手册'],
              '会议系统': ['开会', '周例会', '会议系统']
              }
for label_type in label_rule:
    for text in label_rule[label_type]:
        label_dict.append(text)
tok.dict_combine = my_dict + label_dict


def query_json_all(colmuns, issue_id):  # 查询
    query_json = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {
                        colmuns: issue_id
                    }}]}}
    }
    return query_json


def query_json_select_community(colmuns1, colmuns2):
    query_json = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {
                        colmuns1: colmuns2
                    }}]}}
    }
    return query_json


def query_add_columns():
    query_json = {
        "properties": {
            "text_split": {
                "type": "Array"
            }
        }
    }
    return query_json


def get_index(lst=None, item=''):
    return [index for (index, value) in enumerate(lst) if value == item]


def user_comment_text(self, user_name):  # 用户评论的文本合并
    comment_data = pd.read_csv(
        '/Users/wenzong/PycharmProjects/开源社区推荐系统Project/Project2/用户专业发现/Raw_data/comments_data_0606_0-6000.csv')
    comment_body = comment_data['comments_body']
    comments_username = comment_data['comments_username']
    comment_issue_id = comment_data['issue_id']
    user_comment_text = ''
    index_list = self.get_index(comments_username, user_name)
    for index in index_list:
        if comment_issue_id[index] in list(issue_id):
            user_comment_text += comment_body[index]
    return user_comment_text


def sig_user_list():
    sig_data = pd.read_csv(
        '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/SIG_Info/sig_repositories_maintainers_data.csv')
    sig_maintainers = sig_data['sig_maintainers']
    user_list = []
    for name in sig_maintainers:
        for i in eval(name):
            user_list.append(i)
    user_list = sorted(set(user_list))
    return user_list


class text_porcess():

    def __init__(self, text):
        self.text = text

    def hanlp_text_spilt(self, text):
        pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
        text = re.sub(pattern, '', text)  # http网址去除
        lower = text.lower()  # 全部小写
        punctuation_set = "!#$%&'*+,/:;<.=>?@【】[\]^`{|}~"
        remove_punctuation_map = dict(
            (ord(char), None) for char in punctuation_set)  # 去除标点符号 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        no_punctuation = lower.translate(remove_punctuation_map)
        simple_punctuation = '[’!"#$%&\'*+,/:;.<=>?@[\\]^`{|}~，。,]'
        no_punctuation = re.sub(simple_punctuation, '', no_punctuation)

        if no_punctuation == '' or len(no_punctuation) == 1:
            return no_punctuation
        else:
            tokens = HanLP(no_punctuation)['tok/fine']
            # ['tok/coarse']
            # ['tok/fine']
            if ' ' in tokens[0]:
                return ''
            else:
                return tokens

    def hanlp_text_spilt_noun(self, text_list):  # 词性选择
        pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
        text = re.sub(pattern, '', text_list)  # http网址去除
        lower = text.lower()  # 全部小写
        punctuation_set = "!#$%&'*+,/:;<.=>?@【】[\]^`{|}~"
        remove_punctuation_map = dict(
            (ord(char), None) for char in punctuation_set)  # 去除标点符号 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        no_punctuation = lower.translate(remove_punctuation_map)
        simple_punctuation = '[’!"#$%&\'*+,/:;.<=>?@[\\]^`{|}~，。,]'
        no_punctuation = re.sub(simple_punctuation, '', no_punctuation)

        if no_punctuation == '' or len(no_punctuation) == 1:
            return no_punctuation
        else:
            tokens = HanLP(no_punctuation)['tok/fine']
            stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文分词
            postag = HanLP(no_punctuation)['pos/pku']  # 词性识别
            index = 0
            tokens_new = []
            for pos in postag:
                if 'n' in pos and 'nr' not in pos or 'm' in pos:  # 只选取n词
                    tokens_new.append(tokens[index])
                index += 1
            tokens = [w for w in tokens_new if not w in stopwords_list]
            return tokens

    def hanlp_textlist_spilt_noun(self, text_list):  # 词性选择
        spilt_text_list = []
        count = 0
        for text in text_list:
            print(count)
            text = self.body_clean(text)  # 数据去噪
            if text == '' or text.replace(' ', '') == '':  # 空格检测并去除
                count += 1
                continue
            pattern = re.compile(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
            text = re.sub(pattern, '', text)  # http网址去除
            lower = text.lower()  # 全部小写
            punctuation_set = "!#$%&'*+,/:;<.=>?@【】[\]^`{|}~"
            remove_punctuation_map = dict(
                (ord(char), None) for char in punctuation_set)  # 去除标点符号 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            no_punctuation = lower.translate(remove_punctuation_map)
            simple_punctuation = '[’!"#$%&\'*+,/:;.<=>?@[\\]^`{|}~，。,]'
            no_punctuation = re.sub(simple_punctuation, '', no_punctuation)

            if no_punctuation == '' or len(no_punctuation) == 1:
                count += 1
                continue
            else:
                tokens = HanLP(no_punctuation)['tok/fine']
                stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文停用词
                postag = HanLP(no_punctuation)['pos/pku']
                index = 0
                tokens_new = []
                for pos in postag:
                    if 'n' in pos and 'nr' not in pos:  # 选择n词
                        tokens_new.append(tokens[index])
                tokens = [w for w in tokens_new if not w in stopwords_list]
                # stemmer = PorterStemmer()  # 词性变化
                # stemmed = self.stem_tokens(tokens, stemmer)
                spilt_text_list.append(tokens)
                count += 1
        return spilt_text_list

    def count_term(self, tokens):  # 停用词 并计算频次
        stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文分词
        filtered_stop_words = [w for w in tokens if not w in stopwords_list]

        # stemmer = PorterStemmer()
        # stemmed = self.stem_tokens(filtered_stop_words, stemmer)

        count = Counter(filtered_stop_words)
        # print(count)
        # print('\n')
        return count

    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))  ## 对类似进行变形过的词汇进行词干抽取
            # # apple和apples表示单复数，process和processing的分词和动名词形式
            # stemmed.append(item)
        return stemmed

    def comment_clean(self):
        text = re.sub(r'\@(.*?)[^A-Za-z0-9\-_]', '', self.text)  # 用户名去除
        text = re.sub(r'\> \@(.*?)[^A-Za-z0-9\-_]', '', text)  # 用户名去除
        text = re.sub(r'\> (.*?)\n', '', text)  # 引用的评论进行去除

        pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
        text = re.sub(pattern, '', text)  # http网址去除
        text = re.sub(r'\s', ' ', text)  # 回车去除
        text = re.sub(r'```(.*?)```', '', text)  # ```代码去除
        text = re.sub(r'`(.*?)`', '', text)  # '  '文本去除
        text = re.sub(r'\#(.*?)\s', '', text)  # #37099 去除
        text = re.sub(r'!\[输入图片说明\]\((.*?)\"\)', '', text)  # #37099 去除
        text = re.sub(r'<!-- #请根据issue的类型在标题右侧下拉框中选择对应的选项（需求、缺陷或CVE等）-->', '', text)  # #37099 去除
        text = re.sub(r'<!-- #请根据issue相关的版本在里程碑中选择对应的节点，若是与版本无关，请选择“不关联里程碑”-->', '', text)  # #37099 去除

        return text

    def body_clean(self, text):
        text = re.sub(r'\@(.*?)[^A-Za-z0-9\-_]', '', text)  # 用户名去除
        text = re.sub(r'\> \@(.*?)[^A-Za-z0-9\-_]', '', text)  # 用户名去除
        text = re.sub(r'\> (.*?)\n', '', text)  # 引用的评论进行去除

        pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # http去除
        text = re.sub(pattern, '', text)  # http网址去除
        text = re.sub(r'\s', ' ', text)  # 回车去除
        text = re.sub(r'```(.*?)```', '', text)  # ```代码去除
        text = re.sub(r'`(.*?)`', '', text)  # '  '文本去除
        text = re.sub(r'\#(.*?)\s', '', text)  # #37099 去除
        text = re.sub(r'!\[输入图片说明\]\((.*?)\"\)', '', text)  # #37099 去除
        text = re.sub(r'<!-- #请根据issue的类型在标题右侧下拉框中选择对应的选项（需求、缺陷或CVE等）-->', '', text)  # #37099 去除
        text = re.sub(r'<!-- #请根据issue相关的版本在里程碑中选择对应的节点，若是与版本无关，请选择“不关联里程碑”-->', '', text)  # #37099 去除

        return text


class TF_IDF():
    def __init__(self, issue_id, user_list):
        self.issue_id = issue_id
        self.user_list = user_list

    def tf_idf_issue_result(self, es_index, columns, countlist=None, ):
        if countlist is None:
            countlist = []
        for id in self.issue_id:
            query = es.search(index=es_index, body=query_json_all('issue_id', issue_id=id))["hits"]["hits"]  # 查询
            query_text = query[0]['_source'][columns]  # 从json中提取文本
            text_porcess_class = text_porcess(query_text)  # 实例化
            tokens = text_porcess_class.hanlp_text_spilt(query_text)  # hanlp分词
            countlist.append(text_porcess_class.count_term(tokens))  # 词出现次数统计
        text_tfidf = TF_IDF_main(countlist)  # TF-IDF计算
        return text_tfidf

    def tf_idf_issue_title(self, es_index, columns, countlist=None):  # 只选取n词 词性
        if countlist is None:
            countlist = []
        for id in self.issue_id:
            query = es.search(index=es_index, body=query_json_all('issue_id', issue_id=id))["hits"]["hits"]  # 查询
            query_text = query[0]['_source'][columns]  # 从json中提取文本
            text_porcess_class = text_porcess(query_text)  # 实例化
            tokens = text_porcess_class.hanlp_text_spilt_noun(query_text)  # hanlp分词
            countlist.append(text_porcess_class.count_term(tokens))  # 词出现次数统计
        text_tfidf = TF_IDF_main(countlist)  # TF-IDF计算
        return text_tfidf

    def tf_idf_user_comment(self, es_index, columns, countlist=None):
        user_text_list, user_spilt_text_list = [], []
        if countlist is None:
            countlist = []
        for user_name in self.user_list:
            user_text_temp = ''
            query = es.search(index=es_index, body=query_json_all('commenter', user_name))["hits"]["hits"]  # 查询
            for query_temp in query:
                query_text = query_temp['_source'][columns]  # 从json中提取文本
                text_porcess_class = text_porcess(query_text)  # 实例化
                text_cleaned = text_porcess_class.body_clean(query_text)  # 数据去噪
                user_text_temp += text_cleaned
            text_porcess_class = text_porcess(user_text_temp)  # 实例化
            tokens = text_porcess_class.hanlp_text_spilt_noun(user_text_temp)  # hanlp分词
            user_text_list.append(user_text_temp)
            user_spilt_text_list.append(tokens)
            text_porcess_class = text_porcess(tokens)  # 实例化
            countlist.append(text_porcess_class.count_term(tokens))  # 词出现次数统计
        text_tfidf = TF_IDF_main(countlist)  # TF-IDF计算
        user_tf_idf = pd.DataFrame({
            'user_name': self.user_list,
            'user_tf_idf': text_tfidf,
            'user_comment_split': user_spilt_text_list
        })
        return user_tf_idf


class LDA():
    def __init__(self, issue_id_list, user_list):
        self.user_list = user_list  # 用户列表

        self.issue_id_list = issue_id_list

    def LDA_issue_title_model(self, es_index, columns, num_topics, num_words):
        # es_index  # es数据库中 搜索要用到的索引名称
        # columns  # 查找到的json中需要用到的列名
        issue_titel_list, word_list = [], []
        index = 0

        # title_list = pd.read_csv(
        #     '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')[
        #                  'title'][0:5000]
        # for title in title_list:
        #     issue_titel_list.append(title)
        # text_porcess_class = text_porcess(issue_titel_list)  # 实例化
        # word_list = text_porcess_class.hanlp_textlist_spilt_noun(issue_titel_list)
        # print(word_list)

        for issue_id in self.issue_id_list:
            query = es.search(index=es_index, body=query_json_all("issue_id", issue_id))["hits"]["hits"]
            query_text = query[0]['_source'][columns]
            word_list.append(query_text)
            index += 1
        text_porcess_class = text_porcess(word_list)  # 实例化
        word_list = text_porcess_class.hanlp_textlist_spilt_noun(word_list)
        topic_word, lda_model = LDA2(word_list, num_topics=num_topics, num_words=num_words)

        return topic_word, lda_model

    def LDA_community_topic(self, community_name_list, es_index, columns, num_topics, num_words):
        issue_titel_list, title_spilt_list, community_list = [], [], []
        for community_name in community_name_list:
            print(community_name)
            query = \
                es.search(index=es_index, body=query_json_all("community_name", community_name), scroll='5m',
                          size=9900)[
                    "hits"][
                    "hits"]
            for query_temp in query:
                _id = query_temp['_id']
                print(_id)
                query_text = query_temp['_source'][columns]
                text_porcess_class = text_porcess(query_text)  # 实例化
                text_cleaned = text_porcess_class.body_clean(query_text)  # 数据去噪
                if text_cleaned == '' or text_cleaned.replace(' ', '') == '':  # 空格检测并去除
                    community_list.append(community_name)
                    issue_titel_list.append(query_text)
                    title_spilt_list.append('')
                    continue
                tokens = text_porcess_class.hanlp_text_spilt_noun(text_cleaned)  # 分词
                es.update(index=es_index, id=_id, body={"doc": {"text_split": tokens}})
                community_list.append(community_name)
                issue_titel_list.append(query_text)
                title_spilt_list.append(tokens)
                print(tokens)
        # community_title = pd.DataFrame({
        #     'community_name': community_list,
        #     'issue_titel': issue_titel_list,
        #     'title_spilt': title_spilt_list
        # })
        # community_title.to_csv('community_title.csv', index=None)

        # title_spilt = list(pd.read_csv('community_title.csv')['title_spilt'])
        # title_spilt_list = []
        # for title in title_spilt:
        #     title_spilt_list.append(eval(title))
        print(title_spilt_list)
        topic_word, lda_model = LDA2(title_spilt_list, num_topics=num_topics, num_words=num_words)

        return topic_word, lda_model

    def LDA_topic_detect(self, lda, dictionary, test):
        doc_bow = dictionary.doc2bow(test)  # 文档转换成bow
        doc_lda = lda[doc_bow]
        return doc_lda

    def LDA_issue_topic(self, lda_model, es_index, columns):
        issue_titel_list, title_spilt_list = [], []
        for issue_id in self.issue_id_list:
            query = es.search(index=es_index, body=query_json_all("issue_id", issue_id))["hits"]["hits"]
            for query_temp in query:
                query_text = query_temp['_source'][columns]
                text_porcess_class = text_porcess(query_text)  # 实例化
                text_cleaned = text_porcess_class.body_clean(query_text)  # 数据去噪
                if text_cleaned == '' or text_cleaned.replace(' ', '') == '':  # 空格检测并去除
                    continue
                tokens = text_porcess_class.hanlp_text_spilt_noun(text_cleaned)  # 分词
                issue_titel_list.append(query_text)
                title_spilt_list.append(tokens)
        dictionary = corpora.Dictionary(title_spilt_list)
        title_topic = []
        for text in title_spilt_list:
            user_lda_topic_list = self.LDA_topic_detect(lda_model, dictionary, text)
            title_topic.append(sorted(user_lda_topic_list))
        title_topic = pd.DataFrame({
            'title_list': issue_titel_list,
            'title_topic': title_topic,
        })
        return title_topic

    def LDA_user_topic(self, lda_model, es_index, columns):
        user_text_list, user_spilt_text_list, dict = [], [], []
        for user_name in self.user_list:
            print(user_name)
            query = es.search(index=es_index, body=query_json_all("commenter", user_name))["hits"]["hits"]
            Raw_text, spilt_text = '', []
            for query_temp in query:
                query_text = query_temp['_source'][columns]
                if query_text == '' or query_text.replace(' ', '') == '':  # 空格检测并去除
                    continue
                text_porcess_class = text_porcess(query_text)  # 实例化
                text_cleaned = text_porcess_class.body_clean(query_text)  # 数据去噪
                if text_cleaned == '' or text_cleaned.replace(' ', '') == '':  # 空格检测并去除
                    continue
                Raw_text += text_cleaned
            text_porcess_class = text_porcess(Raw_text)  # 实例化
            tokens = text_porcess_class.hanlp_text_spilt_noun(Raw_text)  # 分词
            user_text_list.append(Raw_text)
            user_spilt_text_list.append(tokens)
            print(tokens)
            if tokens == '':
                continue
            dict.append(tokens)
        dictionary = corpora.Dictionary(dict)
        user_topic = []
        for text in user_spilt_text_list:
            if text == '':
                user_topic.append('')
                continue
            user_lda_topic_list = self.LDA_topic_detect(lda_model, dictionary, text)
            user_topic.append(sorted(user_lda_topic_list))
        user_topic = pd.DataFrame({
            'user_name': self.user_list,
            'user_comment_raw_text': user_text_list,
            'user_comment_spilt_word': user_spilt_text_list,
            'title_topic': user_topic,
        })
        return user_topic


class issue_label_rule_based():
    def __init__(self, label_rule):
        self.label_rule = label_rule  # 用户列表

    def issue_rule_label(self, es_index, community_name_list, columns):
        issue_id, issue_title, issue_body, issue_label, issue_label_rule = [], [], [], [], []
        for community_name in community_name_list:
            print(community_name)
            query = \
                es.search(index=es_index, body=query_json_all("community_name", community_name), scroll='5m',
                          size=9900)[
                    "hits"][
                    "hits"]
            for query_temp in query:
                _id = query_temp['_id']
                query_text = query_temp['_source'][columns]
                body_text = query_temp['_source']['body']
                query_text += body_text
                text_porcess_class = text_porcess(query_text)  # 实例化
                text_cleaned = text_porcess_class.body_clean(query_text)  # 数据去噪
                tokens = text_porcess_class.hanlp_text_spilt_noun(text_cleaned)  # 分词
                label_list_temp = []
                for label_type in self.label_rule:
                    for text in tokens:
                        if text in label_rule[label_type]:
                            label_list_temp.append(label_type)
                print(sorted(set(label_list_temp)))
                es.update(index=es_index, id=_id, body={"doc": {"label(rule)": sorted(set(label_list_temp))}})
                issue_id.append(query_temp['_source']['issue_id'])
                issue_title.append(query_temp['_source']['title'])
                issue_body.append(query_temp['_source']['body'])
                issue_label.append(query_temp['_source']['label'])
                issue_label_rule.append(sorted(set(label_list_temp)))
        issue_rule_label = pd.DataFrame({
            'issue_id': issue_id,
            'issue_title': issue_title,
            'issue_label_rule': issue_label_rule,
            'issue_label': issue_label,
            'issue_body': issue_body,
        })
        return issue_rule_label



if __name__ == '__main__':
    es = Elasticsearch([{"host": "localhost", "port": 9200}])

    issue_data = pd.read_csv(
        '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
    issue_id = issue_data['issue_id']
    sig_user_name_list = sig_user_list()  # 获取用户名列表

    # tf_idf = TF_IDF(issue_id=issue_id, user_list=sig_user_name_list[0:100])

    # 1.1 TF_IDF issue_title 将issue的title进行tf-idf处理后，将关键词赋予给issue
    # issue_tf_idf_result = tf_idf.tf_idf_issue_title(es_index='all_issue_data',
    #                                                     columns='title')  # issue_id to title_tfidf
    # issue_data['title_tfidf'] = issue_tf_idf_result
    # colums = ['community_name', 'issue_id', 'title_tfidf', 'title', 'body', 'issue_url', 'assignee', 'label', 'creator',
    #           'comments', 'created_at']
    # print(issue_data)
    # issue_data.to_csv('OpenEuler+src_title_tfidf_v2.csv', index=None, columns=colums)

    # 1.2 TF_IDF user_comment 关键词提取
    # user_tf_idf = tf_idf.tf_idf_user_comment(es_index='all_issue_comment', columns='body')
    # user_tf_idf.to_csv('user_tf_idf.csv', index=None)
    # print(user_tf_idf)

    # 1.3 TF_IDF community关键词提取

    ########################################################################################
    # LDA_user_comment = LDA(issue_id_list=issue_id, user_list=sig_user_name_list)
    # # 2.1 LDA 根据title的主题模型
    # topic_word, lda_model = LDA_user_comment.LDA_issue_title_model(num_topics=100,
    #                                                                num_words=20,
    #                                                                es_index='all_issue_data',
    #                                                                columns='title')  # user_list to LDA_output
    # lda_model.save('openeuler_title_lda.model')
    # title_LDA_topic_Topic_100_20 = pd.DataFrame({
    #     'Topic_100_20': topic_word})
    # title_LDA_topic_Topic_100_20.to_csv('title_LDA_topic_Topic_100_20.csv', index=None)
    # print(title_LDA_topic_Topic_100_20)

    # 2.2 LDA Issue 的主题分布
    # lda_model = models.ldamodel.LdaModel.load(
    #     '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/数据分析/Lda_model_100/openeuler_title_lda.model')
    # title_topic = LDA_user_comment.LDA_issue_topic(lda_model, es_index='all_issue_data', columns='title')
    # title_topic.to_csv('title_topic.csv', index=None)
    # print(title_topic)

    # 2.3 LDA user_comment 将用户的所有评论进行LDA处理，将获得的主题词赋予用户
    # lda_model = models.ldamodel.LdaModel.load(
    #     '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/数据分析/Lda_model_100/openeuler_title_lda.model')
    # user_topic = LDA_user_comment.LDA_user_topic(lda_model, es_index='all_issue_comment', columns='body')
    # user_topic.to_csv('user_topic.csv', index=None,
    #                   columns=['user_name', 'title_topic', 'user_comment_raw_text', 'user_comment_spilt_word'])
    # print(user_topic)

    # 2.4 LDA community
    # community_name_list = ['openeuler/community', 'openeuler/kernel', 'openeuler/iSulad']
    # topic_word, lda_model = LDA_user_comment.LDA_community_topic(community_name_list=community_name_list,
    #                                                              es_index='all_issue_data',
    #                                                              columns='title',
    #                                                              num_topics=10,
    #                                                              num_words=5)
    # lda_model.save('openeuler_community_title_lda.model')
    # title_LDA_topic_Topic_10_5 = pd.DataFrame({
    #     'Topic_10_5': topic_word})
    # title_LDA_topic_Topic_10_5.to_csv('select_community_title_LDA_topic_Topic.csv', index=None)
    # print(title_LDA_topic_Topic_10_5)

    ########################################################################################
    # 3.1 Rule based label
    label_rule = {'邮件列表': ['邮件', '邮件列表', '邮箱', '求助', '订阅', 'maillist'],
                  '多人协作': ['etherpad', '会议记录', 'etherpad', 'openeuler.org'],
                  '贡献协议签署': ['cla', '签署', '代码提交'],
                  '门禁': ['jenkins', '构建', '静态检查', '测试用例', '编译', '机器人', '测试环境', '功能测试', '测试'],
                  '官网': ['下载', '官网', '博客', '镜像', 'iso', 'rpm', '手册'],
                  '会议系统': ['开会', '周例会', '会议系统']
                  }
    community_name_list = ['openeuler/infrastructure']
    issue_label = issue_label_rule_based(label_rule)
    issue_rule_label = issue_label.issue_rule_label(es_index='all_issue_data',
                                                    community_name_list=community_name_list,
                                                    columns='title')
    issue_rule_label.to_csv('issue_rule_label.csv', index=None)

