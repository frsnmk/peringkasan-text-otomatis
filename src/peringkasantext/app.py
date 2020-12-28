"""
Aplikasi Peringkasan Text Otomatis menggunakan metode CLSA
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class PeringkasanText(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style = Pack(direction = COLUMN, padding = (25,25,25,25)))
        # scrollable_box = toga.ScrollContainer(vertical = True, horizontal = False, content = main_box)

        #create text input for content
        label_content = toga.Label('Isi Berita :', style=Pack(padding_bottom=5))
        main_box.add(label_content)
        self.content = toga.MultilineTextInput(style = Pack(flex=1))
        main_box.add(self.content)

        #create slider for rate compression
        label_rate_compression = toga.Label('Tingkat Peringkasan :  ', style=Pack(padding_top=25))
        main_box.add(label_rate_compression)
        self.rate_compression = toga.Slider(range = (0,10), tick_count = 11)
        main_box.add(self.rate_compression)

        #create button
        button_sum = toga.Button('Ringkas Data', on_press=self.summarize_data, style=Pack(padding_bottom=25))
        main_box.add(button_sum)

        #result of summarize
        label_result_content = toga.Label('Hasil Ringkasan: ', style=Pack(padding_bottom=5))
        main_box.add(label_result_content)
        self.result_content = toga.MultilineTextInput(style = Pack(flex=1))
        main_box.add(self.result_content)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def summarize_data(self, widget):
        ts = TextSummarization(self.content.value, int(self.rate_compression.value)*10)
        ts.stemming
        ts.cleaning
        ts.removeStopword
        ts.getSentence
        ts.getWord
        ts.tfIdf
        ts.lsa
        self.result_content.value = ts.lsa
        # self.result_content.value = int(self.rate_compression.value)*10
        # self.result_content.value = self.content.value


def main():
    return PeringkasanText()


##Text summarization package by frsnmk

import re, string, unicodedata  #modul regular expression
import nltk
from nltk import word_tokenize, sent_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import numpy as np
import math
from math import log

class TextSummarization:
    def __init__(self, data, tingkat_peringkasan):
        self.data = data
        self.data = sent_tokenize(self.data)
        self.tingkat_peringkasan = tingkat_peringkasan
        
    @property   
    def stemming(self):
        # membuat stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        self.stemming_result = [stemmer.stem(sentence) for sentence in self.data]
        return self.stemming_result

    @property
    def cleaning(self):
        self.cleaning_result = []
        for sub_stemming_result in self.stemming_result:
            #remove non-ascii
            sub_stemming_result = unicodedata.normalize('NFKD', sub_stemming_result).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            #remove URLs
            sub_stemming_result = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', sub_stemming_result)
            #remove punctuations
            sub_stemming_result = re.sub(r'[^\w]|_',' ', sub_stemming_result)
            #remove digit from string
            sub_stemming_result = re.sub("\S*\d\S*", "", sub_stemming_result).strip()
            #remove digit or numbers
            sub_stemming_result = re.sub(r"\b\d+\b", " ", sub_stemming_result)
            #to lowercase
            sub_stemming_result = sub_stemming_result.lower()
            #Remove additional white spaces
            sub_stemming_result = re.sub('[\s]+', ' ',sub_stemming_result)
            self.cleaning_result.append(sub_stemming_result)            
        return self.cleaning_result
    @property
    def removeStopword(self):
        f = open('stopwordFile', 'r')
        if f.mode == 'r':
            contents =f.read()
        stopword = contents.split('\n')
        stopword = set(stopword)
        self.remove_stopword_result = []
        for sub_cleaning_result in self.cleaning_result:
            word_tokens = word_tokenize(sub_cleaning_result)
            self.filtered_sentence = [w for w in word_tokens if not w in stopword]
            self.new_filtered_sentence = [a for a in self.filtered_sentence]
            self.remove_stopword_result.append(self.new_filtered_sentence)
        return self.remove_stopword_result
    @property
    def getSentence(self):
        self.kalimat = list(filter(None, self.remove_stopword_result))
        return self.kalimat
    @property
    def getWord(self):
        self.kata = [elem for sublist in self.kalimat for elem in sublist]
        self.kata = set(self.kata)
        self.kata = list(self.kata)
        self.kata.sort()
        return self.kata
    @property
    def tfIdf(self):    
        # mencari nilai tf
        listTf=[[sum(1 for k in j if(k==i)) for j in self.kalimat] for i in self.kata]

        # mencari nilai df
        listDf = [sum(1 for m in l if(m >=1)) for l in listTf]  

        #mencari nilai idf
        listIdf = [log(len(self.kalimat)/n,10)for n in listDf]

        # mencari nilai tf-idf
        self.listTfIdf = [[q*p for q in o]for o, p in zip(listTf, listIdf)]

        return self.listTfIdf
    
    
    @property
    def lsa(self):
        U, S, v = np.linalg.svd(self.listTfIdf, full_matrices=False)
        vt=np.transpose(v)
        newVt = []
        for r in vt:
            tampungLagi = []
            for s in r:
                if (s < np.mean(r)):
                    s = 0
                tampungLagi.append(s)
            newVt.append(tampungLagi)
    # menggunakan fungsi menghitung lenght
        sigmaVt=[]
        for a in newVt:
            c=[]
            for b in a:
                c.append(b**2)
            sigmaA= sum(c)
            sigmaVt.append(sigmaA)
        resultLenght = []
        for d, e in zip(sigmaVt, S):
            f = d*e
            f = math.sqrt(f)
            resultLenght.append(f)
       #sorting dari lenght terbersasr tanpa menghilngkan index 
        listDua = sorted(resultLenght, reverse = True) 
        listAcak =[]
        for a in listDua:
            i = 0
            for b in resultLenght:
                if(a==b):
                    listAcak.append(i)
                i+=1
        rc = round(len(self.data)*((100-self.tingkat_peringkasan)/100))
        indexLenghtDoc = listAcak[:rc] #jumlah Kalimat yang ingin ditampilkan
        indexLenghtDoc.sort()
        ringkasan = [self.data[u] for u in indexLenghtDoc]
        ringkasan = ' '.join(ringkasan)
        
        return ringkasan
