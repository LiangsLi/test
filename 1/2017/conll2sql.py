# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:15:06 2017

@author: Liangs
"""
#这里把1000句话拆成10份，每份annotator不同，
#这样用不同的账号登陆时将被分配给对应任务。此外也是因为1000句sql语句同时上传的时候太卡，拆分之后就快很多。
def output(sents, begin, end, outfile, user):
    annotator = user
    sql = "insert into dependancy(sentid,sent,dep_sent,annoter) values"
    i = begin
    raw_sent = ' '.join(['[' + str(id) + ']' + tok[0] + '/' + tok[1] for id, tok in enumerate(sents[begin])])
    sql += "('" + str(i) + "','" + raw_sent + "','"
    rels = "\t\t".join(['['+str(tok[2])+']'+sents[begin][tok[2]][0]+'_['+str(id+1)+']'+tok[0]+'('+tok[3]+')' for id, tok in enumerate(sents[begin][1:]) ])
    sql += rels + "','"+annotator+"')"
    i += 1
    for sent in sents[begin+1:end+1]:
        raw_sent = ' '.join(['[' + str(id) + ']' + tok[0] + '/' + tok[1] for id, tok in enumerate(sent)])
        sql += ",\n('" + str(i) + "','" + raw_sent + "','"
        rels = "\t\t".join(['['+str(tok[2])+']'+sent[0][0]+'_['+str(id+1)+']'+tok[0]+'('+tok[3]+')' for id, tok in enumerate(sent[1:]) ])
        sql += rels + "','"+annotator+"')"
        i += 1
    fo = open(outfile,"a")
    sql+="\n"
    fo.write(sql)
    fo.close()
    
fi = open("f:/test.txt","r",encoding='UTF-8')
fi = fi.read()
sents = fi.strip().split("\n\n")
print ("total sents: ",len(sents))
sentences = []
n = 0
for sent in sents:
    sentences.append([])
    sentences                         [n].append(("Root", "Root", -1, "-NULL-"))
    lines = sent.strip().split("\n")
    for line in lines:
        items = line.strip().split("\t")
        sentences[n].append((items[1], items[3], int(items[6]), items[7]))
    n += 1
i=0
while(i*100<len(sentences)):
    if (i*100+99)<len(sentences):
        output(sentences, i*100, i*100+99, "daoru4.sql", "user"+str(i))
       # print(1)
    else:
        output(sentences, i*100, len(sentences)-1, "daoru4.sql", "user"+str(i))
       # print(2)
    i+=1
    
