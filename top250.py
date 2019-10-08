import requests,time,json
from requests import RequestException
from lxml import etree
from bs4 import BeautifulSoup as bf
from pyquery import PyQuery as pq

#爬取数据
def pageHtml(url):
    try:
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        res = requests.get(url,headers=headers)
        if res.status_code == 200 :
            return res.text
        else:
            return None
    except RequestException:
        return None
#解析数据
def parseHtml(contant):
    # print(html)
    #用xpath解析
    html  = etree.HTML(contant)
    items = html.xpath("//tr[@class='item']")#获取所有的table标签
    # print(len(items))
    try:
        for item in items:
           yield {
                "书名": item.xpath(".//div[@class='pl2']/a/text()")[0].strip(),
                "原名":item.xpath(".//div[@class='pl2']/span/text()"),
                "图片":item.xpath(".//a[@class='nbg']/img/@src"),
                "作者":item.xpath(".//p[@class='pl']/text()"),
                "评分":item.xpath(".//span[@class='rating_nums']/text()"),
                "描述":item.xpath(".//span[@class='inq']/text()"),
           }

    except Exception:
        print('')

#存储数据
def saveContant(item):
    with open('top250.txt','a',encoding='utf-8') as f:
            #ensure_ascii=False这是json在处理中文时选择用ascii码来完成
            f.write(json.dumps(item,ensure_ascii=False)+'\n')

#主函数
def main(offset):
    url = "https://book.douban.com/top250?start=%s"%str(offset)
    html = pageHtml(url)#执行爬取
    if html:
        for item in  parseHtml(html): #执行解析
            saveContant(item)



#判断是否在当前执行程序
if __name__ == '__main__':
    for i in range(10):
        print('='*40,str(i+1),'次','='*40)
        main(offset=i * 25)
        time.sleep(3)

