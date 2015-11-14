# -*- encoding:utf-8 -*-
import sys
import csv
from xml.etree.ElementTree import *
import codecs
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
import numpy as np

#セットリストの辞書作成
mdic = {}
play_lists = []
elem = parse("anisondisco201505.nml").getroot()

val = 0
rowList = []
rowList.append("start")
print rowList[0]

for e in elem.findall(".//ENTRY"):
    if e.get("TITLE") is not None:
        el = e.find("LOCATION")
        key = el.get("VOLUME") + el.get("DIR") + el.get("FILE")
        mdic[key] = e.get("TITLE").encode('utf-8')

#セットリスト順にrowListに書き出し
for e in elem.findall(".//PRIMARYKEY"):
    if e.get("KEY") is not None:
        print mdic[e.get("KEY")]
        rowList.append(mdic[e.get("KEY")])

#グラフ用のデータフレーム作成
rowList2 = list(rowList)
del rowList2[0]
rowList2.append("end")

print rowList[0]

df1 = pd.DataFrame({"1before" :rowList,
                    "2after" : rowList2
                 })
print df1
df1.to_csv("music_list.csv",index = False)
