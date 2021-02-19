import json
import glob
import nltk
from nltk.tokenize import sent_tokenize
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
import string
import math


######################IMPORT DOCUMENTI
doc_url = "/Users/aldo/Desktop/Dev/Python/BBC News Summary/News Articles/"
business_url = doc_url+"business/*.txt"
entertainment_url = doc_url+"entertainment/*.txt"
politics_url = doc_url+"politics/*.txt"
sport_url = doc_url+"sport/*.txt"
tech_url = doc_url+"tech/*.txt"

def retrieve_docs(url):
    docs = []
    file_list = glob.glob(url)
    for file_path in file_list:
        with open(file_path, 'r', encoding='ISO-8859-1') as file_input:
            #print(file_path)
            docs.append(file_input.read())
    return docs

business = retrieve_docs(business_url)
entertainment = retrieve_docs(entertainment_url)
politics = retrieve_docs(politics_url)
sport = retrieve_docs(sport_url)
tech = retrieve_docs(tech_url)

##############################PREPROCESSING
def preprocessing(docs):
    returned_docs = []
    for doc in docs:
        #lowercase
        doc = doc.lower()
        #remove punctuation
        text_p = "".join([char for char in doc if char not in string.punctuation])
        #tokenization
        words = word_tokenize(text_p)
        #remove stopwords
        stop_words = stopwords.words('english')
        filtered_words = [word for word in words if word not in stop_words]
        #stemming
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in filtered_words]
        returned_docs.append(stemmed)
    return returned_docs

bus_pre = preprocessing(business)

###########################CALCOLO TF-IDF PER CATEGORIA
def tf_score(docs):
    freq = []
    for doc in docs:
        freq_table = {}
        for word in doc:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1
        freq.append(freq_table)
    for doc in freq:
        for word in doc:
            doc[word] = 1 + math.log2(doc[word])
    return freq

def idf_score(docs):
    N = len(docs)
    freq_table = {}
    for doc in docs:
        found = False
        for word in doc:
            if (word in freq_table and found == False):
                found = True
                freq_table[word] += 1
            elif (word in freq_table and found == True):
                continue
            else: freq_table[word] = 1
    for word in freq_table:
        freq_table[word] = math.log2(N/freq_table[word])
    return freq_table

tf = tf_score(bus_pre)
idf = idf_score(bus_pre)

tf_idf = []
for doc in tf:
    tf_idf_temp = {}
    for word in doc:
        tf_idf_temp[word] = doc[word]*idf[word]
    tf_idf.append(tf_idf_temp)

print (tf_idf)


######################ESTRAZIONE FRASI
def extract_sentences(doc_collection):
    sentences = []
    for doc in doc_collection:
        temp = sent_tokenize(doc)
        temp[0] = temp[0].replace('\n\n', '.\n\n')
        temp1 = sent_tokenize(temp[0])
        del temp[0]
        if len(temp1)>1:
            temp.insert(0,temp1[1])
        #matrice di frasi: ogni riga è un documento e ogni colonna è una frase, es prova[0][3] restituisce la terza frase del primo documento
        sentences.append(temp)
        # #vettore di frasi
        # for sent in temp:
        #    sentences.append(sent)
    return sentences


business_sent = extract_sentences(business)
#testS = business_sent[0]
sentences = []
for testS in business_sent:
    sentences.append(preprocessing(testS))

def calculate_score(sentence, tfidf_score):
    score = 0
    for word in sentence:
        score = score + tfidf_score[word]
    return score

scores = []
for i in range(len(sentences[0])):
    scores.append(calculate_score(sentences[0][i], tf_idf[0]))

print(scores)

scoresMax = scores.copy()
max7 = []
for i in range(7):
    max = 0
    for score in scoresMax:
        if score > max:
            max = score;
    max7.append(max)
    scoresMax.remove(max)

# print(scores)
# print(max7)
# for score in max7:
#     print(scores.index(score))
# print(business_sent[0])
for score in max7:
    print(business_sent[0][scores.index(score)])

# #lowercase
# testS = testS.lower()
# #remove punctuation
# text_p = "".join([char for char in testS if char not in string.punctuation])
# #tokenization
# words = word_tokenize(text_p)
# #remove stopwords
# stop_words = stopwords.words('english')
# filtered_words = [word for word in words if word not in stop_words]
# #stemming
# porter = PorterStemmer()
# stemmed = [porter.stem(word) for word in filtered_words]
# testS = stemmed
#
# print(testS)




# entertainment_sent = extract_sentences(entertainment)
# politics_sent = extract_sentences(politics)
# sport_sent = extract_sentences(sport)
# tech_sent = extract_sentences(tech)
# #SCORE FRASI
