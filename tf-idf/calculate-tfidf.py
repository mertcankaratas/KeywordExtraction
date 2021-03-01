import re
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import csv 
import os
pd.options.display.max_colwidth = 8000

docs = [
]

def norm_doc(single_doc):
    # EN: Remove special characters and numbers
    single_doc = single_doc.strip()
    single_doc = re.sub(" \d+", " ", single_doc)
    pattern = r"[{}]".format(",.;") 
    single_doc = re.sub(pattern, "", single_doc) 
    # EN: Convert document to lowercase
    single_doc = single_doc.lower()
    single_doc = single_doc.strip()
    # EN: Tokenize documents
    tokens = WPT.tokenize(single_doc)
    single_doc = ' '.join(tokens)
    return single_doc

def calculateDictAverage(target,iterationCount):
    if iterationCount>=0:
        result = sum(target.values()) / len(target)
        for j in range(len(target)):
            for k,v in target.items():
                if v < result:
                    del target[k]
                    break            
        
        return calculateDictAverage(target,iterationCount-1)
    else:
        if(len(target)>=10):
            calculateDictAverage(target,1)
        return target     

def dictToCsv(data):
    with open('./extracted_keywords/key-' + filename,'a+') as fd:
        
        for i in range(len(data)):
            dictResult=calculateDictAverage(res.loc[i].to_dict(),2)
            
            writer = csv.writer(fd)
            for key, value in dictResult.items():
                writer.writerow([i,key, value])
    fd.close()  

path = './stopwords_filtered'
i = 0

for filename in os.listdir(path):
    docs = []
    i+=1
    fullname = os.path.join(path, filename)
    print(fullname)
    tree = ET.parse(fullname)
    root = tree.getroot()
    for ozetce in root:
        ozetce = ozetce.text
        ozetce = str(ozetce)
        docs.append(ozetce)

    WPT = nltk.WordPunctTokenizer()

    norm_docs = np.vectorize(norm_doc) #like magic :)
    normalized_documents = norm_docs(docs)

    from sklearn.feature_extraction.text import CountVectorizer
    BoW_Vector = CountVectorizer(min_df = 0., max_df = 1.)
    BoW_Matrix = BoW_Vector.fit_transform(normalized_documents)
    #print (BoW_Matrix)

    # TR: BoW_Vector içerisindeki tüm öznitelikleri al
    # EN: Fetch al features in BoW_Vector
    features = BoW_Vector.get_feature_names()

    BoW_Matrix = BoW_Matrix.toarray()
    # TR: Doküman - öznitelik matrisini göster
    # EN: Print document by term matrice
    BoW_df = pd.DataFrame(BoW_Matrix, columns = features)
    BoW_df
    filename = filename.replace('.xml', '')

    from sklearn.feature_extraction.text import TfidfVectorizer
    Tfidf_Vector = TfidfVectorizer(min_df = 0., max_df = 1., use_idf = True)
    Tfidf_Matrix = Tfidf_Vector.fit_transform(normalized_documents)
    Tfidf_Matrix = Tfidf_Matrix.toarray()
    # TR: Tfidf_Vector içerisindeki tüm öznitelikleri al
    # EN: Fetch al features in Tfidf_Vector
    features = Tfidf_Vector.get_feature_names()
    # TR: Doküman - öznitelik matrisini göster
    # EN: Print document by term matrice
    Tfidf_df = pd.DataFrame(np.round(Tfidf_Matrix, 3), columns = features)
    Tfidf_df
    

    Tfidf_df.loc[:, (Tfidf_df != 0).any(axis=0)].to_csv("./all-tf-idf/" +filename , encoding='utf-8', index=True)
    cols = Tfidf_df.columns
    bt = Tfidf_df.apply(lambda x: x > 0)
    res = Tfidf_df[Tfidf_df!=0].stack()

    data=pd.read_csv("./all-tf-idf/" +filename)

    dictToCsv(data)



