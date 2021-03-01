import codecs
import xml.etree.ElementTree as ET
import numpy as np
import os

# Read stopwords
stopwords = []
with codecs.open('stopwords-kokleri.txt', encoding='utf-8') as f:
    for line in f:
        stopwords.append(line.strip())
f.close()

docs = [
]
# Read each articles summary part
# And normalize them
path = './summaries_stemmed'
for filename in os.listdir(path):
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()
    data = ET.Element('data')
    for ozetce in root:
        kelimeler = []
        ozetce = ozetce.text
        ozetce = str(ozetce)
        docs.append(ozetce)
        # Filter the ozetce list based on stopwords list
        stopwords_filtered = [x for x in ozetce.split(' ') if
                all(y.lower() != x.lower() and x != '' for y in stopwords)]
        # Filter single letters
        singleLenFilter = ''
        for word in stopwords_filtered:
            if len(word) > 1:
                singleLenFilter = singleLenFilter + ' ' + word
        ozetce = ET.SubElement(data, 'Özetçe')
        ozetce.text = str(singleLenFilter)
        # create a new XML file with the results

    tree = ET.ElementTree(data)
    tree.write('./stopwords_filtered/' + filename,encoding="UTF-8",xml_declaration=True)


