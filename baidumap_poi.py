# -*- coding:utf-8 -*-
import json
import codecs
import os
import urllib
import sys
import time
from urllib.request import urlopen, quote
import csv
import traceback
class WrongCityException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
class Over400Exception(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
class ChangeAKException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
   
def readTag(road):
    global tag
    tag = []
    #file = road
    #data = open(file,'a+')
    data = open(road, encoding='utf-8-sig')
    #data = csv.reader(file)
    for line in data:
        #for i in line[1:]:
            #tag.append(i)
        tag.append(line.replace("\n", ""))
    print(len(tag))
    data.close()
    return tag

def GaoDeAPI(key,bounds,ak,page_num):
    flag = True
    url = "https://restapi.amap.com/v3/place/polygon"
    output = 'json'

def BaiDuAPI(key,bounds,ak,page_num,city):
    flag = True
    url = "http://api.map.baidu.com/place/v2/search"
    output = 'json'
    ak = ak
    keys = quote(key)
    url_send = url + "?query=%s&bounds=%s&output=json&ak=%s&page_size=20&page_num=%s" % (keys, bounds, ak, page_num)
    req = urlopen(url_send,timeout=120)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)
    print(temp)
    if temp['status'] == 301 or temp['status'] == 302 or temp['status'] == 401 or temp['status'] == 402:
        print("换AK异常")
        raise ChangeAKException("要换AK了")
        return flag
    if temp['results'] == [] or temp['status'] == 1:
        flag = False
    elif  temp['results'][0]['name'] == city:
        pass
    elif temp['results'][0]['city'] != city :   #如果爬取信息不在想要获得的城市之中
        raise WrongCityException("城市不对")
        return flag
    elif temp['total'] == 400 :
        for line in temp['results']:
            name = line.get('name','')
            lat = line['location'].get('lat','')
            lng = line['location'].get('lng','')  
            address = line.get('address','')  
            city = line.get('city','')
            area = line.get('area','')
            try: 
                company_data.write(str(name)+"^"+str(key)+"^"+str(lat)+"^"+str(lng)+"^"+str(address)+"^"+str(city)+"^"+str(area)+"\n")
                company_data.flush()
            except Exception as e:
                pass
        #flag = True
        raise Over400Exception("总个数超过400")  #抛出超过400的错误需要调整矩形框大小
    else:
        for line in temp['results']:
            name = line.get('name','') #如果没有name键，就默认为空值
            lat = line['location'].get('lat','')
            lng = line['location'].get('lng','')  
            address = line.get('address','')  
            city = line.get('city','')
            area = line.get('area','')
            try: 
                company_data.write(str(name)+"^"+str(key)+"^"+str(lat)+"^"+str(lng)+"^"+str(address)+"^"+str(city)+"^"+str(area)+"\n")
                company_data.flush()
            except Exception as e:
                pass
        flag = True
    return flag

class LocaDiv(object):
    def __init__(self, loc_all, square_size):  #square_size 为切分的小矩形框的大小 以经纬度为单位 例如0.03
        self.loc_all = loc_all
        self.square_size = square_size

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0].strip())
        lat_ne = float(self.loc_all.split(',')[2].strip())
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / self.square_size)+1):  # 0.1为网格大小，可更改
            lat_list.append(round(lat_sw + self.square_size * i,2))  # 0.05
        lat_list.append(lat_ne)
        #print("lat_list", lat_list)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1].strip())
        lng_ne = float(self.loc_all.split(',')[3].strip())
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / self.square_size)+1):  # 0.1为网格大小，可更改
            lng_list.append(round(lng_sw + self.square_size * i,2))  # 0.1为网格大小，可更改
        lng_list.append(lng_ne)
        #print("lng_list", lng_list)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls = []
        for i in range(len(l1)-1):
            for j in range(len(l2)-1):
                a = str(l1[i]) + "," + str(l2[j])
                b = str(l1[i+1]) + "," + str(l2[j+1])
                ls.append(a+","+b)
        return ls

