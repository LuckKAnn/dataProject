from pretreatment.Pretreatment import  *
from  crawlWithoutTheme.utils import *
import gensim
"""
    后续工作使用示例
    前面的工作，主要是爬取了数据，同时通过分词，去除停用词等方法，形成全局的词典，之后再用全局的词典重新表示出了每一篇文档
    后续的工作可能用到的就是三部分，原数据，词典，以及每篇文档的表示向量
"""

"""
    通过以下的方式获取词典，词典是(id,词)的形式
"""
dict  = loadDictionary()
dfs = dict.dfs #返回字典：{ 单词id：在多少文档中出现 }
num_docs = dict.num_docs # 返回文档数目
num_pos = dict.num_pos #	返回词的总数（不去重）
token2id = dict.token2id	#返回字典：{ 单词：id }
print(dict)

"""
    通过以下的方式获取每篇文章的表示向量
    courpus，第一级列表内部的每一个列表代表的就是一篇文章的表示向量
"""
courpus = loadCorpora()
print(courpus)
for courpu in courpus[0:2]:
    print(courpu)
tfidf = gensim.models.TfidfModel(courpus)
# 使用tfidf模型将自身的词库转换成tf-idf表示
corpus_tfidf = tfidf[courpus]

for courpu in corpus_tfidf[0:2]:
    print(courpu)

"""
    通过以下的方式获取源数据
    返回的是列表。这个列表当中的每一个对象是一个字典对象，这个字典存储的是一篇文章和其有关信息，其和corpora内的表示向量一样对应
    字典对象示例:
    {
    "id": "32862",
    "topic": "2019年度柬埔寨输华大米达221798吨 创历史新高",
    "content": "原标题：2019年度柬埔寨输华大米数量创出历史新高中新网金边1月1日电 （记者 黄耀辉）当地时间2019年12月31日，中国检验认证集团（简称CCIC）柬埔寨有限公司总经理陈其生向记者表示，截止当日，经该司检验合格和出具证书的2019年度柬埔寨输华大米达到221798吨，比去年增加了35%，创柬埔寨大米出口中国的最高年度记录。陈其生表示，至2019年11月中旬，中国已经完成了中柬两国政府签署的进口柬埔寨大米2018年度30万吨年度计划，并开始执行2019年至2020年度的40万吨采购计划。陈其生解释，2019年度柬埔寨输华大米显著增加，主要是中粮集团（COFCO）根据中柬两国政府的大米贸易协议，加大了采购进度，且不少柬埔寨大米加工厂的生产能力也提高了，增加了供货能力。陈其生说，随着人们越来越关注食品的安全，而柬埔寨大米产区仍保持原生态的生产环境，大米的重金属含量与农药残留都一直符合安全卫生标准，受到越来越多中国消费者的喜爱，国内许多省市和香港的大米进口商也慕名前来采购柬埔寨香米。据陈其生介绍，CCIC柬埔寨公司对大米实施装运前检验工作，并根据中柬两国签署的柬埔寨大米输华检验检疫议定书的要求。同时，中国食品卫生国家标准对大米的卫生安全质量要求和买卖双方签署的贸易合同中的大米品质条款进行，每批大米出口中国之前，都由CCIC柬埔寨公司派出检验员实施驻厂检验，经检验合格才允许包装，并予以全程监督，直到完成整批大米包装工作，在抽样与送检、经实验室品质项目复检和理化项目检测合格，才予以签发证书。陈其生表示，由于严格规范地施检，有效地把好了检验检疫与质量关，几年来柬埔寨输华大米都在中国各口岸顺利通关，受到中国进口商的广泛好评。（完）责任编辑：张玉",
    "time": "20200101"
    }
"""

# datas  = readAllOri("../resource/datasAll.pkl")



"""
    可能还会用到日期和索引的转换 

"""
print(getIndex("20210101"))
print(getDay(366))