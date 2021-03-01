# -*- coding: utf-8 -*-
import codecs
import xml.etree.ElementTree as ET
import os

# tree = ET.parse('./MakaleKokleri/Biyoloji.xml')
# root = tree.getroot()

count=0
kelimeler = {}
with codecs.open('stopwords-kokleri.txt', encoding='utf-8') as f:
    for line in f:
        d = {line.strip() : 0}
        kelimeler.update(d)
f.close()

x = {}
path = './MakaleKokleri'
for filename in os.listdir(path):
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()
    varOlanKelimeler = set([])
    for metin in root:
        metin = metin.text
        metin = str(metin)
        for line, count in kelimeler.items():
            line = line.strip()
            if(' ' + line + ' ' in metin):
                kelimeler[line] += 1
                varOlanKelimeler.add(line)
    d = {filename:varOlanKelimeler}
    x.update(d)


for key,value in x.items():
    key = key.replace('.xml','')
    f = open('./DosyaStopwords/' + key + '-stopwords.txt', "a")
    f.write('Stop Word sayisi:' + str(len(value)) + '\n' + '------------' + '\n')
    for word in value:
        for kelime, count in kelimeler.items():
            if(word == kelime):
                f.write(word + '\n')
    f.close()

temizlenmisKelimeler = {}
for kelime, sayi in kelimeler.items():
        if(sayi == 0): continue
        d = {kelime:sayi}
        temizlenmisKelimeler.update(d)

with open('stopword-frekanslari.txt', "w", encoding="utf-8") as f:
    f.write('Stopwords sayisi: ' + str(len(temizlenmisKelimeler)))
    f.write('\n------------\n')
    for kelime,sayi in temizlenmisKelimeler.items():
        f.write(kelime + ': ' + str(sayi) + '\n')
f.close()
    

