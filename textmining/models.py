from django.db import models
import os
import textract
import nltk

from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

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
                resultado.append(resultWords)
        retorno = {
            'status_code': 200,
            'result': resultado
        }
        return retorno
    