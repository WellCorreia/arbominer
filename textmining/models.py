from django.db import models
import os
import textract
import mysql.connector
import nltk
import matplotlib.pyplot as plt
import numpy as np

from mysql.connector import Error, errorcode
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

class TextMining(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_pubmed = models.IntegerField(default=0)
    serotype = models.CharField(max_length=200)
    word_repetion = models.CharField(max_length=200)
    link_pubmed = models.CharField(max_length=200)

    def __init__(self):         
        self.connection = None                                   
        self.exceptWords = set(stopwords.words('english'))       
        self.filterText = ['age', 'gender', 'fever', 'woman', 'women', 'man', 'men', 'child', 'children']   
        self.wordsForGraphic = None                              
        self.wordsRepetition = None                              
        self.codPubmedFile = None                                
        self.typeVirus = None                                    
        self.fileName = None                

    def returnWords(self):                                    
        linkPubmed = 'https://www.ncbi.nlm.nih.gov/pubmed/'+self.codPubmedFile                         
        words = "".join(str(x) for x in self.wordsRepetition)
        values = {
            self.codPubmedFile,
            self.typeVirus,
            words,
            linkPubmed
        }
        return values

    def readPdf(self, pathToFile, words, analise):
        result = None
        pdf_file = textract.process(pathToFile, encoding='utf-8').decode('utf-8')
        if(analise == '1'):
            token = self.tokenizer(pdf_file) 
            result = self.filterWords(token, words)
        else:
            token = word_tokenize(pdf_file)
            result = self.getContext(token, words)             
        print(result)
        return result                                
        
    def getContext(self, token, words):
        tagged_sent = nltk.pos_tag(token)
        cp = nltk.RegexpParser('NP: {<PRP>?<VBD>?<VBN>?<IN>?<DT>?<NN>?<IN>?<JJ>?<NN|NNS|NNP>?<IN>?<NN|NNS|NNP>?<CC>?<NN|NNS|NNP>?}')
        parsed_sent = cp.parse(tagged_sent)
        phrase = []
        for npstr in self.extract_np(parsed_sent):
            token = word_tokenize(npstr.lower())
            stopwords = None
            stopwords = [x for x in token if x in words]
            if(stopwords and len(token) >= 5):
                phrase.append(npstr)
        return phrase
    
    def extract_np(self, psent):
        for subtree in psent.subtrees():
            if subtree.label() == 'NP':
                yield ' '.join(word for word, tag in subtree.leaves())   
        
    def tokenizer(self, read_pdf):                              
        token = []
        token.append(word_tokenize(read_pdf.lower()))           
        return token
    
    def filterWords(self, token, words):                               
        wordsRepetition = []
        wordsForGraphic = []
        words = [x.lower() for x in words]
        concact = []
        for listWords in token: 
            # stopwords = [x for x in listWords if x not in exceptWords]
            stopwords = [x for x in listWords if x in words]                                      
            concact = concact + stopwords                        
            
        wordsForGraphic = FreqDist(concact)                      
        wordsRepetition = wordsForGraphic.most_common()
        return wordsRepetition
        
    def preparateDataForGraphic(self, forGraphic, typeVirus):
        list_word = []
        qtd_cited_file = None
        label = []
        value = []
        for words in forGraphic:
            list_word.append(words[0])
        qtd_cited_file = dict(Counter(list_word))
        for elements in qtd_cited_file:
            label.append(elements)
            value.append(qtd_cited_file[elements])
        self.generateGraphic(label, value, typeVirus)
        
    def generateGraphic(self, label, value, typeVirus):
        fig, ax = plt.subplots(figsize=(10,6))
        plt.bar(label, value, label = 'Total de Arquivos', color = 'b')
        ax.grid(which='major', linestyle='--', linewidth='0.2', color='gray')
        ax.xaxis.grid(False)
        plt.title('Quantidade de arquivos com os termos citados')
        plt.xlabel('Termos')
        plt.ylabel('Quantidade de arquivos')
        plt.legend(loc='best')
        for i, v in enumerate(value):
            plt.text(i, v + 0.5, str(v), ha='center')
        fig.savefig('static/graphic/termosEncontradoEmArquivo'+typeVirus+'.png')
        plt.close()

    def getWords(self, words, typeV, analise):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        defaultWords = ['fever', 'rash', 'conjunctivitis', 'muscle', 'pain', 'joint', 'malaise', 'headache', 'microcephaly', 'Guillain-Barré', 'neuropathy',  'myelitis']
        if(words == ['']):
            words = defaultWords
        init = TextMining()
        finalPath = '\\static\\pdf\\{}\\'.format(typeV)
        pathToFolder = BASE_DIR + finalPath
        pathToFile = None 
        codPubmedFile = None
        typeVirus = None 
        resultado = []
        resultWords = None
        forGraphic = []
        for fileName in os.listdir(pathToFolder):
            if fileName.endswith('.pdf'):
                pathToFile = pathToFolder + fileName 
                codPubmedFile = fileName.split('-')[0]
                if(fileName.split('-')[1].split('.')[0] != 'CHIKV' and fileName.split('-')[1].split('.')[0] != 'ZIKA'):
                    typeVirus = fileName.split('-')[1]+'-'+fileName.split('-')[2]
                else:
                    typeVirus = fileName.split('-')[1]
                typeVirus = typeVirus.split('.')[0]
                resultMining = init.readPdf(pathToFile, words, analise)
                linkPubmed = 'https://www.ncbi.nlm.nih.gov/pubmed/'+codPubmedFile
                resultWords = {
                    'resultado': resultMining,
                    # 'resultado': None,
                    'typeVirus': typeVirus,
                    'pathToFile': {
                        'uri': '../static/pdf/'+typeV+'/'+fileName,
                        'fileName': fileName,           
                        },
                    'linkPubmed': linkPubmed,
                    'fileName': fileName,
                }
                if(analise == '1'):
                    forGraphic = resultMining + forGraphic
                # forGraphic.append(qtdWords)
                resultado.append(resultWords)
        if(analise == '1'):
            # init.preparateDataForGraphic(forGraphic, typeVirus)
            pass
        retorno = {
            'status_code': 200,
            'result': resultado
        }
        return retorno
    