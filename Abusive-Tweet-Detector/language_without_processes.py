from __future__ import print_function
import json
import sys
import codecs
#import urllib.request
import binascii
import os
# from multiprocessing import Process,Manager

path = "/home/bt1/13CS10060/socompProject/finalPublish/mappedData"

def getFileList():
    files = os.listdir(path)
    return files

dt = {}
dw = {}

def getLanguage(tweet_id,word):
    tup = (0,0)
    if tweet_id in dw.keys():
        if word in dw[tweet_id].keys():
            label = dw[tweet_id][word]['Label']
            matrix = dw[tweet_id][word]['Matrix']
            tup = (label,matrix)

    return tup

def getTweet(tweet_id):
    if tweet_id  in dt.keys():
        return dt[tweet_id]
                
    

def parse(file,jn):
    #file1 = codecs.open(path+"/"+file,'r','utf-8')
    i = 0
    with open(path+"/"+file) as file1:
        for row in file1:
            d = {}
            d = json.loads(row)
            for key in d:
                try:
                    i = i+1
                    dwl = {}
                    #print(d[key])
                    dt[key] = d[key]['Tweet']
                    dw[key] = d[key]['Word-level']
                except Exception as e:
                    print(e,file,key)
    print(file,end = '\t')
    print(i)

def init():
    global dt
    global dw
    filelist = getFileList()
    processes = []
    fn = parse
    j = 0
    for jfile in filelist:
        if(jfile == "allall.json" or jfile == "tweetsonly.json"):
            continue
        #arg = (jfile,j)
        #p = Process(target=fn,args=arg,name=jfile)
        #p.start()
        #processes.append(p)
        j = j+1
        parse(jfile,j)
    print(len(dw),"  ",len(dt))
    temp = dict()
    for item in dw.items():
        temp[item[0]] = item[1]
    dw = temp
    temp = dict()
    print("DW done",len(dw))
    '''for item in dt.items():
        temp[item[0]] = item[1]
    dt = temp
    print("DT done",len(dt))
    onlytweetfile = codecs.open(path+"/tweetsonly.json","w","utf-8")
    allfile = codecs.open(path+"/allall.json","w","utf-8")
    print(json.dumps(dw,ensure_ascii=False),file=allfile)
    print(json.dumps(dt,ensure_ascii=False),file=onlytweetfile)
    onlytweetfile.close()
    allfile.close()'''

