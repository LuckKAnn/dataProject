#-*-coding:utf-8-*-
"""
    爬取新浪新闻，每日的热榜
    按照点击量和评论数目，约20篇，地址为http://news.sina.com.cn/hotnews/


"""
import json
import time
from bs4 import BeautifulSoup
import  requests
from tqdm import  tqdm
import pickle
html = "https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_china_suda&top_time={day}&top_show_num=100&top_order=DESC&js_var=hotNewsData"
from crawlWithoutTheme.utils import *
FILE_OUT = "list_data"

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}

FILE_NAME= "./tmp/dataWithTheme_domestic01.pkl"
def mainCrawl(day):
    url =html.format(day=day)
    ret = requests.get(url, headers=headers)
    ret.encoding = 'Unicode'
    first = ret.text.index("{")
    jsonContent = ret.text[first:-2]
    jsonContent = json.loads(jsonContent.strip())
    new_list = jsonContent['data']
    save = []
    for new in new_list:
        CrawlDetail(new,day,save)
    for d in save:
        writeInPKLByName(FILE_NAME, d)

def CrawlDetail(new,day,save):
    try:
        href = new['url']
        article_topic = new['title']
        article_id = new['id']
        # print(href)
        content_ret = requests.get(href, headers=headers)
        content_ret.encoding = content_ret.apparent_encoding
        bs_con = BeautifulSoup(content_ret.text, "html.parser")
        # contents = bs_con.find('div', attrs={"class": "rm_txt_con cf"}).find_all('p')
        atr = bs_con.find('div', attrs={"id": "article"})
        if atr is not None:
            contents = atr.find_all('p')
        else:
            contents = bs_con.find('div', attrs={"class": "article"}).find_all('p')
        if contents is not None:
            ans = ""
            for content in contents:
                ans += content.text.strip()
            # 爬     取的字段:
            # ID：id
            # 主题: topic
            # 内容: content
            # 时间: time
            # 可选参数:
            # 阅读量: read
            # 转载量: trans
            # 点赞量: like
            data = {'id': article_id, 'topic': article_topic, 'content': ans, 'time': day,'theme':"domestic"}
            save.append(data)
    except Exception as e:
        print(e.args)

if __name__=="__main__":
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

