import json
import pickle
import time


def writeInPKL(list_data):
    with open("list_data", "ab+") as fo:         #write
       pickle.dump(list_data, fo)
       fo.close()



def readXinHuaInPKL(fileName):
    with open(fileName, "rb") as fo:  # read
        datas = []
        try:
           while True:
                A = pickle.load(fo, encoding='bytes')
                datas.append(A)
                # jdata = json.loads(A)
        except EOFError as e:
            print("文件读取完成")
        # 返回json对象
        return json.dumps(datas, ensure_ascii=False)


# 读取新浪的数据
def readInPKLSina(fileName):
    with open(fileName, "rb") as fo:  # read
        datas = []
        try:
            while True:
                A = pickle.load(fo, encoding='bytes')
                datas.append(A)
                # jdata = json.loads(A)
        except EOFError as e:
            print("文件{file}读取完成".format(file=fileName))
        # 返回json对象
        return datas
# 根据传入的文件名称写入相应的数据
def writeInPKLByName(file_name,list_data):
    with open(file_name, "ab+") as fo:         #write
       pickle.dump(list_data, fo)
       fo.close()

def addZeroToSingleNum(num):
    ans = ""
    if num<10:
        ans+="0"

    ans+=str(num)
    return  ans



def combineAllData():
    dataAll = []
    datas01 = readInPKLSina("xinlangnews-all")
    datas02 = readInPKLSina("xinlangnews-all02")
    print(type(datas01))
    # print(datas)
    datas03 = readXinHuaInPKL("list_data")
    datas03_list = readInPKLSina("list_data")
    datas04_list = readInPKLSina("list_data_to_210403")
    allLen = len(datas01)+len(datas02)+len(datas03_list)+len(datas04_list)
    print("总长度:"+str(allLen))  #总长度:66629
    # print(json.loads(datas03))
    # time.sleep(100)
    for datas in datas01:
        dataAll.append(datas)
    for datas in datas02:
        dataAll.append(datas)
    for datas in datas03_list:
        dataAll.append(datas)
    for datas in datas04_list:
        dataAll.append(datas)
    writeInPKLByName("datasAll.pkl", dataAll)



# 读取总数据
# 返回的是包含源数据的list集合
def readAllOri(fileName):
    with open(fileName, "rb") as fo:  # read
        try:
            while True:
                A = pickle.load(fo, encoding='bytes')
                jdata = json.loads(json.dumps(A))
        except EOFError as e:
            print("文件{file}读取完成".format(file=fileName))
        # 返回json对象
        return jdata

def countData():
    count = []
    for i in range(getIndex(20211031)+1):
        count.append(0)

    datas = readAllOri("../resource/datasAll.pkl")
    # datas = readInPKLSina("../ori/xinlangnews-all")
    print(type(datas))
    for data in datas:
        day = data['time']
        dayIndex = getIndex(day)
        count[dayIndex]+=1
    for i in range(len(count)):
        print(getDay(i)+":"+str(count[i]))


"""
 传入的日期格式为: 20200110之类的
 返回索引
 以20200101索引为1
"""
def getIndex(times):
    times = str(times)
    year =int( times[:4])
    month = int(times[4:6])
    day = int(times[6:])
    index = 0
    if year>2020:
        index+=366

    for i in range(1,13):
        if month>i:
            if i in (1,3,5,7,8,10,12):
                index+=31
            elif year==2020 and i==2:
                index+=29
            elif year==2021 and i==2:
                index+=28
            else:
                index+=30
    index+=day-1
    return index


"""
 传入索引返回日期
"""
def getDay(index):
    index+=1
    for i in range(2020, 2022):
        for j in range(1, 13):
            flag = False
            if i == 2020 and j == 2:
                if index>29:
                    flag=True
                    index -= 29
            elif i == 2021 and j == 2:
                if index > 28:
                    flag = True
                    index -= 28
            elif j in (1, 3, 5, 7, 8, 10, 12):
                if index>31:
                    flag=True
                    index-= 31
            else:
                if index > 30:
                    flag = True
                    index-= 30
            if not flag:
                ymd = str(i) + addZeroToSingleNum(j) + addZeroToSingleNum(index)
                return ymd

    # 转换出错
    return  -1

