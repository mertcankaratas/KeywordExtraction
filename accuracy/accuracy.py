import codecs
import os
import pandas as pd
import xml.etree.ElementTree as ET
import csv
from sklearn.metrics import classification_report
path = './keywords_stemmed'
total_articles=0
total_accuracy_of_articles=0
for fileName in os.listdir(path):
    total_articles+=1
    actual_keywords = []
    print(fileName)
    fileName=fileName.replace('.xml','')
    path = 'keywords_stemmed/' + fileName + '.xml'
    tree = ET.parse(path)
    root = tree.getroot()
    for anahtar in root:
        kelimeler = []
        anahtar = anahtar.text
        anahtar = str(anahtar)
        for i in anahtar.split(','):
            if(i != ''):
                kelimeler.append(i)
        actual_keywords.append(kelimeler)

    extracted_keywords = {}
    with open('extracted_keywords/key-'+fileName+'.csv', mode='r') as f:
        reader = csv.reader(f, delimiter=',') 
        for n, row in enumerate(reader):
            article_index, keyword, length = row
            if article_index not in extracted_keywords:
                extracted_keywords[article_index] = list()
            extracted_keywords[article_index].append((keyword))
    total_accuracy = 0
    total_count = 0
    f = open('./accuracy/' + fileName + '.txt', "a")
    for index,item in enumerate(actual_keywords):
        f.write('Article Index: ' + str(index+1))
        f.write('\n')
        f.write('Actual: ' + str(item))
        f.write('\n')
        if(extracted_keywords[str(index)]):
            key = extracted_keywords[str(index)]
            f.write('Extracted: '+ str(key))
            f.write('\n')
            accuracy=0
            TP=0
            TN=0
            FP=0
            FN=0
            for predicted in key:
                if predicted in item:
                    TP+=1
                elif predicted not in item:
                    FN+=1
            for actual in item:
                if actual not in key:
                    FP+=1
            accuracy = (TP + TN)/(TP + TN + FP + FN)
            total_accuracy+=accuracy
            total_count+=1
            f.write('TP: '+ str(TP) + ' TN: ' + str(TN) +
            ' FP: ' + str(FP)+ ' FN: ' + str(FN) + 
            ' \nAccuracy: %' + str(accuracy*100))
            f.write('\n')
            f.write('-----------------\n')
    
    f.write('Total accuracy of document "'+fileName+'" is: %'+str((total_accuracy/total_count)*100))
    print(total_accuracy/total_count)
    total_accuracy_of_articles+=(total_accuracy/total_count)
    f.close()

f = open('./total_accuracy/total.txt', "a")
print(total_articles)
print(total_accuracy_of_articles)
f.write('Total accuracy of the keyword extraction system (on all the articles) is %' + str((total_accuracy_of_articles/total_articles)*100))
f.close()