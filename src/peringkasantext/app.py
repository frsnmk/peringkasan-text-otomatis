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
        # f = open('stopwordFile', 'r')
        # if f.mode == 'r':
        #     contents =f.read()
        # stopword = contents.split('\n')
        stopword = ["ada","adanya","adalah","adapun","agak","agaknya","agar","akan","akankah","akhirnya","aku","akulah","amat","amatlah","anda","andalah","antar","diantaranya","antara","antaranya","diantara","apa","apaan","mengapa","apabila","apakah","apalagi","apatah","atau","ataukah","ataupun","bagai","bagaikan","sebagai","sebagainya","bagaimana","bagaimanapun","sebagaimana","bagaimanakah","bagi","bahkan","bahwa","bahwasanya","sebaliknya","banyak","sebanyak","beberapa","seberapa","begini","beginian","beginikah","beginilah","sebegini","begitu","begitukah","begitulah","begitupun","sebegitu","belum","belumlah","sebelum","sebelumnya","sebenarnya","berapa","berapakah","berapalah","berapapun","betulkah","sebetulnya","biasa","biasanya","bila","bilakah","bisakah","sebisanya","boleh","bolehkah","bolehlah","buat","bukan","bukankah","bukanlah","bukannya","dahulu","dalam","dan","dari","daripada","demikian","demikianlah","sedemikian","dengan","di","dia","dialah","dini","diri","dirinya","terdiri","dong","dulu","enggak","enggaknya","entah","entahlah","terhadap","terhadapnya","hal","hampir","hanya","hanyalah","harus","haruslah","harusnya","seharusnya","hendak","hendaklah","hendaknya","hingga","sehingga","ia","ialah","ibarat","ingin","inginkah","inginkan","ini","inikah","inilah","itu","itukah","itulah","jangan","jangankan","janganlah","jika","jikalau","juga","justru","kala","kalau","kalaulah","kalaupun","kalian","kami","kamilah","kamu","kamulah","kan","kapan","kapankah","kapanpun","dikarenakan","karena","karenanya","ke","kemudian","kenapa","kepada","kepadanya","ketika","seketika","khususnya","kini","kinilah","kiranya","sekiranya","kita","kitalah","kok","lagi","lagian","selagi","lah","lain","lainnya","melainkan","selaku","lalu","melalui","terlalu","lama","lamanya","selama","selama","selamanya","lebih","terlebih","bermacam","macam","semacam","maka","makanya","makin","malah","malahan","mampu","mampukah","mana","manakala","manalagi","masih","masihkah","semasih","masing","mau","maupun","semaunya","memang","mereka","merekalah","meski","meskipun","semula","mungkin","mungkinkah","nah","namun","nanti","nantinya","nyaris","oleh","olehnya","seorang","seseorang","pada","padanya","padahal","paling","sepantasnya","sepantasnyalah","para","pasti","pastilah","per","pernah","pula","pun","merupakan","rupanya","serupa","saat","saatnya","sesaat","saja","sajalah","saling","bersama","sama","sesama","sambil","sampai","sana","sangat","sangatlah","saya","sayalah","se","sebab","sebabnya","sebuah","tersebut","tersebutlah","sedang","sedangkan","sedikit","sedikitnya","segala","segalanya","segera","sesegera","sejak","sejenak","sekali","sekalian","sekalipun","sesekali","sekaligus","sekarang","sekarang","sekitar","sekitarnya","sela","selain","selalu","seluruh","seluruhnya","semakin","sementara","sempat","semua","semuanya","sendiri","sendirinya","seolah","seperti","sepertinya","sering","seringnya","serta","siapa","siapakah","siapapun","disini","disinilah","sini","sinilah","sesuatu","sesuatunya","suatu","sesudah","sesudahnya","sudah","sudahkah","sudahlah","supaya","tadi","tadinya","tak","tanpa","setelah","telah","tentang","tentu","tentulah","tentunya","tertentu","seterusnya","tapi","tetapi","setiap","tiap","setidaknya","tidak","tidakkah","tidaklah","toh","waduh","wah","wahai","sewaktu","walau","walaupun","wong","yaitu","yakni","yang","untuk","untukmu","untuknya","untukku","nya","pun","se","sekedar","dirut","terlalu","sebelah","antitesa","blusuk","an","sebelum","aa","abis","ad","aj","ajk","alm","almt","ank","ap","aq","aqu","asek","asik","ati2","ato","atw","awl","ayang","ayok","ayuk","ayukz","bag","bales","bantuin","bbrp","benr","bg","bgg","bgian","bgmn","bgs","bgt","bgtu","bgus","bhs","bhsa","bju","bk","bka","bkn","bkr","blan","bleh","blh","bli","blkg","blkng","blm","bln","blom","bls","blum","bnar","bner","bngt","bnr","bntr","bnyk","bodo","boong","bosen","bosenin","bp","bpk","brg","brng","brp","brpa","bs","bsa","bsar","bsh","bsk","bsn","bsok","bsr","bw","bwt","byk","cape","cbt","ce","cepet","cew","ckp","clana","cnth","cntik","cntk","co","cp","cpt","cr","cth","cuekin","da","dah ","dg","dgn","dikit","dj","dkat","dket","dkt","dlam","dll","dlm","dn","dng","dosn","dpn","dpt","dsb","dsn","dtg","dtng","elo","elu","elu ","emg","emng","engga'","ente","fak","fikir","ga","ga'","gak","gapapa","gd","gde","ggu","gini","gitchu","gitu","gk","gmn","gmpng","gn","gnggu","gpp","gt","gua","guwe","gw","gy","haha","hahaha","hapal","hbgn","hbis","hbngn","hbs","hbt","hee","hehe","hehehe","hihi","hihihi","hiks","hr","hrf","hrg","hri","hsil","hsl","ht2","hub","http","https","ja","jd","jg","jgan","jgn","jk","jl","jlan","jlek","jln","jm","jml","jmlh","jmt","jngn","jrg","jrng","ju2r","jur","jursn","kacian","kaco","kagak","kalo","karisma","kasian","katrok","kcl","kdg","kdng","kecian","kesian","kharisma","kharismatik","kl","klo","km","kmnangan","kmrn","knp","kongkrit","kpn","krg ","krm","krn","krng","ktawa","kul","kulyh","ky","lap","laper","lbh","lbih","lg","lht","liat","lk","lo","lol ","lom","lp","lpa","lpr","lu","lum ","maap","maba","makacih","makasi","makasih","males","malming","masi","mcem","mcm","mdh","met","mg","mggu","mgk","mgkn","mgnggu","mgu","mhs","mhsw","mkn","mks","mksd","mksh","mlm","mls","mlu","mnang","mngkn","mnrt","mnurut","mo","mrh","msh","msk","mslh","msuk","mudh","mw","napa","ndak","ngak","ngalah","ngapa","ngapain","ngebosenin","ngga","nggak","ngurus","ngurusin","ni","nnt","nnti","np","nt","nti","ntr","nulis","nunggu","ny","nyimak","org","orng","pa","pd","pdhl","pengen","pg","pingin","pinter","pk","pke","pkl","plg","plh","pny","psg","psng","pusng","py","qm","rbu","rmh","sbg","sbgn","sbntr","sbt","scr","scra","sdh","sdkt","sdr","selaen","sem","sempet","seneng","sgl","sgt","sht","sj","skit","sklh","skolah","skr","skrg","skt","skul","slamat","slasa","slg","sll","sllu","slmt","slng","slsa","slse","slu","sm","smg","smngt","smp","smpai","smpe","smt","smtr","smua","smw","snang","sndri","snen","sneng","sng","sngt","snin","snyum","sono ","sono ","sp","spa","sprti","spt","spti","spy","srt","ssh","sumpe","surt","sush","sy","syp","t4","tauladan","tbh","td","tdi","tdi","tdk","tdr","tgas","tgl","tgs","thn","thx","ti2","tidk","tinggl","titi","tlg","tlng","tmn","tmpt","tnggl","tnp","tny","tnya","toladan","tp","trims","trs","trus","ttp","ttp ","tu","tu2p","tugs","tuk","tw","uda","udh","utk","wkwkwk","wnt","wrn","wrna","xixixi","yg","yng","yukz","yups","lsg","ha","he","hi","iki","nih","dimana","kok","karenanya","sinilah","itulah","inilah","dll","de el el","situ","it","toh","artinya","sebagainya","sebagai","shbt","diri","dirimu","diriku","dirinya","lah","kah","dah","iya","ah","ih","oh","wah","wuih","weh","gimana","in","http","tidak","tak","bukan","saw","swt","ra","jam","jadi","sama","nya","mu","ku ","setiap","stlh","dq","semakin","kpd","jangan","banyak","bisa","hal","darinya","ingin","sebenarnya","lebih","perlu","yaa","amp","quwh","qu","dpu","qs","rt","slrh","sbb","ds","mq","sd","smp","sma","tar","jkt","kok","koq","and","the","rp","dr","yi","cc","sblm","bnr","on","in","jan","jak","kyk","wkt","tu","tuh","ttg","asy","asp","dis","is","si","qt","do","bhw","slh","by","to","say","sblh","dll","dkk","akn","am","thd","www","no","lho","go","my","pic","trhdp","thd","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","el","ul","ol","lol","xi","cont","htt","thd","thdp"]
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
