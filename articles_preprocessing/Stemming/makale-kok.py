
import os
import re
import nltk
nltk.download("punkt")
import xml.etree.ElementTree as ET
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
ZEMBEREK_PATH = './zemberek-full.jar'
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))


TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

path = './Makaleler'
for filename in os.listdir(path):
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()
    for ozetce in root:
        ozetce = ozetce.find('Özetçe').text
        ozetce = str(ozetce)
        kelimeler = nltk.word_tokenize(ozetce)
        yeni_kelimeler= [kelimeler for kelimeler in kelimeler if kelimeler.isalnum()]

        pos: List[str] = []
        for kelime in yeni_kelimeler:
            analysis: java.util.ArrayList = (
                morphology.analyzeAndDisambiguate(kelime).bestAnalysis()
                )
            for i, analysis in enumerate(analysis, start=1):
                if "UNK" in str(analysis.getDictionaryItem()):
                    pos.append(' ' + kelime + ' ')

                else:
                    kok = str(analysis.getDictionaryItem())
                    kok = re.sub(r'\[(.*)\]', '', kok)
                    pos.append(
                        kok
                        )
        with open('./MakaleKokleri2/' + filename, "a", encoding="utf-8") as f:
            f.write('<Özetçe> ')
            for i in pos:
                f.write(i+ '')
            f.write(' </Özetçe>')
            f.write('\n')
            f.write('\n')
        f.close()