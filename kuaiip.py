import requests,re,time,random
from lxml import etree
from threading import Thread #多线程包
#导入需要的包

class IPspider(object):
    def __init__(self,path):
        #指定文件保存路径
        self.path = path

    #添加请求头
    def get_header(self):
        ug_list =[
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        ug = random.choice(ug_list)
        headers = {'User-Agent':ug}
        return headers
    def get_ip(self,pagenum):
        url_list ='https://www.kuaidaili.com/free/inha/'
        #拼接url
        url = url_list + str(pagenum)
        #获取header头
        headers = self.get_header()
        #发送url和header头,设置响应时间，获取响应体
        response = requests.get(url=url,headers=headers).text
        #对获取到的数据进行转译，提供给xpath解析
        data= etree.HTML(response)
        #分析网页结构，获取整页的ip列表
        all = data.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")
        #遍历得到列表，去掉表头
        for i in all:
            #获取host
            host = i.xpath("./td[1]/text()")[0]
            #获取端口号
            port = i.xpath("./td[2]/text()")[0]
            #拼接一个ip地址
            ip = host+":"+port
            #验证ip是否可用
            is_avali=self.check_ip(ip)
            #保存save_ip
            if is_avali:
                self.save_ip(ip)
                self.ip_count()
    def check_ip(self,ip):
        header = self.get_header()
        #使用百度验证ip是否有效
        check_url = 'http://httpbin.org/get'
        #不确定是哪种协议，requests自动识别
        proxies = {'http':'http://'+ip,'https':'https://'+ip}
        #使用try—except，防止报错中断
        try:
            response = requests.get(url=check_url,headers=header,proxies=proxies)
            if  response.status_code == 200:
                return True
        except:
            return False
    def save_ip(self,ip):
        with open(self.path,'a',encoding='utf-8') as f :
            f.write(ip + '\n')

    def ip_count(self):
        #读取ip的个数
        print('开始统计数量')
        with open(self.path,'r',encoding='utf-8') as f:
            #读取ip放进列表中
            ip_list = f.readlines()
                #统计ip数量
            count = len(ip_list)
            #返回数量
            return count

    # 启用多线程爬取
    def start(self):
        #程序运行，创建一个开始时间
        start_time = time.time()
        #创建一个线程池，方便阻塞和开启线程
        threds=[]
        #创建线程，4个网站，每个网站爬取前3页，创建4*3个线程
        #多线程带参数执行，args携带get_ip方法的参数
        for pagenum in range(5):
            t = Thread(target=self.get_ip,args=(pagenum,))
            #放入线程池
            threds.append(t)
        print('开始爬取')
        #开启线程
        for i in threds:
            i.start()
        #阻塞线程，直到threds结束
        for i in threds:
            i.join()
        print('爬取结束')
        #记录结束时间
        end_time = time.time()
        #计算爬取耗时间
        time1 = end_time - start_time
        #获取ip的数量
        ip_count = self.ip_count()
        print("共计获取%s个ip，耗时%s时间"%(ip_count,time1))
if __name__ == '__main__':
    path = 'ip.txt'
    IPspider(path).start()
    time.sleep(3)





