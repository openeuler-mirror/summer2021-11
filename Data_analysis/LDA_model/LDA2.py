from gensim import corpora, models
import jieba.posseg as jp
import jieba
import hanlp
from nltk.corpus import stopwords
import numpy
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
tok = HanLP['tok/fine']
tok.dict_force = None
my_dict = []
with open("../Data_analysis/LDA_model/my_dict.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        my_dict.append(line)
tok.dict_combine = my_dict

cn_stopwords = []
with open("../Data_analysis/LDA_model/cn_stopwords.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        cn_stopwords.append(line)

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
tok = HanLP['tok/fine']
tok.dict_force = None
my_dict = []


# 简单文本处理
def get_text(texts):
    # flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性
    stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文分词
    for w in ['!', ',', '.', '(', ')', '[', ']', '/', '\\', ':', ';', '【', '】', '?', '-s', '-ly', '</s>', 's']:
        stopwords_list.append(w)
    words_list = []
    for text in texts:
        if text == '' or text.replace(' ', '') == '':  # 空格检测并去除
            continue
        words = [w for w in HanLP(text)['tok/fine'] if w not in stopwords_list]
        postag = HanLP(words)['pos/pku']
        index = 0
        tokens_new = []
        for pos in postag:
            if 'n' in pos[0] and 'nr' not in pos[0]:
                tokens_new.append(words[index])
            index += 1
        words_list.append(tokens_new)
    return words_list


# 生成LDA模型
def LDA_model(words_list, num_topics):
    # 构造词典
    # Dictionary()方法遍历所有的文本，为每个不重复的单词分配一个单独的整数ID，同时收集该单词出现次数以及相关的统计信息
    dictionary = corpora.Dictionary(words_list)
    print(dictionary)
    print('打印查看每个单词的id:')
    print(dictionary.token2id)  # 打印查看每个单词的id

    # 将dictionary转化为一个词袋
    # doc2bow()方法将dictionary转化为一个词袋。得到的结果corpus是一个向量的列表，向量的个数就是文档数。
    # 在每个文档向量中都包含一系列元组,元组的形式是（单词 ID，词频）
    corpus = [dictionary.doc2bow(words) for words in words_list]
    print('输出每个文档的向量:')
    print(corpus)  # 输出每个文档的向量

    # LDA主题模型
    # num_topics -- 必须，要生成的主题个数。
    # id2word    -- 必须，LdaModel类要求我们之前的dictionary把id都映射成为字符串。
    # passes     -- 可选，模型遍历语料库的次数。遍历的次数越多，模型越精确。但是对于非常大的语料库，遍历太多次会花费很长的时间。
    lda_model = models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=100)

    return lda_model


def LDA2(words_list, num_topics, num_words):
    # words_list = get_text(texts)
    lda_model = LDA_model(words_list, num_topics)
    # 可以用 print_topic 和 print_topics 方法来查看主题
    # 打印所有主题，每个主题显示5个词
    topic_words = lda_model.print_topics(num_topics=num_topics, num_words=num_words)
    # print('打印所有主题，每个主题显示5个词:')
    # print(topic_words)

    # 输出该主题的的词及其词的权重
    # words_list = lda_model.show_topic(0, 5)
    # print('输出该主题的的词及其词的权重:')
    # print(words_list)
    # print('\n')

    return topic_words, lda_model


def LDA_eval_fun(texts, num_topics):
    # texts = get_text(texts)
    numpy.random.seed(1)

    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # lda_model = LDA_model(words_list, num_topics=num_topics)
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, iterations=50, num_topics=num_topics)

    return lda_model, texts, dictionary, corpus


def LDA3(words_list, num_topics, num_words):
    lda_model = LDA_model(words_list, num_topics=num_topics)
    # 可以用 print_topic 和 print_topics 方法来查看主题
    # 打印所有主题，每个主题显示5个词
    topic_words = lda_model.print_topics(num_topics=num_topics, num_words=num_words)
    print('打印所有主题，每个主题显示5个词:')
    print(topic_words)

    # 输出该主题的的词及其词的权重
    words_list = lda_model.show_topic(0, 5)
    print('输出该主题的的词及其词的权重:')
    print(words_list)
    print('\n')

    return topic_words, lda_model

#
if __name__ == "__main__":
    texts = ["支持BIOS参数调优以及centos操作系统", \
             "是否有计划支持BIOS参数调优", \
             "在centos7.6中部署A-Tune时，安装collector报错，请问是否有计划完善对centos操作系统的支持"]
    # texts = ['离线动态调优框架中，若运行到service命令会导致程序停在某个地方']
    # texts = ['set memory failed when analysis default workload']
    # texts = ['atune-adm analysis时模型导入出错【joblib.load(net_clf.m、cpunet_clf.m)】']
    words_list = get_text(texts)
    print('分词后的文本：')
    print(words_list)

    # # 获取训练后的LDA模型
    # lda_model = LDA_model(words_list)
    #
    # # 可以用 print_topic 和 print_topics 方法来查看主题
    # # 打印所有主题，每个主题显示5个词
    # topic_words = lda_model.print_topics(num_topics=2, num_words=5)
    # print('打印所有主题，每个主题显示5个词:')
    # print(topic_words)
    #
    # # 输出该主题的的词及其词的权重
    # words_list = lda_model.show_topic(0, 5)
    # print('输出该主题的的词及其词的权重:')
    # print(words_list)
    # LDA2(texts)
