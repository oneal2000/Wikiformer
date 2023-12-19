
import os
from tqdm import tqdm
import json
import re
import random


import argparse

parser = argparse.ArgumentParser(description="Process markdown files.")
parser.add_argument("--input_folder", required=True, help="Path to the input directory")
parser.add_argument("--output_path", required=True, help="Path to the output JSON file")
parser.add_argument("--log_path", required=True, help="Path to the error log file")


args = parser.parse_args()



cnt = 0
cnt1 = 0
cnt_error = 0
file = args.input_folder
writter = open(args.output_path,'w')
error_writter =open(args.log_path,'w')




def one_file(path):
    global cnt,cnt1,cnt_error
    with open(path,'r') as f:
        if ".DS_Store" in path:return
        txt = f.read()

        docs = txt.split('<doc')

        for doc in docs[1:]:
            out_dict = {}
            out_subtitle_list = []
            structure = []
            doc = doc.strip('</doc>\n')
            lines = doc.split('\n')
            if len(lines) < 4:
                continue

            # 存下来title
            docid = lines[0].split('\"')[1]
            title = lines[1]


            tree = []
            tree.append(title)
            top_level =1
            max_level = 0

            out_dict['title'] = title
            out_dict['docid'] = docid
            error_flag = 0
            session_list = []



            for i in range(len(lines)):
                line = lines[i]
                if not line:
                    continue
                if '#' in line.split(' ')[0]:
                    title_grade = len(line.split(' ')[0])
                    sub = ' '.join(line.split(' ')[1:])
                    structure.append((sub,i,title_grade))

            if len(structure)!=0:
                first_title = structure[0][1]
                abstract = (lines[2:first_title])
            else:
                abstract = (line[2:])

            for i in range(len(structure)):
                out_section = {}
                start = structure[i][1]
                if i !=len(structure)-1:
                    end = structure[i+1][1]
                else:
                    end = len(lines)

                subtitle = structure[i][0]
                curr_level = structure[i][2]
                if curr_level>max_level:
                    max_level=curr_level

                if curr_level==top_level:
                    tree.pop()
                    tree.append(subtitle)
                elif curr_level == top_level +1:
                    tree.append(subtitle)
                elif curr_level < top_level:
                    times = top_level - curr_level
                    for _ in range(times+1):
                        try:
                            tree.pop()
                        except:


                            error_writter.write(path + ',' + docid + '\n')
                            cnt_error += 1
                            error_flag = 1
                            break
                    tree.append(subtitle)
                else:
                    cnt_error += 1
                    error_flag = 1
                    error_writter.write(path + ',' + docid + '\n')
                    break
                top_level=curr_level
                # deep copy
                curr_tree = []
                for ___ in tree:
                    curr_tree.append(___)


                txt_ = lines[start+1:end]
                txt = ' '.join(txt_)
                out_section['subtitle'] = subtitle
                out_section['level'] = curr_level
                out_section['merged_title'] = curr_tree
                out_section['text'] = txt
                session_list.append(out_section)

            out_dict['section_list'] = session_list
            out_dict['max_level'] = max_level
            out_dict['abstract'] = abstract
            out_dict['error'] = error_flag
            if error_flag ==0:
                cnt += 1
            else:
                cnt1 += 1
            writter.write(json.dumps(out_dict) + '\n')


for root, dirs, files in os.walk(file):
    for f in (files):
        path = os.path.join(root, f)
        one_file(path)

print(cnt,cnt1,cnt_error)
