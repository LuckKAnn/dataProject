import math
import time

from gensim import corpora, models
import jieba.posseg as jp, jieba

STOP_WORDS_FILE= "../resource/stop_words_ch-停用词表.txt"
from  crawlWithoutTheme.utils import *
# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open(STOP_WORDS_FILE).readlines()]
    return stopwords
"""
    构造词典的过程，也是进行分词和停用词处理的过程
"""
def buildDictionary(jData):
    # 文本集
    texts = jData
    # 分词过滤条件
    jieba.add_word('n')
    flags = ('n')
    stopwords = stopwordslist()
    # 分词,去除停用词
    words_ls = []
    for text in texts:
        words = [w.word for w in jp.cut(text) if w.flag in flags and w.word not in stopwords and w.word not in words_ls]
        words_ls.append(words)
    # 构造词典
    return words_ls

"""根据公式自行构造的TF-IDF计算方式,但是没有使用
    实际上corpora模型自带了计算TF-IDF的模型
"""
def tf_IDF(dictionary,article):
    num_docs = dictionary.num_docs
    docs_showTime = dictionary.dfs
    print(article)
    for word in article:
        index = word[0]
        Dx = word[1]
        D = docs_showTime[index]
        tf = Dx/num_docs
        idf = math.log(D+1/Dx+1)+1
        tfIdf = tf*idf
        print(dictionary[index]+"--------->tfidf:"+str(tfIdf))


def saveDictionary(dictionary):
    dictionary.save('../crawlWithoutTheme/store01/dictionary.dict')

def loadDictionary():
    dict = corpora.Dictionary()
    dictionary = dict.load('../resource/dictionary.dict')

    return  dictionary

def loadCorpora():
    corpus = corpora.MmCorpus('../resource/corpora.mm')
    return  corpus

def useLDA(corpus,dictionary):
    # LDA模型使用示例
    # lda模型，num_topics设置主题的个数
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2)
    # 打印所有主题，每个主题显示5个词
    for topic in lda.print_topics(num_words=5):
        print(topic)
    # 主题推断
    # print(lda.inference(corpus))
    for e, values in enumerate(lda.inference(corpus)[0]):
        for ee, value in enumerate(values):
            print('\t主题%d推断值%.2f' % (ee, value))


def pretreatment(listData,words_ls):
    print("开始生成词典")
    dictionary = corpora.Dictionary(words_ls)
    saveDictionary(dictionary)
    # 去掉出现次数前三的词
    print("开始去除一些高/低频词汇")
    dictionary.filter_n_most_frequent(3)
    # 去掉仅仅在一篇文章当中出现的词和在90%的文档中都出现的词
    dictionary.filter_extremes(2,no_above=1.0,keep_n=100000)
    print(len(dictionary))
    # print(dictionary.token2id)
    # 重新对词典排序，防止单词序号间的空隙
    dictionary.compactify()
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
    # 形成的是词在dictionary里面的索引和相应词出现的词频
    # 是针对于每一篇文档的
    print("开始每篇文档的重新表示")
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    corpora.MmCorpus.serialize('../crawlWithoutTheme/store01/corpora.mm', corpus)  # store to disk, for later use
    # 测试自行编写的TF-IDF
    # tf_IDF(dictionary,corpus[0])
    # useLDA(corpus,dictionary)

if __name__=="__main__":
    # listData = readAllOri("../resource/datasAll.pkl")
    listData = readInPKLSina("../crwalWithTheme/dataAll01.pkl")
    listArticle = []
    for data in listData:
        listArticle.append(data['content'])
    print(len(listArticle))
    words_ls = buildDictionary(listArticle)
    pretreatment(listData,words_ls)

