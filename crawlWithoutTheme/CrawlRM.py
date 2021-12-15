#-*-coding:utf-8-*-

import json
import time
# 0lXzv_waZ9d0H08zpB9gFGpOO27RcMcNurad6ecA
from bs4 import BeautifulSoup
import  requests
from tqdm import  tqdm
import pickle
html = "http://www.people.com.cn/GB/59476/review/{day}.html"
from  utils import *
FILE_OUT = "list_data"

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}
def mainCrawl(day):
    datas = []
    count = 0
    url = html.format(day=day)
    print(url)
    ret = requests.get(url, headers=headers)
    ret.encoding = ret.apparent_encoding
    bs = BeautifulSoup(ret.text, "html.parser")
    headers['Referer'] = url
    contentTd = bs.find(name='td', attrs={"class": "p6"}).find_all('a')
    for i in contentTd:
        try:
            href = i.get('href')
            # print(href)
            article_id = href.split('/')[-1][:-5]
            article_topic = i.text
            content_ret = requests.get(href, headers=headers)
            content_ret.encoding = content_ret.apparent_encoding
            bs_con = BeautifulSoup(content_ret.text, "html.parser")
            contents = bs_con.find('div', attrs={"class": "rm_txt_con cf"}).find_all('p')
            if contents is not None:
                ans = ""
                for content in contents:

                    ans += content.text.strip()
                # 爬取的字段:
                # ID：id
                # 主题: topic
                # 内容: content
                # 时间: time
                # 可选参数:
                # 阅读量: read
                # 转载量: trans
                # 点赞量: like
                count += 1
                data = {'id': article_id, 'topic': article_topic, 'content': ans, 'time': day}
                datas.append(data)
                writeInPKL(data)
        except Exception as e:
            print(end="")


    # json_data = json.dumps(datas, ensure_ascii=False)
    # print(json_data)
    # writeInPKL(json_data)
    # readInPKL(FILE_OUT)
    return count

    # goods = ansJson['']

if __name__=="__main__":
    counttmp = 0
    count_data = []
    for i in range(2020,2022):
        for j in range(1,13):
            if i==2020 and j==2:
                day = 29
            elif i==2021 and j==2:
                day = 28
            elif i==2021 and j>=11:
                break
            elif j in (1,3,5,7,8,10,12):
                day = 31
            else:
                day=30
            for k in range(1,day+1):
                ymd = str(i)+addZeroToSingleNum(j)+addZeroToSingleNum(k)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++开始爬取日期:"+ymd+"的数据+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                count = mainCrawl(ymd)
                counts = {'id': ymd, 'count': count}
                count_data.append(counts)
                time.sleep(5)
            print(count_data)