def initial_AK_pond():   #初始化ak 池 0 为有额度 1为额度已经用完 保存成数组格式
    global ak_dic
    ak_dic = {}
    ak_dic = {
        "g3LUhuGRHmgbf2SFwaCF8yAtGW4nezPS": 0,
        "UKg9gDjYcHMB5hSFMi1HxuQz18f041t1": 0,
        "cq1NkGxVDIyVZSK1xLV2vsfVwOu5ajhV": 0,
        "kIzerPbQFAhs01H85XRNvngmXU73RF8L": 0,
        "mKOV9991B7N98C46kUeNRUXScM067Xys": 0,
        "hvZ5O0of19Alfl7HShUWyOVlFiD8WYWG": 0,
        "5tlPS97zCcgTjbk6gy6AnLVG4p2jtg7u": 0,
        "GEC7Zek74HysO1AKCx1iG6bOXCzTWE6z": 0,
        "9HnBVwKEC01DMgxmINhOSGMt5q1M8kyr": 0,
        "SB3KV3mGWLQ3ncHEk7QfiRNCYHFMYtav": 0,
        "CDjmH9V1ZFfhv9qX2KzGvCrf8UVdUu99": 0,
        "y0j1hsIBRInpjyXub9dFLwsHjnTx73m4": 0,
        "YrwNoo8bNA2Nzfj7pldFXaXVz7iyEPXZ": 0,
        "jGDQ054Yx7n9MNFewodPgykG9UlvlYNa": 0,
        "c5AA39AFSpEAtDCRWWCRhoG5htUrUWvD": 0,
        "lN8FZ9Y8dXeGVdv7aTKvdcnkpXUuMcpQ": 0,
        "zer4hmUsf2Cppl2Z3ozkRMrGx6phGMVf": 0,
        "KdaCBLpAZrUApkiVqjYFSheusOwf2bhh": 0,
        "gwThbIBPPOlUYBQIMUhIP5haNLLkG3Nx": 0,
        "yHHqlqI0pLycBZVlMRjCFtQ8HSyMVWgv": 0,
        "cON4dGCQZyz5IqglB7dYcbCPyrYxoxu1": 0,
    }
def exchange_AK():
    for line in ak_dic.items():
        if line[1] == 0:
            return line[0]
    print("ak池的额度全部用完了")
    return None

def run():
    initial_AK_pond()
    ak = exchange_AK()
    print("初始AK为",ak)
    city = "昆明市"  #填入需要爬取的城市名字
    print("开始爬取数据，请稍等...")
    global company_data
    company_data = open("/Users/ake/Downloads/公司/昆明.txt", 'a+',encoding='utf8')
    tag_list = readTag("/Users/ake/Downloads/公司/行业.txt")
    global error_list
    error_list = open("/Users/ake/Downloads/公司/昆明error.txt", 'a+',encoding='utf8')
    print("标签列表",tag_list)
    bounds = '24.388,102.170,26.545,103.668'
    loc = LocaDiv(bounds, 0.015)  #将城市用最西南 和 最东北的经纬度划分 0.02为划分的矩形大小
    locs_to_use = loc.ls_row()  #生成划分完毕后的 bounds
    print("总共有", len(locs_to_use), "个矩形框")
    global loc_list
    global loc_lists
    loc_lists=[]
    loc_list=open("/Users/ake/Downloads/公司/昆明经纬度.txt", 'a+',encoding='utf8')#用于保存已经检索的矩形区域
    loc_list.seek(0,0)#将光标位置移到文本开始位置
    for line in loc_list:
        loc_lists.append(line.replace("\n", ""))
    break_flag = False  #用于表示跳出循环  当前矩形在框外时触发 跳出两层循环 换到下一个小矩形
    for loc_to_use in locs_to_use:  #遍历每个小矩形框
        print("下一个矩形框",loc_to_use)
        if loc_to_use in loc_lists: #判断矩形是否已经检索过
            print(loc_to_use+"已经检索")
            continue
        for x in tag_list:   #按照标签来跑 例如金融
            sum = 0
            for i in range(20):  #最多20条
                print("第", i, "条", x)
                try:
                    flag = BaiDuAPI(x, loc_to_use, ak, i, city)  #调用百度地图API
                    if flag == False:  # 如果flag 为False 意味着这一次掉用哪个API结果为空，跳出第一层循环
                        break
                except WrongCityException as e:
                    print("捕获到 城市不对异常",e)
                    break_flag = True
                    break
                except Over400Exception as e:
                    print("捕获到 大于400个消息异常",e)
                    if sum == 0: #第一次遇到问题写入
                        writing_str = "超过400个数量错误 在 " + loc_to_use + " " + x + "出了错误"
                        error_list.write(writing_str)
                        error_list.write("\n")
                        error_list.flush()
                        sum += 1
                    continue
                except ChangeAKException as e:  #捕捉AK额度不够的异常
                    print("捕获到AK额度不够的异常")
                    ak_dic[ak] = 1   #将当前AK的状态设置为 已经跑完  P.S 1为已经跑完 0 为还有剩余额度
                    ak = exchange_AK()  #换一个AK
                    print("已经更换AK",ak)
                    print("-----------------等待3s-------------------")
                    time.sleep(3)
                    if ak == None:   #如果调用ak 之后为None 证明ak池的额度全部用完 错误文件记录当前运行结束时的状态
                        error_list.write("在这里停止了:" + loc_to_use + "爬取大区域为"+ bounds)
                        error_list.write("\n")
                        error_list.flush()
                        return None
                    else:
                        continue
                except Exception as e:
                    error_list.write("其他异常:" + loc_to_use + "爬取大区域为"+ bounds)
                    error_list.write("\n")
                    error_list.write(traceback.format_exc()+"\n")
                    error_list.flush()
            if break_flag == True:
                break_flag = False
                break
        loc_list.write(loc_to_use+"\n")
        loc_list.flush()
        

if __name__ == '__main__':
    run()
    company_data.close()
    error_list.close()
    loc_list.close()
