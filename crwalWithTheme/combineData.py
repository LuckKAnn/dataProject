
FILE_NAME= "dataAll01.pkl"
from  crawlWithoutTheme.utils import *


"""
    将三个部分的数据进行聚合
"""
if __name__=="__main__":
    # 193352条
    print("开始读取数据")
    listData = readInPKLSina("./dataWithTheme.pkl")
    count = 0
    listArticle = []
    for data in listData:
        print(data)
        listArticle.append(data)
        count+=1
        if count%500==0:
            for d in listArticle:
                writeInPKLByName(FILE_NAME, d)
            listArticle=[]

    for d in listArticle:
        writeInPKLByName(FILE_NAME, d)

    # 下一个文件
    listData = readInPKLSina("./tmp/dataWithTheme_domestic01.pkl")
    listArticle = []
    for data in listData:
        print(data)
        listArticle.append(data)
        count += 1
        if count % 500 == 0:
            for d in listArticle:

                writeInPKLByName(FILE_NAME, d)
            listArticle = []

    for d in listArticle:
        writeInPKLByName(FILE_NAME, d)

    # 下一个文件
    listData = readInPKLSina("./tmp/dataWithTheme_international01.pkl")
    listArticle = []
    for data in listData:
        print(data)
        listArticle.append(data)
        count += 1
        if count % 500 == 0:
            for d in listArticle:
                writeInPKLByName(FILE_NAME, d)
            listArticle = []

    for d in listArticle:
        writeInPKLByName(FILE_NAME, d)

    print(count)

