import hanlp
import pandas as pd
import math
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
import re

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
tok = HanLP['tok/fine']
# output = HanLP(['智能解析引擎所用到的正则库pygrok依赖于正则库python-regex', 'suggest to provide English version README'])
# print(output['tok/coarse'])
# oe_closed_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
# title = oe_closed_data['title']
# issue_id = oe_closed_data['issue_id']
# label = oe_closed_data['label']
# issue_url = oe_closed_data['issue_url']

cn_stopwords = []
with open("../Data_analysis/TF_ID分析/cn_stopwords.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        cn_stopwords.append(line)

tok.dict_force = None
my_dict = []
with open("../Data_analysis/TF_ID分析/my_dict.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        my_dict.append(line)
tok.dict_combine = my_dict


def get_tokens(text):
    print(text)
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


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))  ## 对类似进行变形过的词汇进行词干抽取
        # # apple和apples表示单复数，process和processing的分词和动名词形式
        # stemmed.append(item)
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
    stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文分词
    filtered_stop_words = [w for w in tokens if not w in stopwords_list]

    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered_stop_words, stemmer)

    count = Counter(stemmed)
    print(count)
    print('\n')
    return count


def TF_IDF_main(countlist):
    title_tfidf = []

    index = 0
    for i, count in enumerate(countlist):
        # print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        title_tfidf.append(sorted_words)
        index += 1

    return title_tfidf

# if __name__ == "__main__":
#     title = oe_closed_data['title']
#
#     TF_IDF_main(title)
