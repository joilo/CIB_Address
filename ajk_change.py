# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:48:28 2019

@author: Administrator
"""

#这个爬虫是获取安居客小区数据(需要header)
import requests
from bs4 import BeautifulSoup
#from urllib2 import urlopen, quote
from urllib.request import urlopen,quote
import json
import sys
import time
import urllib.request
import csv
import json
import random
import pandas as pd
import re

header = {#由于安居客网站的反爬虫，这里必须要设置header
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https://wuhan.anjuke.com/sale/?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

header1={
             'authority': 'shanghai.anjuke.com',
             'method': 'GET',
             'path': '/community/view/8',
             'scheme': 'https',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cache-control': 'max-age=0',
             #cookie: aQQ_ajkguid=800FA604-5D1A-00F4-08A9-68DE3E56C4CD; _ga=GA1.2.1498089315.1557366771; 58tj_uuid=fd294f3f-34d9-43de-b8d3-d82fb4d5457f; als=0; propertys=rfcpsr-pr7rxx_rnuzqb-pr7rx1_; wmda_uuid=05489995ac1849eeb7c240ea86ae22c3; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1557478788; _gid=GA1.2.2037604567.1557672399; ajk_member_key=92a6833752ae99f70b73f334488dff97; ajk_member_time=1589208780; lui=160409419%3A1; sessid=AB7A17AE-185A-7CC7-1C2E-4570F1631E1F; lps=http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00f7WWws0JbN600PpAsjGkI9T00000KUv7dC00000TDKLTn.THvs_oeHEtvvO_oyVet0UWdBmy-bIfK15ynLPynzPj-Bnj0zuHRYPWn0IHdDwHbYwbD3rH7jnWDvnWIjnj7jn1c3rRnLnDw7Pj7Kn0K95gTqFhdWpyfqn1ckPWmdnH0dPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz49UhGdpvR8mvqVQ1qspHdfyBdBmy-bIidsmzd9UAsVmh-9ULwG0APzm1Y1P1f4n6%26tpl%3Dtpl_11534_19640_15673%26l%3D1511519766%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2-%2525E5%252585%2525A8%2525E6%252588%2525BF%2525E6%2525BA%252590%2525E7%2525BD%252591%2525EF%2525BC%25258C%2525E6%252596%2525B0%2525E6%252588%2525BF%252520%2525E4%2525BA%25258C%2525E6%252589%25258B%2525E6%252588%2525BF%252520%2525E6%25258C%252591%2525E5%2525A5%2525BD%2525E6%252588%2525BF%2525E4%2525B8%25258A%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2525EF%2525BC%252581%2526xp%253Did%28%252522m3216651054_canvas%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D173%26ie%3Dutf-8%26f%3D3%26tn%3Dbaidu%26wd%3D%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%25E4%25BA%258C%25E6%2589%258B%25E6%2588%25BF%26oq%3Dqq%2525E9%252582%2525AE%2525E7%2525AE%2525B1%26rqlang%3Dcn%26inputT%3D4482; twe=2; wmda_session_id_6289197098934=1557745006672-df700ca3-0c99-3351; init_refer=https%253A%252F%252Fshanghai.anjuke.com%252Fcommunity%252Fpudong-q-beicai%252F; new_uv=17; new_session=0; ctid=11; __xsptplusUT_8=1; __xsptplus8=8.20.1557745010.1557748103.24%232%7Csp0.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23sWn7x3Za7Ci2urFE2igisQuRnV7ly0rT%23
             'referer': 'https://shanghai.anjuke.com/community/pudong/',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

def initial(road,city):  #初始化小区名列表  road 为存储文件路径   例如C:\Users\刘凡\Desktop\深圳.txt
    global name_list
    global error_file
    name_list = []
    road_split = road.split("\\")
    road2 = ""
    for i in road_split[:-1]:
        road2 += i + "\\"
    error_file_road = road2 + "%s_error.txt" % (city)
    error_file = open(error_file_road, 'a+')
    file = open(road)
    for line in file:
        line = line.split('&')
        name = line[0]
        name_list.append(name)
    global log_file
    global finished_district
    finished_district = []
    log_file_road = road2 + "%s_log.txt" % (city)
    log_file = open(log_file_road,'a+')
    log_file = open(log_file_road,encoding='utf8')
    for lines in log_file:
        finished_district.append(lines.replace("\n", ""))
    log_file = open(log_file_road, 'a+')
def isDistrict(district):  #判断当前区是否已经爬取完毕
    if district in finished_district:
        return True
    else:
        return False
def isIn(name):  #判断当前小区名字是否已被爬取过
    if name in name_list:
        return True
    else:
        return False
class ajkxq:
#获取小区信息的函数
    def getRegion(self,citypy):
        time.sleep(random.randint(10, 30) / 10)
        list=[]
        url = 'https://'+citypy+'.anjuke.com/community/'
        response = requests.get(url, headers = header, timeout=1000)
        html = response.content.decode('utf8')
        soup = BeautifulSoup(html,'html.parser')
        info = soup.find('div', class_ = "div-border items-list")
        data = info.find_all(title=True,class_="")
        for line in data:
            url = line['href']
            list.append(re.findall(r"/community/(.+?)/",url))
            #region = line.get_text()
        return list
    
    def getNum(self,url):   #获取小区有多少个
        time.sleep(random.randint(10, 30) / 10)
        response = requests.get(url, headers = header,timeout=1000)
        html = response.content.decode('utf8')
        soup = BeautifulSoup(html,'html.parser')
        info = soup.find('span', class_ = "tit")
        pattern = re.compile(r"小区(.*?)个", re.MULTILINE | re.DOTALL)
        #print(pattern.search(info.get_text()).group(1))
        return int(pattern.search(info.get_text()).group(1).strip())
    
    def getTown(self,district,citypy):    
        time.sleep(random.randint(10, 30) / 10)
        list=[]
        url = 'https://'+citypy+'.anjuke.com/community/'+district+'/'
        response = requests.get(url, headers = header,timeout=1000) 
        html = response.content.decode('utf8')
        soup = BeautifulSoup(html,'html.parser')
        info = soup.find('div', class_ = "sub-items")
        data = info.find_all(class_="")
        for line in data:
            url = line['href']
            list.append(re.findall(r"-q-(.+?)/",url))
        return list
            #region = line.get_text()

    def getLocation(self,url):    #获取小区经纬度信息
        time.sleep(random.randint(10, 30) / 10)
        response = requests.get(url, headers = header1,timeout=1000)  
        html = response.content.decode('utf8')
        soup = BeautifulSoup(html,'html.parser')
        pattern = re.compile(r"lat : \"(.*?)\",(.*?)lng : \"(.*?)\"", re.MULTILINE | re.DOTALL)
        script=soup.find('script',text=pattern)
        return pattern.search(script.text).group(1),pattern.search(script.text).group(3)
		
    def getInfo(self,fh,url):    #获取表层页面小区基本信息
        time.sleep(random.randint(10, 30) / 10)
        response = requests.get(url, headers=header,timeout=1000)
        html = response.content.decode('utf8')
        soup = BeautifulSoup(html,'html.parser')
        info = soup.find('div', class_ = "list-content")
        data = info.find_all('div', class_ = "li-itemmod")
        for line in data:
            name = line.a["title"].strip()
            if isIn(name):
                print(name, "已经爬取过")
                continue
            url = line.a["href"]
            print(url)
            try:
                lat,lnt=self.getLocation(url)
            except Exception as e:
                print("哎呀获取经纬度出问题了！",e)
                error_file.write(name)
                error_file.write("&")
                error_file.write(url)
                error_file.write("\n")
                error_file.flush()
                continue
                    #id = url[42:]
            detail = line.find('div', class_ = "li-info")
            address = detail.address.get_text().strip()
            finished_time = detail.find('p', class_ = "date").get_text().strip()[5:]
            avg_price = line.find('div', class_ = "li-side").p.get_text()
            fh.write(name.strip()+'&'+address.strip() + '&'+lat.strip()+'&'+lnt.strip()+'&'+finished_time.strip()+ '&'+avg_price.strip()+'\n')
                            # strip()是去掉每行后面的换行符，只有str类型才能用strip()
            fh.flush()
            print("success!")
                    

#以福州为例，爬取房源信息
def run(citypy,stradd):
    initial(stradd,citypy)
    print(finished_district)
    fh = open(stradd, "a")
    test=ajkxq()#实例化对象d
    district=test.getRegion(citypy)
    print("地区列表:",district)
    for i in range(len(district)-1):
        if isDistrict(district[i][0]):
            print(district[i][0],"已经爬取完成")
            continue
        url = 'https://'+citypy+'.anjuke.com/community/'+district[i][0]+'/'
        num=test.getNum(url)
        if num<=1500:
            for page in range(1,int(num/30)+2):
                url = 'https://'+citypy+'.anjuke.com/community/'+district[i][0]+'/p' + str(page)+'/'
                print(url)
                try:
                    test.getInfo(fh,url)
                except Exception as e:
                    print(e)
                    continue
        else:
            town=test.getTown(district[i][0],citypy)
            for j in range(len(town)):
                url_1='https://'+citypy+'.anjuke.com/community/'+district[i][0]+'-q-'+town[j][0]+'/'
                num_1=test.getNum(url_1)
                for page_1 in range(1,int(num_1/30)+2):
                    url_1 = 'https://'+citypy+'.anjuke.com/community/'+district[i][0]+'-q-'+town[j][0]+'/p'+str(page_1)+'/'
                    print(url_1)
                    try:
                        test.getInfo(fh,url_1)
                    except Exception as e:
                        print(e)
                        continue
        log_file.write(district[i][0])
        log_file.write('\n')
        log_file.flush()
        
    fh.close()

if __name__ == "__main__":
    citypy='nanjing'
    stradd=r'C:\Users\Administrator.USER-20190427RU\Desktop\nanjing.txt'
    run(citypy,stradd)
    log_file.close()
    error_file.close()
