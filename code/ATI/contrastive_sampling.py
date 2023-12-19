import json
from tqdm import tqdm

writer = open('./ATI.json','w')
cnt,cnt1 = 0,0
cnt2,cnt3 = 0,0
with open('./output.json') as f:
    lines = f.read().split('\n')
    for line in tqdm(lines):
        if not line:break
        tmp = json.loads(line)
        abstract = tmp['abstract']
        title = tmp['title']
        if type(abstract) is list:
            out_dict = {}
            out_dict['title'] = title
            abstract = ' '.join(abstract[1:])
            out_dict['abstract'] = abstract

            negs = []

            sections = tmp['section_list']
            for sec in sections:
                negs.append(sec['text'])

            out_dict['negs'] = negs
            writer.write(json.dumps(out_dict) + '\n')



