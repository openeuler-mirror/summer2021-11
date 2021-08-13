import hanlp
import pandas as pd
import math
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
# output = HanLP(['智能解析引擎所用到的正则库pygrok依赖于正则库python-regex', 'suggest to provide English version README'])
# print(output['tok/coarse'])
oe_closed_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/Raw_data/Openeuler_all_issue_data.csv')[0:10]
title = oe_closed_data['title']
body = oe_closed_data['body']
issue_id = oe_closed_data['issue_id']
label = oe_closed_data['label']
issue_url = oe_closed_data['issue_url']
cn_stopwords = []
with open("cn_stopwords.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        cn_stopwords.append(line)


# print(stopwords.words('english'))


# for i in title:
#     output = HanLP(i)['tok/coarse']
#     print(output)


def get_tokens(text):
    lower = text.lower()  # 英文全部设置为小写
    punctuation_set = "!#$%&'*+,-/:;<=>?@[\]^_`{|}~"
    remove_punctuation_map = dict(
        (ord(char), None) for char in punctuation_set)  # 去除标点符号 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    no_punctuation = lower.translate(remove_punctuation_map)
    tokens = HanLP(no_punctuation)['tok/coarse']
    # print(tokens)
    return tokens


# 对类似进行变形过的词汇进行词干抽取
# apple和apples表示单复数，process和processing的分词和动名词形式
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
        stemmed.append(item)
    return stemmed


# 一段文本中出现的频率较高的词
def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# 逆文档频率
def idf(word, count_list):
    return math.log(len(count_list)) / (1 + n_containing(word, count_list))


# TF-IDF的值
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


def count_term(text):
    tokens = get_tokens(text)
    stopwords_list = stopwords.words('english') + cn_stopwords
    filtered_stop_words = [w for w in tokens if not w in stopwords_list]

    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered_stop_words, stemmer)

    count = Counter(stemmed)
    return count


def main():
    title = oe_closed_data['title']
    title_tfidf, countlist = [], []
    count = 0
    for text in title:
        countlist.append(count_term(text))
        # print(count_term(text))
    index = 0
    for i, count in enumerate(countlist):
        # print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        temp_word = []
        temp_score = []
        # print(sorted_words[:5])
        # for word, score in sorted_words:
        # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
        title_tfidf.append(sorted_words)
        index += 1

    title_tfidf = pd.DataFrame(
        {'issue_id': issue_id, 'title_tfidf': title_tfidf, 'title': title, 'issue_url': issue_url, 'label': label})
    title_tfidf.to_csv('OpenEuler_title_tfidf.csv', index=None)


if __name__ == "__main__":
    main()
