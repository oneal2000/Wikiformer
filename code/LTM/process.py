import json
from tqdm import tqdm
id_title = {}
title_id = {}
cnt_error = 0
with open('https://dumps.wikimedia.org/enwiki/latest/enwiki-20220101-pages-articles-multistream.xml') as f:
    print()
    txt = f.read()
    sections = txt.split('<page>')
    print(len(sections))  # 21726008
    for sec in tqdm(sections[1:len(sections)-1]):
        sa = []
        lines = sec.split('\n')
        title = 'null'
        see_also = 0
        for i in range(1,len(lines)):
            line = lines[i]
            if '<id>' in line:
                id = int(line.strip('    <id>').strip('</id>'))
            if '<title>' in line:
                title = line.strip('<title>').strip('</title>')
                title = title.strip('    <title>')
            if '==See also==' in line:
                see_also = i
                break
        if title != 'null':
            id_title[id] = title
            title_id[title] = id
        if title == 'null':
            cnt_error = 1
            continue
        for i in range(see_also+1,len(lines)):
            if '==' in lines[i]:
                break
            if '* [[' in lines[i]:
                sa.append(lines[i].split(']]')[0].strip('* [['))
        writer.write(title + '\t' + json.dumps(sa) + '\n')


dict_id_title = open('./dict_id_title','w')
dict_id_title.write(json.dumps(id_title))

dict_title_id = open('./dict_title_id','w')
dict_title_id.write(json.dumps(title_id))

print(cnt_error)