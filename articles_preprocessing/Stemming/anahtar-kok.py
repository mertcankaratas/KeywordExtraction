import os
import re
import nltk
nltk.download("punkt")
import xml.etree.ElementTree as ET
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
ZEMBEREK_PATH = 'zemberek-full.jar'
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))


TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

path = './Makaleler'
for filename in os.listdir(path):
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()
    data = ET.Element('data')
    for anahtar in root:
        anahtar = anahtar.find('Anahtar').text
        anahtar = str(anahtar)
        kelimeler = nltk.word_tokenize(anahtar)
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
        eklenecek_kelimeler = ''
        anahtar_kelimeler = set()
        anahtar = ET.SubElement(data, 'Anahtar')
        for i in pos:
            anahtar_kelimeler.add(i.strip().lower())
        for y in anahtar_kelimeler:
            eklenecek_kelimeler+=y + ','
        anahtar.text = str(eklenecek_kelimeler)                     
    

    tree = ET.ElementTree(data)
    tree.write('./anahtar_kokleri/' + filename,encoding="UTF-8",xml_declaration=True)