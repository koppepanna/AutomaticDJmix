# -*- encoding:utf-8 -*-
# vim:fenc=utf-8
import sys
import codecs
import csv
from xml.etree.ElementTree import *
from graphillion import GraphSet as gs
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import pyper
import networkx as nx
import pylab
from IPython import embed


file_list = [r.split('/')[-1] for r in glob.glob('*.nml')]
print file_list

#セットリストの辞書作成

rowList_b = []
rowList_a = []



for i in file_list:
    mdic = {}
    play_lists = []
    elem = parse(i).getroot()
    
    rowList1 = []
    rowList2 = []
    
    val = 0
    rowList1.append("start")
    #print rowList1[0]

    for e in elem.findall(".//ENTRY"):
        if e.get("TITLE") is not None:
            el = e.find("LOCATION")
            key = el.get("VOLUME") + el.get("DIR") + el.get("FILE")
            mdic[key] = e.get("TITLE")

    #セットリスト順にrowListに書き出し
    for e in elem.findall(".//PRIMARYKEY"):
        if e.get("KEY") is not None:
            #print mdic[e.get("KEY")]
            rowList1.append(mdic[e.get("KEY")])

    #グラフ用のデータフレーム作成
    rowList2 = list(rowList1)
    del rowList2[0]
    rowList2.append("end")
    rowList_b.extend(rowList1)
    rowList_a.extend(rowList2)


#print rowList_b[0]

df1 = pd.DataFrame({"1before" :rowList_b,
                    "2after" : rowList_a,
                   "3weight" : 1
                   })
#print df1
df1.to_csv("music_list_all.csv",index = False,encoding='utf-8',sep = "|")


#universe製作第2
#networkxからのアプローチ
"""
ai_net = nx.Graph()

for line in range(0,len(df1)):
    temp = df1.ix[line]
    #ai_net.add_edge(temp["1before"].encode('utf-8'),temp["2after"].encode('utf-8'),weight = temp["3weight"])
    ai_net.add_edge(temp["1before"],temp["2after"],weight = temp["3weight"])

for i in ai_net.nodes():
    print i

gs.converters['to_graph'] = nx.Graph
gs.converters['to_edges'] = nx.Graph.edges
#g = nx.Graph(ai_net)
gs.set_universe(ai_net)

embed()
paths = gs.paths('start','end')
print len(paths)
"""
#universe製作第2
#Rのigraphからのアプローチ
"""
r = pyper.R(use_pandas='True')
ml = pd.read_csv("music_list_all.csv")
r.assign("ml",ml)
r("library(igraph)")
r("ai.net <- graph.data.frame(ml,directed=F)")
res1 = pd.Series(r.get("ai.net"))
print res1
gs.converters['to_graph'] = res1.Graph
gs.converters['to_edges'] = res1.Graph.edges

gs.set_universe(res1.Graph)
"""

#universes製作第3
#csvからtupleを作るアプローチ
filename = "music_list_all.csv"
f = codecs.open(filename, 'r','utf-8')
lines = f.readlines()[1:]
f.close()

univ = {}
namedict = {}

for line in lines:
    dat = line.replace(",","_").split("|")
    lex = sorted([dat[0],dat[1]])
    lex = lex[0] + "|" + lex[1]
    if lex in univ:
        univ[lex] = univ[lex]+1
    else:
        univ[lex] = 1

universe = []

for name,times in univ.items():
    tmp = name.split("|")
    universe.append((tmp[0],tmp[1],times))

#universeのサイズの調整
scale_universe = universe[0:450]
gs.set_universe(scale_universe)


#node数計算の為にnetworkx利用
node_search = nx.Graph()

a = scale_universe
for d in range(len(a)):
    node_search.add_edge(a[d][0],a[d][1],wight = a[d][2])

#エッジ数、ノード数
print node_search.size()
print node_search.order()

embed()

"""
start = u"start"
end = u"end"
print "creating paths…"
paths = gs.paths(start, end)
print len(paths),"setlists"
"""
