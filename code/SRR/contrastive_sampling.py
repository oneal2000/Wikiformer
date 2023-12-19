import json
from tqdm import tqdm
import copy
import random
from transformers import AutoTokenizer
import re

dataset ='./output.json'
writter = open('./SRR.json','w')


cnt = 0
cnt4 = 0
cnt8 = 0
cnt16 = 0
cnt32 = 0
num_neg = 8



with open(dataset) as f:
    for __ in tqdm(range(6397126+1)):
        line = f.readline()
        if not line:break
        tree = json.loads(line)
        max_level = tree['max_level']


        if len(tree['section_list'])>5:
            section_list = copy.deepcopy(tree['section_list'])
            pos = {}

            long_section_list = []

            for sc in section_list:
                txt = sc['text']
                sp = re.split('[ ,.?!，。？！()/\n\"]', txt)
                words = list(filter(None, sp))
                if len(words) > 20:

                    long_section_list.append(sc)

            if len(long_section_list) < 4:
                continue


            break_flag = 1
            for section in long_section_list:
                pos = section
                if (section['level'] == max_level or section['level'] == max_level-1) and len(section['text']) > 20:
                    long_section_list.remove(section)
                    break_flag = 0
                    break
            if break_flag == 1:
                continue


            for sc in long_section_list:
                if len(sc['text']) < 20 or sc==pos:
                    print(sc)
                    long_section_list.remove(sc)

            negs = long_section_list


            if len(negs)<3:
                continue

            pos_list = pos['merged_title']
            qry = ' '.join(pos_list)


            pos_txt = pos['text']
            out_dict = {}
            out_dict['qry'] = qry
            out_dict['pos'] = pos_txt
            out_dict['neg'] = negs
            writter.write(json.dumps(out_dict) + '\n')

