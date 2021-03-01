
import os
import codecs
import re
# import nltk
# nltk.download("punkt")
import xml.etree.ElementTree as ET
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
ZEMBEREK_PATH = './zemberek-full.jar'
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))


TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

yeni_kelimeler = []
with codecs.open('turkish-stopwords.txt', encoding='utf-8') as f:
    for line in f:
        yeni_kelimeler.append(line.strip())
f.close()

# path = './Stopwords filtrelenmesi/Makaleler/Biyoloji.xml'
# tree = ET.parse(path)
# root = tree.getroot()
# varOlanKelimeler = set([])
# ozetce = root[0].find('Özetçe').text
# ozetce = str(ozetce)
# kelimeler = nltk.word_tokenize(ozetce)
# yeni_kelimeler= [kelimeler for kelimeler in kelimeler if kelimeler.isalnum()]

pos: List[str] = []
for kelime in yeni_kelimeler:
    analysis: java.util.ArrayList = (
        morphology.analyzeAndDisambiguate(kelime).bestAnalysis()
        )
    for i, analysis in enumerate(analysis, start=1):
        if "UNK" in str(analysis.getDictionaryItem()):
            pos.append(kelime)

        else:
            pos.append(
                str(analysis.getDictionaryItem())
                )
temizlenmis = set()
for i in pos:
   i=re.sub(r'\[(.*)\]', '', i)
   temizlenmis.add(i)



with open('stopwords-kokleri.txt', "w", encoding="utf-8") as f:
    for i in sorted(temizlenmis):
        f.write(i)
        f.write('\n')
f.close()