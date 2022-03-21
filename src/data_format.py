#语料库的预处理
import numpy as np
import re
import json
import os
from tqdm import tqdm
from filepath import LIB_PATH

#TODO：这个方式好像识别率还下降了
num2char_dict = {"1":"零","1":"一","2":"二","3":"三","4":"四","5":"五","6":"六","7":"七","8":"八","9":"九"}

def num2char(num) :
    repl = num2char_dict.get(num.group('val'),"")
    return repl


#处理语料库，提取出每条新闻的html和title,并将其清洗为只有汉字余留
def read_news(path : str) :
    data = []
    with open(path,encoding="gbk")as f:
        raw_data = f.readlines()
        sentence_data = []
        print("fetching data from json")
        for raw_news in tqdm(raw_data) :
            #对每一行数据，先loadinjson，再提取出它们的每一行
            json_data = json.loads(raw_news)
            sentence_data.append(json_data["html"])
            sentence_data.append(json_data["title"])
        print("cleaning invalid chars")
        for sentence in tqdm(sentence_data) :
            raw_line = re.split(r'[，。！：]',sentence)
            for line in raw_line :
                #TODO:或许之后可以有更精细的划分方式，比如可以把数字全部改成汉字显示
                num_changed_line = re.sub('(?P<val>\d)', num2char , line)
                data.append((''.join(re.findall('[\u4e00-\u9fa5]',num_changed_line)))+"\n")
    return data
#data = read_news("./database_lib/database/sina_news_gbk/2016-02.txt")

news_path = LIB_PATH+"database_lib/database/sina_news_gbk/"
data_path = LIB_PATH+"database_lib/formated_database.txt"
os.remove(data_path)
with open(data_path,'a+',encoding='gbk') as db :
    for (root,dirs,files) in os.walk(news_path) : 
        for name in files :
            if re.match(r'2016',name):
                print("ready for reading " + name)
                db.writelines(read_news(news_path + name))


    
            





