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

"""根据公式自行构造的TF-IDF计算方式
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
    dictionary.save('../resource/dictionary.dict')

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


def pretreatment(listData,words_ls,fileName):
    print("开始生成词典")
    dictionary = corpora.Dictionary(words_ls)
    # saveDictionary(dictionary)
    dictionary.save('./store01/{}_dictionary.dict'.format(fileName))
    # 去掉出现次数前三的词
    dictionary.filter_n_most_frequent(3)
    # 去掉仅仅在一篇文章当中出现的词和在90%的文档中都出现的词
    dictionary.filter_extremes(2, no_above=1.0, keep_n=100000)
    print(len(dictionary))
    # print(dictionary.token2id)
    # 重新对词典排序，防止单词序号间的空隙
    dictionary.compactify()
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
    # 形成的是词在dictionary里面的索引和相应词出现的词频
    # 是针对于每一篇文档的
    print("开始每篇文档的重新表示")
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    corpora.MmCorpus.serialize('./store01/{}_corpora.mm'.format(fileName), corpus)  # store to disk, for later use
    # 测试自行编写的TF-IDF
    # tf_IDF(dictionary,corpus[0])

    # useLDA(corpus,dictionary)

def analyzeTheme():
    datas = readInPKLSina("../crwal02/dataAll01.pkl")
    print(len(datas))
    ent=[]
    news=[]
    mil=[]
    finance=[]
    sports = []
    domestic = []
    international = []
    for data in datas:
        theme = data['theme']
        if theme=="ent":
            ent.append(data['content'])
        elif theme=="news":
            news.append(data['content'])
        elif theme=="mil":
            mil.append(data['content'])
        elif theme=="finance":
            finance.append(data['content'])
        elif theme=="sports":
            sports.append(data['content'])
        elif theme=="domestic":
            domestic.append(data['content'])
        elif theme=="International":
            international.append(data['content'])
    return ent,news,mil,finance,sports,domestic,international



def analyzeByTheme():
    ent, news, mil, finance, sports,domestic,international = analyzeTheme()
    words_ls = buildDictionary(ent)
    pretreatment(ent, words_ls, 'ent')
    words_ls = buildDictionary(news)
    pretreatment(news, words_ls, 'news')
    words_ls = buildDictionary(mil)
    pretreatment(mil, words_ls, 'mil')
    words_ls = buildDictionary(finance)
    pretreatment(finance, words_ls, 'finance')
    words_ls = buildDictionary(sports)
    pretreatment(sports, words_ls, 'sports')
    words_ls = buildDictionary(domestic)
    pretreatment(domestic, words_ls, 'domestic')
    words_ls = buildDictionary(international)
    pretreatment(international, words_ls, 'international')




"""
分析和处理不同类别的数据，会进行单独的词典生成和总的词典生成
"""
if __name__=="__main__":
    analyzeByTheme()

