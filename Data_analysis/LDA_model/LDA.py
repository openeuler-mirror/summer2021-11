from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
import gensim
import hanlp
from gensim import corpora
from nltk.corpus import stopwords

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
tok = HanLP['tok/fine']
tok.dict_force = None
my_dict = []
with open("my_dict.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        my_dict.append(line)
tok.dict_combine = my_dict

cn_stopwords = []
with open("cn_stopwords.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        cn_stopwords.append(line)


def LDA(doc_complete):
    # 整合文档数据
    doc_complete = doc_complete
    # 加载停用词
    stopwords_list = stopwords.words('english') + cn_stopwords  # 中英文分词

    for w in ['!', ',', '.', '【', '】', '?', '-s', '-ly', '</s>', 's']:
        stopwords_list.append(w)

    with open("/Data_analysis/LDA_model/cn_stopwords.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            stopwords_list.append(line)
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stopwords_list])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        tokens = HanLP(normalized)['tok/fine']
        print(tokens)
        return tokens

    doc_clean = [clean(doc) for doc in doc_complete]

    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    dictionary = corpora.Dictionary(doc_clean)
    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # 使用 gensim 来创建 LDA 模型对象
    Lda = gensim.models.ldamodel.LdaModel

    # 在 DT 矩阵上运行和训练 LDA 模型
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word=dictionary, passes=50, random_state=3)
    # 输出结果
    print(ldamodel.print_topics(num_topics=3, num_words=3))
    return ldamodel.print_topics(num_topics=3, num_words=3)


doc1 = "支持BIOS参数调优以及centos操作系统"
doc2 = "是否有计划支持BIOS参数调优"

doc3 = "在centos7.6中部署A-Tune时，安装collector报错，请问是否有计划完善对centos操作系统的支持"

doc_complete = [doc1 + doc2 + doc3]
LDA(doc_complete)
