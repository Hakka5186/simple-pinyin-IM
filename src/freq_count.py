#数据学习
import re
import json
from matplotlib.pyplot import text
from tqdm import tqdm
from filepath import LIB_PATH,MID_PATH

#读取一二级汉字，做成矩阵
char_map = {} #某字单独出现的频率,包括总频率和句首频率
pair_map = {} #两字连续出现的频率

print("init char map")
with open(LIB_PATH+"spell2char/full_char_list.txt","r",encoding="gbk") as f:
    char_str = f.read()
    for i in char_str:
        char_map[i] = {"head":0 , "count":0}

print("build up char&pair maps")
total = 0
with open(LIB_PATH+"database_lib/formated_database.txt") as f:
    data = f.read().splitlines()
    bef_char = ""
    #学习语料
    print("leaning sentences")
    for sentence in tqdm(data):
        if not sentence:continue
        #识别句首的字
        total += len(sentence)
        if sentence[0] in char_map:
            char_map[sentence[0]]["head"] += 1
            char_map[sentence[0]]["count"] += 1
            bef_char = sentence[0]
        for char in sentence[1:]:
            if char in char_map:
                char_map[char]["count"] += 1
                if bef_char : 
                    pair = bef_char+char
                    if pair in pair_map : pair_map[bef_char+char] += 1
                    else : pair_map[bef_char+char] = 1
                bef_char = char 
char_map["total"] = total
#读取拼音表，做成spell_map
print("build up spell map")
spell_map = {}
with open(LIB_PATH+"spell2char/spell2char_list.txt","r",encoding="gbk") as f:
    spell_list = f.read().splitlines()
    for line in spell_list:
        spell = re.split(r'[ ]',line)
        spell_map[spell[0]] = spell[1:]

print("save in json style")
#将预处理好的map以json文件形式存档
json_str = json.dumps(char_map,ensure_ascii=False)
with open(MID_PATH+'char_map.json', 'w') as json_file:
    json_file.write(json_str)
json_str = json.dumps(pair_map,ensure_ascii=False)
with open(MID_PATH+'pair_map.json', 'w') as json_file:
    json_file.write(json_str)
json_str = json.dumps(spell_map,ensure_ascii=False)
with open(MID_PATH+'spell_map.json', 'w') as json_file:
    json_file.write(json_str)






