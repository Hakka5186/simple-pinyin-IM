import numpy as np
import math
import json
from tqdm import trange
from tqdm import tqdm
import difflib
from filepath import LIB_PATH,MID_PATH,DATA_PATH

#读取json文件中的几个表格
print("read file for map init")
char_map = {}
char_str = ""
pair_map = {}
spell_map = {}
with open(MID_PATH+'char_map.json', 'r') as json_file:
    json_str = json_file.read()
    char_map = json.loads(json_str)
with open(MID_PATH+'pair_map.json', 'r') as json_file:
    json_str = json_file.read()
    pair_map = json.loads(json_str)
with open(LIB_PATH+"spell2char/full_char_list.txt","r",encoding="gbk") as f:
    char_str = f.read()
with open(MID_PATH+'spell_map.json', 'r') as json_file:
    json_str = json_file.read()
    spell_map = json.loads(json_str)


#初始化每个字的出现概率
head_p_map = {}
p_map = {}
#加点平滑度
HEAD_SMOOTHEN = 1/100
PAIR_SMOOTHEN = 1/100000
print("calculating percentage of a char at head of sentence")
for char in tqdm(char_str):
    p_map[char] = char_map[char]["count"]/char_map["total"]
    p_head = char_map[char]["head"]/char_map["total"]
    head_p_map[char] = (1-HEAD_SMOOTHEN)*p_head + HEAD_SMOOTHEN * p_map[char]

def translate(input : list):
    #viterbi算法
    prefix_list = []#已确定的最小前缀串
    pre_char_list = []#i-1位置拼音对应的字符list
    pre_q_list = []#Qi-1
    #初始化第一条
    if input[0] in spell_map:
        char_list = spell_map[input[0]]
        pre_q_list = [ math.inf if (not head_p_map[char]) else -math.log(head_p_map[char]) for char in char_list]
        pre_char_list = char_list
        prefix_list = char_list
    else: 
        return "error"
    for spell in input[1:] : 
        if spell not in spell_map:
            #print(spell)
            continue
        char_list = spell_map[spell]
        min_q_list = []
        min_pre_list = []
        for char in char_list :
            q_list = []
            for i in range(0,len(pre_char_list)):
                pair = pre_char_list[i]+char
                pair_count = pair_map.get(pair,0)
                pre_count = char_map[pre_char_list[i]]["count"]
                #如果precount直接是零的话就砍掉这条路叭
                if pre_count == 0 :
                    q_list.append(math.inf)
                    continue
                #平滑化概率
                smoothen_p = (1-PAIR_SMOOTHEN)*(pair_count/pre_count) + PAIR_SMOOTHEN * p_map[char]
                #计算边权
                d = math.inf if (not smoothen_p) else -math.log(smoothen_p)
                q_list.append(d + pre_q_list[i])
            min_pl = np.argmin(np.array(q_list))
            min_q_list.append(q_list[min_pl])
            min_pre_list.append(prefix_list[min_pl]+char)
        pre_q_list = min_q_list
        pre_char_list = char_list
        prefix_list = min_pre_list
    res_pl = np.argmin(np.array(pre_q_list))
    res = prefix_list[res_pl]
    return res

input = []
std_output = []
with open(DATA_PATH+"input.txt") as f:
    input = f.read().splitlines()
with open(DATA_PATH+"std_output.txt" , encoding="gbk") as f:
    std_output = f.read().splitlines()

perc = 0
full_match = 0
with open(DATA_PATH+"output.txt","w") as out :
    with open(DATA_PATH+"result.txt","w") as f :
        for i in trange(len(input)) :
            print("拼音输入："+input[i],file=f)
            spell_list = input[i].replace("\t","").split(" ")
            output = translate(spell_list)
            print(output,file=out)
            single_perc = difflib.SequenceMatcher(None,output,std_output[i]).ratio()
            print("我的输出："+output,file=f)
            print("标准输出："+std_output[i] + ",句子匹配度"+str(single_perc),file=f)
            print("--------------------------------------",file = f)
            perc += single_perc
            if single_perc == 1.0:
                full_match += 1
        print("总匹配度:"+str(perc/len(input)))
        print("整句匹配度:"+str(full_match/len(input)))


            
